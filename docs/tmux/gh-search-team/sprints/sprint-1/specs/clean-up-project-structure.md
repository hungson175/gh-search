# Technical Specification: Clean Up Project Structure

**Sprint:** sprint-1
**Priority:** P0 (Highest)
**Estimated Effort:** 1-2 hours
**Created by:** Tech Lead
**Date:** 2026-01-01

---

## Overview

Reorganize project structure to clearly separate production code, utility scripts, and experimental/trial code. Establish TDD boundaries and create a sustainable sprint folder structure for ongoing development.

## Requirements Analysis

### Functional Requirements
- Create `experiments/` folder for exploratory/trial code
- Move `test_connections.py` from `scripts/` to `experiments/`
- Maintain `scripts/` for production-ready utilities only
- Ensure clean separation of concerns
- Document folder structure in README.md

### Non-Functional Requirements
- Performance: No impact (file reorganization only)
- Quality: Clear, documented structure
- Security: No sensitive data in repository (enforce via .gitignore)
- Maintainability: Self-documenting folder organization

## Progressive Development Plan ⚡ CRITICAL

**NEVER build everything at once. Always progressive:**

### Phase 1: Minimal (Create Basic Structure)
- **Goal:** Create `experiments/` folder and move one file
- **Scope:**
  - Create `experiments/` directory
  - Move `test_connections.py` to `experiments/`
  - Add `experiments/` to .gitignore (for temporary outputs)
- **Success:** File moved, git recognizes rename
- **Time:** 5 minutes

### Phase 2: Medium (Documentation & Validation)
- **Goal:** Update documentation and validate structure
- **Scope:**
  - Update README.md with folder structure explanation
  - Review .gitignore completeness
  - Verify all folders have appropriate __init__.py or lack thereof
  - Create sprint folder template
- **Success:** README clearly explains structure, .gitignore is complete
- **Dependencies:** Phase 1 complete

### Phase 3: Full (Sprint Structure & Final Validation)
- **Goal:** Complete sprint folder structure and final review
- **Scope:**
  - Document sprint folder pattern in team docs
  - Create SPRINT_BACKLOG.md for sprint-1
  - Final validation of all changes
  - Commit with clear message
- **Success:** All acceptance criteria met
- **Dependencies:** Phase 2 validates approach

## Technical Approach

### Architecture

Current structure:
```
gh-search/
├── scripts/
│   ├── fetch_readmes.py     # Production script
│   └── test_connections.py  # Exploratory (MOVE TO experiments/)
├── src/gh_search/           # Production code (TDD required)
├── tests/                   # Tests for src/
├── docs/                    # Documentation
└── ...
```

Target structure:
```
gh-search/
├── src/gh_search/           # PRODUCTION CODE (TDD required)
│   ├── __init__.py
│   └── ...
├── tests/                   # TESTS (pytest) - mirrors src/
│   ├── __init__.py
│   └── ...
├── scripts/                 # PRODUCTION-READY UTILITIES
│   └── fetch_readmes.py     # May have tests if complex
├── experiments/             # TRIAL/LEARNING CODE (NO tests required)
│   └── test_connections.py  # Exploratory scripts
├── docs/
│   ├── tmux/gh-search-team/
│   │   └── sprints/
│   │       ├── sprint-1/
│   │       │   ├── specs/
│   │       │   └── SPRINT_BACKLOG.md
│   │       └── templates/
│   └── ...
└── ...
```

### Technology Choices
- **Language:** Python 3.11
- **Frameworks:** None (file reorganization)
- **Libraries:** None
- **Rationale:** Simple file system operations

### File Structure

**New Files:**
```
experiments/
  └── test_connections.py (moved from scripts/)
docs/tmux/gh-search-team/sprints/
  └── sprint-1/
      ├── specs/
      │   └── clean-up-project-structure.md (this file)
      └── SPRINT_BACKLOG.md
```

**Modified Files:**
```
README.md                    # Add folder structure section
.gitignore                   # Add experiments/ outputs if needed
```

