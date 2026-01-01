# gh-search 3-Person Scrum Team

**Team Type:** Progressive Development Scrum Team (Simplified)
**Project:** GitHub Project Search MCP Server
**Roles:** PO (Product Owner), TL (Tech Lead), DEV (Developer)

---

## Quick Start

### Start the Team

```bash
# Run the setup script
./docs/tmux/gh-search-team/setup-team.sh

# Attach to session
tmux attach -t gh-search-team
```

### First Sprint

The **PRODUCT_BACKLOG.md** has P0 tasks ready:

1. **P0-1:** Clean Up Project Structure (TL)
2. **P0-2:** Fetch 100 READMEs (DEV) - Progressive validation
3. **P0-3:** Build Resumable Background Service (DEV) - For 55K READMEs

---

## Team Structure

```
   BOSS (Human User - YOU)
        ↓
       PO (Product Owner) - Pane 0
        ↓
       TL (Tech Lead) - Pane 1
        ↓
      DEV (Developer) - Pane 2
```

**All communication flows through PO** (hub pattern)

---

## Core Principles

### 1. Progressive Development ⚡

**ALWAYS scale gradually:**
- **10 → 100 → 1,000 → 55,000**
- Never jump to full scale
- Validate quality and costs at each step
- Each phase works end-to-end

**Example:**
```
❌ BAD:  Fetch 55,000 READMEs at once
✓ GOOD:  10 (test) → 100 (validate) → 1K (scale) → 55K (production)
```

### 2. Test-Driven Development (TDD)

**DEV MUST write tests first:**
1. RED: Write failing test
2. GREEN: Write code to pass
3. REFACTOR: Improve quality
4. COMMIT: Save progress

**Git history proves TDD:**
```
✓ test: add test for X
✓ feat: implement X
```

### 3. Sprint-Based Workflow

**10-Step Sprint Process:**
1. BOSS → PO (requirements)
2. PO → TL (sprint assignment)
3. TL creates spec
4. PO → DEV (sprint with spec)
5. DEV implements (TDD + progressive)
6-7. Clarifications (via PO)
8. DEV reports completion
9. PO → TL (review request)
10. TL reviews, PO approves

**BOSS intervenes only AFTER step 10** - team self-coordinates during sprint.

### 4. Git as Truth

**Commits show real progress:**
- Frequent small commits
- Progressive development visible
- TDD pattern in history
- Clear commit messages

### 5. Resumable Operations

**For long-running tasks (55K fetches):**
- Can interrupt anytime (Ctrl+C)
- Resume from where stopped
- No duplicate work
- Progress tracked in DB

---

## Workflow Details

See **[workflow.md](workflow.md)** for complete workflow documentation.

### PO Responsibilities
- Manage PRODUCT_BACKLOG.md
- Route all team communication
- Approve final deliverables
- Maintain WHITEBOARD.md
- Verify work independently

### TL Responsibilities
- Create technical specifications
- Guard progressive development
- Review all code
- Enforce TDD compliance
- Make technical decisions

### DEV Responsibilities
- Implement using TDD
- Follow TL specifications
- Build progressively
- Commit frequently
- Report to PO

---

## File Structure

```
docs/tmux/gh-search-team/
├── README.md                    # This file
├── workflow.md                  # Complete workflow docs
├── PRODUCT_BACKLOG.md           # All work items (PO manages)
├── WHITEBOARD.md                # Real-time status
├── setup-team.sh                # Team setup script
├── sprints/                     # Sprint-specific folders
│   ├── sprint-0/                # Current sprint
│   │   ├── SPRINT_BACKLOG.md    # Sprint items
│   │   ├── specs/               # TL specifications
│   │   └── lessons.md           # Sprint lessons learned
│   └── templates/               # Sprint templates
├── prompts/                     # Role prompts
│   ├── PO_PROMPT.md             # Product Owner
│   ├── TL_PROMPT.md             # Tech Lead
│   └── DEV_PROMPT.md            # Developer
└── po/                          # PO workspace
    └── (PO management files)
```

---

## Communication Patterns

### BOSS to PO

**BOSS uses `>>>` prefix:**
```
>>> start sprint 1 with P0 project structure
```

PO receives:
```
BOSS [14:30]: start sprint 1 with P0 project structure
```

### Agent Communication

**Use `tm-send` (installed globally):**
```bash
# DEV to PO
tm-send PO "DEV [15:00]: Sprint complete. Ready for review."

# TL to PO
tm-send PO "TL [10:30]: Spec ready. See docs/tmux/gh-search-team/sprints/sprint-0/specs/..."

# PO to TL
tm-send TL "PO [11:00]: Sprint assigned. See PRODUCT_BACKLOG P0-1."
```

