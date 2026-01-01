# gh-search Team Workflow

**Team Type:** 3-Person Scrum Team (Simplified)
**Project:** GitHub Project Search MCP Server
**Working Directory:** `/home/hungson175/dev/mcp-servers/gh-search`

---

## Team Structure

### Roles

**PO (Product Owner)** - Pane 0
- Manages Product Backlog
- Selects sprint items and prioritizes
- Final approver for all work
- Communicates with BOSS (human user)

**TL (Tech Lead)** - Pane 1
- Creates technical specs for sprint items
- Reviews all code implementations
- Makes technical decisions
- Ensures quality and best practices

**DEV (Developer)** - Pane 2
- Implements features using Test-Driven Development (TDD)
- Writes tests FIRST, then code to pass tests
- Follows Tech Lead's specifications
- Reports completion to PO via TL

### Communication Flow

```
BOSS (Human User)
    ↓
   PO (Hub - All communication flows through PO)
    ↓
   TL (Specs & Review)
    ↓
  DEV (TDD Implementation)
    ↓
   TL (Code Review)
    ↓
   PO (Final Approval)
```

**CRITICAL:** All inter-agent communication goes through PO. Never direct TL ↔ DEV.

---

## Sprint Workflow (10 Steps)

### Before Sprint: Backlog Management

**PO manages PRODUCT_BACKLOG.md:**
- Reviews items from BOSS
- Prioritizes by business value
- Selects items for next sprint
- Moves to SPRINT_BACKLOG.md

### Step 1: Sprint Assignment

**PO → TL:**
- Assigns sprint item from SPRINT_BACKLOG
- Provides context and requirements
- References Product Backlog for details

**Message Format:**
```
PO [HH:mm]: Sprint assigned - [Item Name]. See PRODUCT_BACKLOG.md for details. Priority: P0/P1/P2.
```

### Step 2: Tech Lead Creates Spec

**TL creates specification:**
- File: `docs/specs/[sprint-item].md`
- Includes: Requirements, architecture, API design, test plan
- **Guards Progressive Approach:** Break into small increments
- **Technical Decisions:** Framework choices, patterns, structure

**Spec Template:**
```markdown
# Specification: [Sprint Item Name]

## Overview
[Brief description]

## Requirements
- Functional requirements
- Non-functional requirements
- Acceptance criteria

## Technical Approach
- Architecture decisions
- Implementation strategy
- PROGRESSIVE PLAN: [small → medium → full]

## API Design
[If applicable]

## Test Plan
- Unit tests required
- Integration tests required
- Test scenarios

## Implementation Steps (TDD)
1. Write test for X
2. Implement X to pass test
3. Write test for Y
4. Implement Y to pass test
...

## Definition of Done
- [ ] All tests written first (TDD)
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documented
- [ ] Committed to Git
```

### Step 3: TL → PO (Spec Review)

**TL → PO:**
```
TL [HH:mm]: Spec complete for [Item]. See docs/specs/[file].md. Ready for DEV assignment?
```

**PO reviews spec, approves or requests changes**

### Step 4: PO → DEV (Sprint Assignment with Spec)

**PO → DEV:**
```
PO [HH:mm]: Sprint assigned to DEV - [Item Name]. Tech Lead spec at docs/specs/[file].md. Use TDD: tests first, code second.
```

**DEV acknowledges:**
```
DEV [HH:mm]: Sprint received. Starting TDD implementation per spec.
```

### Step 5: DEV Implementation (TDD)

**DEV follows Test-Driven Development:**

**For each feature/function:**
1. **Write test FIRST** (in `tests/`)
2. **Run test** - should FAIL (red)
3. **Write minimal code** to pass test (green)
4. **Refactor** if needed
5. **Commit** with message: `test: add test for X` then `feat: implement X`

**Progressive Implementation:**
- Start with smallest increment
- Get it working end-to-end
- Scale up gradually
- Commit frequently

**Test Requirements:**
- All `src/` code MUST have tests
- Use pytest
- Async tests use `pytest-asyncio`
- Aim for >90% coverage

### Step 6-7: Clarification Loop

**DEV ↔ PO ↔ TL:**

If DEV needs clarification:
```
DEV [HH:mm]: Question about [X]. Requesting Tech Lead input.
```