## API Design (if applicable)

N/A - This is a file reorganization task, no API changes.

## Test-Driven Development (TDD) Plan

**CRITICAL: This is a structural task, not code implementation.**

Since this task involves file reorganization (not code implementation), traditional TDD doesn't apply. However, we will follow a **verification-first approach**:

### Verification Steps (Instead of Tests)

1. **Verify folder creation:**
   - Check `experiments/` exists: `ls -la experiments/`

2. **Verify file move:**
   - Check `test_connections.py` in `experiments/`: `ls experiments/test_connections.py`
   - Check it's removed from `scripts/`: `! ls scripts/test_connections.py`

3. **Verify git recognizes rename:**
   - Check git status shows rename, not delete+add: `git status`

4. **Verify documentation updated:**
   - Check README.md has folder structure section
   - Check .gitignore has appropriate entries

5. **Verify sprint structure:**
   - Check sprint-1 folder exists with specs/
   - Check SPRINT_BACKLOG.md created

### TDD Workflow for DEV

Since this is structural work:
```
1. Create experiments/ folder
2. Move test_connections.py
3. Verify with ls/git commands
4. Update README.md
5. Verify README content
6. Create sprint structure
7. Verify sprint structure
8. Commit
```

## Implementation Steps

**For DEV to follow:**

### Phase 1: Create Basic Structure (5 min)

1. **Create experiments folder:**
   ```bash
   mkdir -p experiments
   ```

2. **Move test_connections.py:**
   ```bash
   git mv scripts/test_connections.py experiments/
   ```

3. **Verify move:**
   ```bash
   ls -la experiments/
   git status  # Should show rename, not delete+add
   ```

4. **Commit Phase 1:**
   ```bash
   git add -A
   git commit -m "refactor: move test_connections.py to experiments/

   - Created experiments/ for exploratory code
   - Moved test_connections.py from scripts/ to experiments/
   - This is trial code, not production-ready"
   ```

### Phase 2: Documentation & Validation (10 min)

5. **Update README.md:**
   - Add "Folder Structure" section (see template below)
   - Explain TDD requirements for each folder

6. **Review .gitignore:**
   - Check if experiments/ outputs need ignoring
   - Add patterns if needed (e.g., `experiments/*.log`)

7. **Verify folders:**
   ```bash
   # src/ should have __init__.py (it's a package)
   ls src/gh_search/__init__.py

   # tests/ should have __init__.py
   ls tests/__init__.py

   # experiments/ should NOT have __init__.py (not a package)
   ! ls experiments/__init__.py

   # scripts/ should NOT have __init__.py (not a package)
   ! ls scripts/__init__.py
   ```

8. **Commit Phase 2:**
   ```bash
   git add README.md .gitignore
   git commit -m "docs: update README with folder structure

   - Added Folder Structure section
   - Documented TDD requirements
   - Updated .gitignore for experiments/"
   ```

### Phase 3: Sprint Structure & Final Validation (15 min)

9. **Create sprint folder structure:**
   ```bash
   mkdir -p docs/tmux/gh-search-team/sprints/sprint-1/specs
   ```

10. **Create SPRINT_BACKLOG.md:**
    - Copy template from sprint-0 or create new
    - List P0-1 as first item

11. **Create sprint template folder:**
    ```bash
    mkdir -p docs/tmux/gh-search-team/sprints/templates
    ```

12. **Document sprint pattern:**
    - Update team workflow docs if needed
    - Ensure sprint pattern is clear

13. **Final verification:**
    ```bash
    # Check all changes
    git status
    git diff HEAD

    # Verify structure
    tree -L 3 -I '.venv|__pycache__'
    ```

14. **Commit Phase 3:**
    ```bash
    git add -A
    git commit -m "docs: create sprint-1 folder structure

    - Created sprint-1/specs/ folder
    - Added SPRINT_BACKLOG.md for sprint-1
    - Created sprint templates/ folder
    - Documented sprint folder pattern"
    ```