### Two-Enter Rule

**CRITICAL:** All tmux messages need TWO separate commands:
```bash
tm-send TL "PO [11:00]: Message here"
# Second enter sent automatically by tm-send
```

---

## Sprint Management

### Sprint Folder Structure

Each sprint gets its own folder:
```
sprints/
├── sprint-0/
│   ├── SPRINT_BACKLOG.md        # This sprint's items
│   ├── specs/                   # TL specs for this sprint
│   │   ├── project-structure.md
│   │   └── fetch-100.md
│   └── lessons.md               # What we learned
├── sprint-1/
│   └── ...
```

**Sprint-specific docs stay in sprint folder** - easier to find later.

### Definition of Done

**Sprint item is complete when:**
- [ ] All tests written first (TDD)
- [ ] All tests passing
- [ ] Code coverage >90%
- [ ] Code quality passing (black, ruff)
- [ ] Progressive development verified (git log)
- [ ] TL reviewed and approved
- [ ] PO approved
- [ ] Documentation updated
- [ ] Committed with clear messages
- [ ] WHITEBOARD updated

---

## Tools & Commands

### Starting Team
```bash
# Setup and start
./docs/tmux/gh-search-team/setup-team.sh

# Attach
tmux attach -t gh-search-team

# Detach (without killing)
Ctrl+b d
```

### Communication
```bash
# Send message to agent
tm-send [ROLE] "Sender [HH:mm]: message"

# List roles in session
tm-send --list
```

### Quality Checks
```bash
# Run tests
pytest

# Check coverage
pytest --cov=src/gh_search --cov-report=term

# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/
```

### Git
```bash
# View history
git log --oneline -10

# Check status
git status

# Progressive commits
git add tests/test_X.py
git commit -m "test: add test for X"
git add src/gh_search/X.py
git commit -m "feat: implement X"
```

---

## Session Resumption

**After tmux restart or auto-compact:**

1. **SessionStart hook** auto-injects:
   - workflow.md
   - Role-specific prompt

2. **Agents check:**
   - WHITEBOARD.md (current status)
   - Sprint folder (current sprint docs)
   - git log (recent progress)

3. **PO coordinates:**
   - Updates WHITEBOARD
   - Verifies team understands tasks
   - Resumes workflow

---

## Progressive Development Examples

### Example 1: README Fetching

**Progressive Phases:**
```
Phase 1: 10 READMEs (test)
  ✓ Success rate: 80%
  ✓ Time: 16 seconds
  → Validated script works

Phase 2: 100 READMEs (validate)
  → Goal: Validate quality, calculate costs
  → Estimated: 2-3 minutes

Phase 3: 1,000 READMEs (scale test)
  → Goal: Test at scale, verify performance
  → Estimated: 30 minutes

Phase 4: 55,000 READMEs (production)
  → Requires: Resumable background service
  → Estimated: 25-30 hours
  → Must be interruptible
```

### Example 2: Search Engine

**Progressive Phases:**
```
Phase 1: Basic vector search
  → Single vector query
  → Returns top 10 results
  → Works end-to-end

Phase 2: Add BM25
  → Keyword search working
  → Separate from vector
  → Works end-to-end

Phase 3: Hybrid ranking
  → Combine vector + BM25
  → 70/30 weighting
  → Works end-to-end
```

---

## Troubleshooting

### Team Not Responding

1. Check WHITEBOARD.md
2. Check git log for recent activity
3. Use `>>>` to send message to PO
4. PO coordinates team

### Agent Lost Context

**SessionStart hook should auto-inject context**

If not:
1. Run `/init-role [ROLE]` manually
2. Check `.claude/hooks/session_start_team_docs.py` exists
3. Check `.claude/settings.json` configured

### Communication Not Working

1. Verify tm-send installed: `which tm-send`
2. Check in correct session: `tmux display-message -p '#S'`
3. Use two-enter rule
4. Check pane IDs match

---

## Success Metrics

**Team succeeds when:**
- ✓ Progressive development followed (10 → 100 → 1K → full)
- ✓ TDD verified in all src/ code (git history proof)
- ✓ All tests passing
- ✓ Code quality high
- ✓ Sprints complete successfully
- ✓ Git shows incremental progress
- ✓ WHITEBOARD always current
- ✓ Team self-coordinates efficiently

---

## Next Steps

1. **Review PRODUCT_BACKLOG.md** - See available work
2. **Start setup script** - Initialize team
3. **BOSS assigns P0-1** - First sprint (project structure)
4. **Team executes** - Self-coordinates through 10 steps
5. **Iterate** - Continue with progressive sprints

---

**Ready to start Sprint 0!**

Run: `./docs/tmux/gh-search-team/setup-team.sh`