PO routes to TL:
```
PO [HH:mm]: DEV question forwarded. See above.
```

TL responds via PO:
```
TL [HH:mm]: Answer to DEV question: [response]. PO please relay.
```

PO relays:
```
PO [HH:mm]: From TL: [response].
```

### Step 8: DEV → PO (Completion Report)

**When sprint item complete:**

```
DEV [HH:mm]: Sprint [Item] complete.
- Tests: X/X passing
- Coverage: Y%
- Files: [list]
- Commits: [git log one-liner]
Ready for Tech Lead review.
```

**Update WHITEBOARD.md with status**

### Step 9: PO → TL (Review Request)

**PO → TL:**
```
PO [HH:mm]: DEV completed [Item]. Requesting code review. See commits: [hash].
```

### Step 10: Tech Lead Review

**TL performs code review:**

**Reviews:**
- [ ] Tests written first (TDD proof in git history)
- [ ] All tests passing
- [ ] Code quality (readability, structure)
- [ ] Follows spec
- [ ] Best practices
- [ ] Documentation

**TL has 3 options:**

**Option A - APPROVED:**
```
TL [HH:mm]: Code review APPROVED for [Item].
- Tests: ✓ All passing
- Coverage: ✓ [X]%
- Quality: ✓ Meets standards
- TDD: ✓ Tests written first (verified in git history)
Ready for PO final approval.
```

**Option B - CHANGES REQUESTED:**
```
TL [HH:mm]: Code review - CHANGES REQUESTED for [Item].
Issues found:
1. [Issue 1]
2. [Issue 2]
Returning to DEV via PO.
```
→ Back to Step 6 (Clarification Loop)

**Option C - NEEDS DISCUSSION:**
```
TL [HH:mm]: Code review - QUESTIONS for [Item]. Need to discuss with DEV via PO.
```
→ Clarification loop

### After Step 10: PO Final Approval

**When TL approves, PO makes final decision:**

**PO reviews:**
- Tech Lead approval report
- Git commits (progressive development)
- Tests passing
- Meets sprint goal

**PO → BOSS:**
```
PO [HH:mm]: Sprint [Item] complete and approved.

Sprint Summary:
- Item: [Name]
- Deliverables: [List]
- Tests: X/X passing
- Tech Lead: Approved
- Git commits: [summary]
- Status: Ready for merge

Awaiting BOSS review and next sprint assignment.
```

**PO updates:**
- SPRINT_BACKLOG.md (mark complete)
- WHITEBOARD.md (status)

---

## BOSS Interaction

**BOSS (human user) appears ONLY:**
1. **Before Sprint 1:** Provides initial requirements/priorities to PO
2. **After Step 10:** Reviews sprint completion, approves, provides next priorities

**BOSS does NOT intervene during Steps 1-10** - team self-coordinates.

**BOSS operates from separate terminal (Boss Terminal):**
- Uses `>>>` prefix to send messages to PO
- Example: `>>> start sprint 1 with P0 project structure`
- PO receives: `BOSS [HH:mm]: start sprint 1 with P0 project structure`

---

## Git Workflow

**All agents use Git to track progress:**

**Commit Message Format:**
```
type: description

[optional body]
```

**Types:**
- `test`: Add or modify tests
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `docs`: Documentation
- `chore`: Tooling, dependencies

**TDD Git Pattern (DEV):**
```bash
# 1. Write test
git add tests/test_feature.py
git commit -m "test: add test for feature X"

# 2. Implement feature
git add src/gh_search/feature.py
git commit -m "feat: implement feature X to pass tests"

# 3. Refactor if needed
git commit -m "refactor: improve feature X code quality"
```

**Branching (optional for small team):**
- `main`: Production-ready code
- `sprint-X`: Sprint work (merge after PO approval)

---

## Progressive Development Principle

**CRITICAL: Always build incrementally**

**Bad:**
```
DEV: Building entire search engine... (3 days later) Done!
```

**Good:**
```
DEV: Step 1 - Basic vector search (working end-to-end)
DEV: Step 2 - Add BM25 (working end-to-end)
DEV: Step 3 - Hybrid ranking (working end-to-end)
DEV: Step 4 - Add filters (working end-to-end)
```

**Each increment:**
- Has tests
- Works end-to-end
- Is committed to Git
- Can be demoed

**Tech Lead guards this principle in specs**

