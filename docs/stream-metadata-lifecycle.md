# Stream-Native Metadata Lifecycle Management

PulseBot stores all metadata in Proton append-only streams rather than a traditional mutable database. This document explains the design patterns, query techniques, and trade-offs for each metadata stream.

---

## Core Principle: Event Sourcing on Append-Only Streams

Proton streams are unbounded, append-only logs. Rows are never updated or deleted in place. Instead:

- **Create** → append a new row with `status = 'active'` (or `action = 'install'`)
- **Update** → append a new row with the same stable ID and new field values
- **Delete** → append a tombstone row with `status = 'deleted'` (or `action = 'remove'`)
- **Read (current state)** → query with `LIMIT 1 BY <id> ORDER BY timestamp DESC` to get the latest row per entity

This gives a full audit trail for free and makes the system resilient to crashes: state is always recoverable by re-reading the stream.

---

## Deduplication Pattern

All "get latest state" queries follow the same shape:

```sql
-- Single entity
SELECT * FROM table(pulsebot.<stream>)
WHERE <id_col> = '<value>'
ORDER BY <timestamp_col> DESC
LIMIT 1

-- All entities (deduplicate to one row per entity)
SELECT * FROM table(pulsebot.<stream>)
ORDER BY <timestamp_col> DESC
LIMIT 1 BY <id_col>
```

**Important Proton constraint:** `HAVING` without `GROUP BY` is not supported. To filter after deduplication, wrap in a subquery:

```sql
SELECT * FROM (
  SELECT * FROM table(pulsebot.<stream>)
  ORDER BY <timestamp_col> DESC
  LIMIT 1 BY <id_col>
) WHERE status != 'deleted'
```

---

## Stable IDs

Each metadata entity uses a **stable, deterministic ID** derived from its natural key (not auto-generated on every insert). This is critical: if the ID changes per-insert, `LIMIT 1 BY <id>` cannot deduplicate across status changes.

| Stream | ID Column | How Generated |
|---|---|---|
| `tasks` | `task_id` | `uuid5(namespace, task_name)` |
| `skills` | `slug` | natural key (skill name) |
| `kanban_projects` | `project_id` | `"proj_" + random hex` (set once at creation) |
| `kanban_agents` | `agent_id` | `"agent_" + name + "_" + project_id` (set once) |

---

## Stream-by-Stream Reference

### `pulsebot.tasks`

**Schema key fields:** `task_id`, `task_name`, `task_type`, `prompt`, `schedule`, `status`, `created_at`

**Stable ID:** `uuid5(NAMESPACE, task_name)` — same task name always yields the same UUID.

#### Create / Update
```python
client.insert("pulsebot.tasks", [{
    "task_id": _task_id(name),   # deterministic
    "task_name": name,
    "task_type": "interval",
    "prompt": prompt,
    "schedule": "15m",
    "status": "active",
}])
```
Re-inserting with the same `task_id` and new fields acts as an update — the latest row wins.

#### Delete (tombstone)
```python
client.insert("pulsebot.tasks", [{
    "task_id": _task_id(name),
    "task_name": name,
    "status": "deleted",
    # other fields can be empty
}])
```

#### Read (current state, exclude deleted)
```sql
SELECT task_id, task_name, task_type, prompt, schedule, status, created_at, created_by
FROM (
  SELECT * FROM table(pulsebot.tasks)
  ORDER BY created_at DESC
  LIMIT 1 BY task_id
) WHERE status != 'deleted'
```

#### Notes
- The Timeplus Task (the scheduler engine object) is managed separately via `CREATE TASK` / `DROP TASK IF EXISTS`. The `pulsebot.tasks` stream is purely the metadata mirror for UI display.
- `DROP TASK` must always be paired with a tombstone insert so the UI reflects the deletion.

---

### `pulsebot.skills`

**Schema key fields:** `slug`, `version`, `content_hash`, `source`, `action`, `installed_at`, `created_at`

