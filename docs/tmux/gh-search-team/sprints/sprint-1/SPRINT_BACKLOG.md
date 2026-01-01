# Sprint 1 Backlog - gh-search

**Sprint Goal:** Establish clean project structure and validate README fetching at medium scale

**Sprint Duration:** 2026-01-01 (Sprint 1)

**Team:**
- **PO (Product Owner):** Manages sprint, communicates with BOSS
- **TL (Tech Lead):** Creates specs, reviews code
- **DEV (Developer):** Implements features using TDD

---

## Sprint Items

### P0-1: Clean Up Project Structure ✓ COMPLETED

**Assigned to:** Tech Lead
**Priority:** P0 (Highest)
**Estimated Effort:** 1-2 hours
**Status:** ✅ COMPLETED

**Deliverables:**
- [x] Created `experiments/` folder for trial/learning code
- [x] Moved `test_connections.py` from `scripts/` to `experiments/`
- [x] Updated README.md with detailed folder structure and TDD requirements
- [x] Updated .gitignore for experiments/ outputs
- [x] Created sprint-1 folder structure with specs/
- [x] Created SPRINT_BACKLOG.md (this file)

**Specification:** `specs/clean-up-project-structure.md`

---

### P0-2: Fetch 100 READMEs (Progressive Validation)

**Assigned to:** Developer
**Priority:** P0 (Highest)
**Estimated Effort:** 30 minutes
**Status:** 🔜 READY FOR DEV

**Description:**
Scale README fetching from 10 to 100 repos to validate quality and costs at medium scale.

**Progressive Approach:**
1. ✅ Phase 1: 10 READMEs (test) → 8 successful (80%)
2. 🔄 Phase 2: 100 READMEs (validation) ← CURRENT
3. ⏭️ Phase 3: 1,000 READMEs (if 100 successful)
4. ⏭️ Phase 4: 55,000 READMEs (if 1K successful)

**Requirements:**
- Run `fetch_readmes.py --limit 100`
- Monitor success rate (should be ~80%)
- Review quality of fetched READMEs
- Calculate cost/time estimates for full 55K
- Report results to PO

**Acceptance Criteria:**
- [ ] 100 READMEs attempted
- [ ] Success rate >75%
- [ ] README content validated (not truncated/corrupted)
- [ ] Time and cost per repo calculated
- [ ] Estimate for 55K repos provided
- [ ] Results documented in sprint folder

**Specification:** TBD (Tech Lead will create)

---

## Sprint Summary

**Total Items:** 2
**Completed:** 1
**In Progress:** 0
**Ready for DEV:** 1

**Sprint Health:** 🟢 On track

---

## Definition of Done (Sprint-Wide)

For each sprint item to be considered complete:
- [ ] All acceptance criteria met
- [ ] Tests written first (TDD) for code items
- [ ] All tests passing
- [ ] Code quality checks pass (black, ruff, mypy)
- [ ] Tech Lead reviewed and approved
- [ ] PO approved
- [ ] Documentation updated
- [ ] Committed to Git with clear messages
- [ ] WHITEBOARD updated

---

**Last Updated:** 2026-01-01 by Tech Lead