---

## TDD (Test-Driven Development)

**Required for all `src/` code:**

**The TDD Cycle:**
```
1. RED: Write failing test
2. GREEN: Write minimal code to pass
3. REFACTOR: Improve code quality
4. COMMIT: Save progress
```

**Example:**
```python
# tests/test_search.py
def test_vector_search_returns_results():
    """Test that vector search returns relevant results."""
    # ARRANGE
    query = "machine learning framework"

    # ACT
    results = search_engine.vector_search(query, limit=10)

    # ASSERT
    assert len(results) == 10
    assert all(r.relevance_score > 0.5 for r in results)

# NOW implement src/gh_search/search.py to pass this test
```

**Proof of TDD:**
Git history shows test commits BEFORE implementation commits.

---

## File Organization

```
gh-search/
├── src/gh_search/         # PRODUCTION CODE (TDD required)
│   ├── server.py          # MCP server
│   ├── search.py          # Search engine
│   └── embeddings.py      # Embedding generation
├── tests/                 # TESTS (pytest)
│   ├── test_search.py
│   └── test_embeddings.py
├── scripts/               # RUNNABLE SCRIPTS (may have tests)
│   └── fetch_readmes.py
├── experiments/           # TRIAL CODE (NO tests required)
│   └── test_connections.py
└── docs/
    ├── specs/            # Tech Lead specifications
    └── tmux/gh-search-team/  # Team workspace
```

---

## Team Coordination Files

**All agents maintain these:**

1. **WHITEBOARD.md** - Real-time status (PO maintains)
2. **PRODUCT_BACKLOG.md** - All work items (PO manages)
3. **SPRINT_BACKLOG.md** - Current sprint (PO updates)
4. **docs/specs/** - Tech Lead specifications (TL creates)

**Before ANY action, check WHITEBOARD for current status**

---

## Communication Protocols

### Two-Enter Rule (CRITICAL)

All tmux messages require TWO separate commands:

```bash
# CORRECT
tmux send-keys -t %1 "PO [14:30]: Message here" C-m
tmux send-keys -t %1 C-m  # Second Enter!

# WRONG
tmux send-keys -t %1 "Message" C-m C-m  # Doesn't work!
```

### Message Format

```
[ROLE] [HH:mm]: [Brief message]. See [reference].
```

Examples:
- `PO [10:15]: Sprint assigned to DEV. See docs/specs/project-structure.md`
- `DEV [11:30]: Implementation complete. Tests: 12/12 passing.`
- `TL [12:00]: Code review approved. Ready for PO.`

### Update-Then-Notify

Always write files FIRST, then notify:

```bash
# 1. Write spec file
# 2. THEN notify
tmux send-keys -t %2 "TL [10:30]: Spec ready. See docs/specs/feature.md" C-m
tmux send-keys -t %2 C-m
```

---

## Session Resumption

**After tmux restart or auto-compact:**

1. **Read WHITEBOARD.md** - Current status
2. **Read SPRINT_BACKLOG.md** - Active sprint items
3. **Check git log** - Recent commits
4. **Resume work** from last known state

**PO responsibilities after restart:**
- Update WHITEBOARD with current status
- Verify all agents understand their current tasks
- Re-communicate any pending actions

---

## Quality Standards

**Definition of Done (all sprints):**
- [ ] Tests written first (TDD)
- [ ] All tests passing
- [ ] Code follows style guide (black, ruff)
- [ ] Tech Lead reviewed and approved
- [ ] PO approved
- [ ] Documentation updated
- [ ] Committed to Git with clear messages
- [ ] WHITEBOARD updated

**Code Quality:**
- Type hints used
- Docstrings for public APIs
- Black formatted (100 char line length)
- Ruff linting passes
- No obvious bugs or issues

---

## Emergency Procedures

**If team is stuck:**

1. **PO** updates WHITEBOARD with blocker
2. **BOSS** (human) can intervene via `>>> [message]`
3. Team discusses solution via PO hub
4. Resume normal workflow when unblocked

**If agent loses context after auto-compact:**

1. SessionStart hook injects role + workflow
2. Agent reads WHITEBOARD for current state
3. Agent asks PO for current task if unclear

---

**Next:** Run `docs/tmux/gh-search-team/setup-team.sh` to initialize the team in tmux.
