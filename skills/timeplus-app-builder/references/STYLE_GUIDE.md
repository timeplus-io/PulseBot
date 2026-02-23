# Timeplus Application Style Guide

Source: https://gist.github.com/gangtao/5307e8bbb84384804c7fb9480a515925

---

## Design Principles

1. **Dark-first** — All Timeplus apps use a dark theme. Never ship a light-mode app without an explicit request.
2. **Data density** — Maximize information per pixel. Avoid decorative whitespace.
3. **Live awareness** — Always show whether the app is connected and streaming.
4. **Monospace for data** — All numeric values, SQL, and raw data use monospace font.
5. **Subtle motion** — Streaming updates should feel fluid, not jarring.

---

## Color Palette

### Background layers (darkest → lightest)
```
--tp-bg-primary:    #0f1117   /* Page background */
--tp-bg-secondary:  #1a1d27   /* Header, sidebar, nav */
--tp-bg-card:       #1e2235   /* Cards, panels */
--tp-bg-hover:      #252a3a   /* Interactive hover states */
--tp-bg-overlay:    #2e3450   /* Modals, dropdowns */
```

### Brand / Accent colors
```
--tp-accent-primary:    #7c6af7   /* Timeplus purple — primary actions, links */
--tp-accent-secondary:  #4fc3f7   /* Cyan — data, streaming indicators */
--tp-accent-success:    #4caf82   /* Green — OK / connected */
--tp-accent-warning:    #f7a84f   /* Orange — warnings */
--tp-accent-danger:     #f76f6f   /* Red — errors, alerts */
```

### Text
```
--tp-text-primary:   #e8eaf6   /* Main text */
--tp-text-secondary: #9ea3b8   /* Labels, subtitles */
--tp-text-muted:     #5c6380   /* Disabled, placeholders */
```

### Borders
```
--tp-border:       #2e3450   /* Default border */
--tp-border-hover: #4a5280   /* Hover border */
```

---

## Typography

```
Font stack (sans):  'Inter', system-ui, -apple-system, sans-serif
Font stack (mono):  'JetBrains Mono', 'Fira Code', 'Consolas', monospace

Base size:    14px
Line height:  1.5

Heading lg:   20px, weight 600
Heading md:   16px, weight 600
Heading sm:   13px, weight 600, uppercase, letter-spacing 0.04em
Body:         14px, weight 400
Small:        12px
Tiny:         11px
```

---

## Spacing

```
4px   — tight (icon gap)
8px   — inner padding (badge, chip)
12px  — small gap (card internals)
16px  — card padding, section gap
20px  — main content padding
24px  — page-level horizontal gutter
32px  — large section separation
```

---

## Borders & Radius

```
--tp-radius-sm:  4px   /* Buttons, inputs, chips */
--tp-radius-md:  8px   /* Tooltips, dropdowns */
--tp-radius-lg:  12px  /* Cards, panels */
--tp-radius-xl:  16px  /* Full panels */

--tp-shadow:     0 2px 12px rgba(0, 0, 0, 0.4)
--tp-shadow-lg:  0 8px 32px rgba(0, 0, 0, 0.6)
```

---

## Layout Patterns

### App Shell
```
+------------------------------------------+
| HEADER  56px  [Logo] [Title] [Badge]      |
+------------------------------------------+
| MAIN CONTENT (flex/grid, padding 20/24)  |
|  +--------+  +-----------+  +----------+ |
|  | Card   |  | Card      |  | Card     | |
|  |        |  |           |  |          | |
|  +--------+  +-----------+  +----------+ |
+------------------------------------------+
```

- Header: `height: 56px`, `background: var(--tp-bg-secondary)`, bottom border
- Main: `padding: 20px 24px`, `gap: 16px`, CSS grid or flex wrap
- Cards: `background: var(--tp-bg-card)`, border, `border-radius: var(--tp-radius-lg)`

### Multi-panel Dashboard
Use CSS Grid with named areas:
```css
.tp-main {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 200px 1fr;
  gap: 16px;
}
```

---

## Components

### Card
```html
<div class="tp-card">
  <div class="tp-card-title">THROUGHPUT</div>
  <!-- content -->
</div>
```

### Status Badge (live indicator)
```html
<!-- Connected -->
<span class="tp-status">
  <span class="tp-status-dot connected"></span>
  LIVE
</span>

<!-- Error -->
<span class="tp-status">
  <span class="tp-status-dot error"></span>
  DISCONNECTED
</span>
```

### "LIVE" badge in header
```html
<span class="tp-header-badge">LIVE</span>
```
Style: `background: #7c6af7`, `color: white`, `border-radius: 99px`, `padding: 2px 8px`, `font-size: 11px`

### Error panel
```html
<div class="tp-error">
  Connection failed: HTTP 404 — stream not found
</div>
```

---

## Vistral Integration

Chart containers should have:
```css
.chart-container {
  background: var(--tp-bg-card);
  border: 1px solid var(--tp-border);
  border-radius: var(--tp-radius-lg);
  padding: 16px;
  min-height: 250px;
}
```

Always pass `theme="dark"` to Vistral components.

Use the **Midnight** palette for brand consistency (`findPaletteByLabel('Midnight')`).

---

## Do / Don't

| DO | DON'T |
|----|-------|
| Dark background `#0f1117` | White or light backgrounds |
| Purple `#7c6af7` for primary actions | Bright red or green for primary |
| Monospace for numbers and data | Proportional font for values |
| Show live/disconnected status | Hide connection state |
| CSS variables for all colors | Hard-coded hex values |
| Dense information layout | Excessive padding / decorative space |
| `border-radius: 12px` for cards | Sharp corners or over-rounded pills |
| `font-weight: 600` for labels | Bold body text |