**Stable ID:** `slug` (the skill's natural name, e.g. `"searxng-web-search"`).

**Delete semantics:** uses `action = 'remove'` tombstone instead of a `status` field.

#### Create (install)
```python
client.insert("pulsebot.skills", [{
    "slug": "searxng-web-search",
    "version": "1.2.0",
    "content_hash": "abc123",
    "source": "clawhub",
    "action": "install",
    "installed_at": "2026-01-01T00:00:00Z",
}])
```

#### Update (re-install / upgrade)
Re-insert with `action = 'install'` and the new version. The `GROUP BY slug` + `arg_max` picks the latest values.

#### Delete (tombstone)
```python
client.insert("pulsebot.skills", [{
    "slug": "searxng-web-search",
    "version": "",
    "content_hash": "",
    "source": "",
    "action": "remove",
    "installed_at": "",
}])
```

#### Read (currently installed)
```sql
SELECT name, version, content_hash, source, installed_at FROM (
  SELECT slug AS name,
         arg_max(version,      created_at) AS version,
         arg_max(content_hash, created_at) AS content_hash,
         arg_max(source,       created_at) AS source,
         arg_max(installed_at, created_at) AS installed_at,
         arg_max(action,       created_at) AS action
  FROM table(pulsebot.skills)
  GROUP BY slug
) WHERE action != 'remove'
```

**Why not `GROUP BY` + `arg_max`?** Both patterns produce equivalent results when every insert is a complete row. `LIMIT 1 BY` is simpler and consistent with the other streams. `arg_max` is only needed if partial-row updates are intentional (e.g. only updating one field without repeating all others) — skills does not do this.

---

### `pulsebot.kanban_projects`

**Schema key fields:** `project_id`, `timestamp`, `name`, `description`, `status`, `session_id`, `agent_ids`, `is_scheduled`, `schedule_type`, `schedule_expr`, `trigger_prompt`, `event_query`, `context_field`

**Stable ID:** `project_id` — assigned once at project creation (`"proj_" + random hex`), reused on every subsequent status update.

#### Create
Written once when the project is first created with `status = 'active'` and all scheduling fields populated.

#### Update (status change)
The `ManagerAgent._update_project_status()` re-inserts a **complete** row (all fields) with the new status. Partial rows are avoided because `LIMIT 1 BY project_id` returns the entire latest row — if scheduling fields are omitted, the UI sees blank values.

```python
client.insert("pulsebot.kanban_projects", [{
    "project_id": self.project_id,
    "name": self.project_name,          # must carry forward
    "description": self.project_description,  # must carry forward
    "status": "completed",
    "session_id": self.session_id,
    "agent_ids": [...],
    "is_scheduled": ...,
    "schedule_type": ...,
    # all fields populated
}])
```

#### Delete
Uses physical `DELETE FROM` (not a tombstone), because cancelled projects are removed entirely rather than logically soft-deleted:

```python
client.execute(f"DELETE FROM pulsebot.kanban_projects WHERE project_id = '{pid}'")
```

This is the one exception to the append-only pattern. It is acceptable here because project cancellation is an intentional, permanent operation — there is no need for an audit trail of the deletion event.

#### Read (latest state per project)
```sql
SELECT project_id, name, description, status, session_id, timestamp
FROM table(pulsebot.kanban_projects)
ORDER BY timestamp DESC
LIMIT 1 BY project_id
```

#### Read (single project)
```sql
SELECT * FROM table(pulsebot.kanban_projects)
WHERE project_id = '<id>'
ORDER BY timestamp DESC
LIMIT 1
```

---

### `pulsebot.kanban_agents`

**Schema key fields:** `agent_id`, `timestamp`, `project_id`, `name`, `role`, `task_description`, `target_agents`, `status`, `skills`, `checkpoint_sn`

**Stable ID:** `agent_id` — set once at agent construction.

#### Create
Written by `_write_agent_metadata()` when a project is created. One row per agent (including the manager).

#### Update (checkpoint)
`SubAgent._persist_checkpoint()` appends a new row with the updated `checkpoint_sn`. All other fields must be carried forward to avoid the "blank on latest-row read" problem.

#### Delete
Same physical `DELETE FROM` as `kanban_projects`, scoped to the project:
```python
client.execute(f"DELETE FROM pulsebot.kanban_agents WHERE project_id = '{pid}'")
```

#### Read (latest state per agent in a project)
```sql
SELECT agent_id FROM table(pulsebot.kanban_agents)
WHERE project_id = '<id>'
ORDER BY timestamp DESC
LIMIT 1 BY agent_id
```

---

## Pattern Comparison

| Stream | ID type | Delete style | Dedup query | Full-row on update? |
|---|---|---|---|---|
| `tasks` | Deterministic uuid5 | Status tombstone | `LIMIT 1 BY task_id` | No (only changed fields needed) |
| `skills` | Natural key (slug) | Action tombstone | `LIMIT 1 BY slug` | No (only changed fields needed) |
| `kanban_projects` | Random hex prefix | Physical DELETE | `LIMIT 1 BY project_id` | **Yes — required** |
| `kanban_agents` | Constructed string | Physical DELETE | `LIMIT 1 BY agent_id` | **Yes — required** |

---

## Key Rules

1. **Stable IDs are mandatory.** Auto-generated UUIDs (`DEFAULT uuid()`) on every insert break `LIMIT 1 BY` deduplication — every row gets a unique key and nothing is deduplicated. Use `uuid5` for name-keyed entities, or pass an explicit ID set at creation time.

2. **Full-row updates for `LIMIT 1 BY` streams.** When using `LIMIT 1 BY <id>`, the latest row is returned wholesale. If a status-update row omits non-status fields, those fields will appear blank in queries. Always carry all fields forward on every write.

3. **Partial rows are safe only with `GROUP BY` + `arg_max`.** Each `arg_max(field, timestamp)` resolves independently, so different writes can contribute different fields. This is the `skills` pattern.

4. **Tombstones for audit-trail-required deletions.** Use a status/action tombstone (tasks, skills) when the deletion record itself has value or when the entity may reappear with the same ID.

5. **Physical DELETE for ephemeral lifecycle entities.** Use `DELETE FROM` (kanban_projects, kanban_agents) when the data has no value after the entity is gone and reuse of the same ID is not expected.

6. **Filter after deduplication using subqueries.** Proton 3.0.18 does not support `HAVING` without `GROUP BY`. Wrap the deduplication query in a subquery and apply `WHERE` on the outer level.
