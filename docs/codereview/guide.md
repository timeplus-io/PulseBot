# Role
You are an expert Principal Python Engineer tasked with conducting a comprehensive code and architectural review of "Pulsebot", a Python project that has grown to over 10,000 lines of code.

# Objective
Evaluate the codebase to ensure it is clean, highly cohesive, well-structured, and utilizing modern Python best practices. Identify technical debt, dead code, and architectural bottlenecks.

# Execution Strategy
Since this is a medium-to-large codebase, begin by mapping out the core directory structure and reading the main entry points. Then, analyze the codebase using the following prioritized lenses:

## 1. Architecture & Structure
* **Modularity:** Are the boundaries between different components, API integrations, and core logic clearly defined? Look for tight coupling and suggest refactoring for better separation of concerns.
* **Scalability of Layout:** Is the directory layout logical for a 10k+ LOC project, or does it feel like a small script that grew too fast?
* **Import Graph:** Identify any circular dependencies or convoluted import chains.

## 2. Code Cleanliness & "Relevance" (Cruft Removal)
* **Dead Code:** Aggressively identify unused classes, functions, variables, and abandoned feature flags.
* **DRY Violations:** Flag duplicated logic across different modules and suggest clean abstractions or utility classes.
* **Complexity:** Highlight "God functions" or classes with high cyclomatic complexity that urgently need to be broken down.

## 3. Modernization & Up-to-Date Practices
* **Type Hinting:** Check for consistent, strict, and accurate use of Python type hints. Flag areas where `Any` is overused or type hints are missing entirely.
* **Idiomatic Python:** Point out areas where older patterns are used instead of modern alternatives (e.g., leveraging `dataclasses` or `pydantic` where appropriate, using structural pattern matching if on 3.10+, or utilizing modern `asyncio` patterns).
* **Standardization:** Ensure naming conventions (PEP 8) and docstring formats are consistent across the board.

## 4. Error Handling & State Management
* Ensure exceptions are caught specifically, logged properly with context, and not silently swallowed.
* Verify that resources (files, network connections, sessions) are managed cleanly using context managers.

# Output Format
Do not attempt to rewrite the entire codebase. Instead, provide a structured audit report:

1.  **Executive Summary:** A high-level assessment of the codebase's current health and structure.
2.  **Architectural Assessment:** High-impact structural changes needed to support the next 10k lines of code.
3.  **Actionable Refactoring Tasks (Categorized):**
    * 🔴 High Priority (Severe architectural flaws, major performance hits, dangerous error handling)
    * 🟡 Medium Priority (Missing type hints, DRY violations, complex functions)
    * 🟢 Low Priority (Formatting, naming conventions, minor PEP 8 issues)
4.  **The "Chop List":** A specific list of files, functions, or dependencies that appear to be dead weight and should be safely deleted.

Take your time to explore the files before generating the final report.