15. **Report completion to PO:**
    - Send completion message via tm-send
    - Include git log summary
    - Request Tech Lead review (yourself!)

## Acceptance Criteria

**Definition of Done:**
- [x] `experiments/` folder created
- [x] `test_connections.py` moved to `experiments/`
- [x] Git shows rename, not delete+add
- [x] README.md updated with folder structure section
- [x] .gitignore reviewed and updated if needed
- [x] `src/` has __init__.py (is a package)
- [x] `tests/` has __init__.py (is a package)
- [x] `experiments/` NO __init__.py (not a package)
- [x] `scripts/` NO __init__.py (not a package)
- [x] Sprint-1 folder structure created
- [x] SPRINT_BACKLOG.md created
- [x] Sprint template folder created
- [x] All changes committed with clear messages
- [x] Tech Lead reviewed (self-review for this task)

## README.md Template - Folder Structure Section

Add this section to README.md after the project description:

```markdown
## Folder Structure

```
gh-search/
├── src/gh_search/           # PRODUCTION CODE (TDD required ✓)
│   ├── __init__.py          # Python package
│   ├── server.py            # MCP server implementation
│   ├── search.py            # Search engine
│   └── embeddings.py        # Embedding generation
│
├── tests/                   # TESTS (pytest)
│   ├── __init__.py          # Python package
│   ├── test_search.py       # Tests for search.py
│   └── test_embeddings.py   # Tests for embeddings.py
│   # REQUIREMENT: All src/ code MUST have tests (TDD)
│   # Write tests FIRST, then implementation
│
├── scripts/                 # PRODUCTION-READY UTILITIES
│   └── fetch_readmes.py     # Production script for README fetching
│   # May have tests if complex logic
│   # NOT a Python package (no __init__.py)
│
├── experiments/             # TRIAL/LEARNING CODE (NO tests required)
│   └── test_connections.py  # Database connection testing
│   # One-off exploration scripts
│   # Learning/trial code
│   # NOT a Python package (no __init__.py)
│
├── docs/                    # DOCUMENTATION
│   ├── product/             # Product requirements, specs
│   ├── architecture/        # Architecture docs
│   ├── specs/               # Technical specifications
│   └── tmux/gh-search-team/ # Team workflow & sprint docs
│       └── sprints/         # Sprint-specific documentation
│           ├── sprint-1/    # Current sprint
│           │   ├── specs/   # Technical specs for sprint items
│           │   └── SPRINT_BACKLOG.md
│           └── templates/   # Sprint templates
│
└── logs/                    # Application logs (gitignored)
```

### TDD Requirements by Folder

| Folder | TDD Required? | Tests Location |
|--------|---------------|----------------|
| `src/gh_search/` | **YES** ✓ | `tests/` |
| `scripts/` | Optional (if complex) | `tests/` |
| `experiments/` | **NO** | N/A |

**Test-Driven Development (TDD) Workflow:**
1. Write test FIRST (red)
2. Write minimal code to pass (green)
3. Refactor if needed
4. Commit: "test: ..." then "feat: ..."

Goal: >90% coverage for `src/gh_search/`
```
```

## Technical Decisions

### Decision 1: experiments/ vs scripts/
**Rationale:** Clear separation between production-ready utilities and one-off exploratory code.
- `scripts/`: Production-ready, may be used in deployment
- `experiments/`: Trial code, learning, testing connections

### Decision 2: No __init__.py for experiments/ or scripts/
**Rationale:** These are not Python packages, just collections of standalone scripts.
- `src/gh_search/`: IS a package (will be imported)
- `tests/`: IS a package (pytest discovers tests)
- `scripts/`, `experiments/`: NOT packages (standalone scripts)

### Decision 3: Sprint folder structure
**Rationale:** Each sprint gets its own folder for specs, backlogs, and artifacts.
- Pattern: `docs/tmux/gh-search-team/sprints/sprint-N/`
- Keeps sprint artifacts together
- Easy to reference in team communication

---

**Tech Lead Signature:** TL
**Date:** 2026-01-01
