# Sprint 2 Backlog - gh-search

**Sprint Goal:** Build and run resumable background service to fetch all 55,000 READMEs with rate limiting and progress monitoring

**Sprint Duration:** 2026-01-01 (Sprint 2)

**Team:**
- **PO (Product Owner):** Manages sprint, communicates with BOSS
- **TL (Tech Lead):** Creates specs, reviews code
- **DEV (Developer):** Implements features using TDD

---

## Sprint Items

### P0-3: Build Resumable Background Service for 55K READMEs

**Assigned to:** Tech Lead (spec) → Developer (implementation)
**Priority:** P0 (Highest)
**Estimated Effort:** 2-3 hours dev + ~27 hours runtime
**Status:** 🔄 IN PROGRESS - TL creating spec

**Description:**
Build a resumable background service to fetch all ~54,900 remaining READMEs (105 already fetched in Sprint 1).

**BOSS Requirements:**
- Resumable operation (can interrupt and resume without duplicates)
- Background process (nohup or similar)
- Rate limit aware: GitHub API 5,000 req/hour (authenticated)
- Progress monitoring: Check every 15 min initially, then 30 min, then hourly
- Fetch all remaining READMEs (~54,900 repos)

**Technical Requirements:**

1. **Resumability**
   - Track progress in database or file
   - Can interrupt at any time (Ctrl+C)
   - Resumes from exactly where it left off
   - No duplicate fetches

2. **Rate Limiting**
   - GitHub API: 5,000 requests/hour (authenticated)
   - Calculate safe delay: 3600s / 5000 = 0.72s minimum
   - Recommended: 1.0-1.5s delay between requests
   - Exponential backoff on errors

3. **Background Execution**
   - Runs via nohup or systemd
   - Logs to file
   - Can check status without interrupting
   - Shows progress and ETA

4. **Progress Monitoring**
   - Initial checks: Every 15 minutes
   - Mid-run checks: Every 30 minutes
   - Late-run checks: Hourly
   - Reports: fetched count, success rate, ETA, errors

5. **Batch Processing**
   - Process in batches of 100-1000
   - Commit progress after each batch
   - Alert if success rate drops <70%

**Acceptance Criteria:**
- [ ] Spec created by Tech Lead
- [ ] TDD: Tests for resume logic written first
- [ ] Service runs in background (nohup)
- [ ] Resumable after interruption
- [ ] Progress tracked persistently
- [ ] Rate limiting implemented (stays under 5,000/hour)
- [ ] Status monitoring available
- [ ] Logs all activities with timestamps
- [ ] Successfully fetches ~54,900 remaining READMEs
- [ ] Success rate >75%
- [ ] No duplicate fetches on resume
- [ ] Tech Lead reviewed and approved
- [ ] PO approved
- [ ] All tests passing

**Specification:** TBD (Tech Lead creating now)

**Expected Results:**
- Duration: ~27 hours runtime
- Success rate: >75% (based on Sprint 1: 97%)
- Total READMEs: ~55,000 (105 existing + 54,900 new)
- Rate: ~2,000-2,500 repos/hour (with 1-1.5s delay)

---

## Sprint Summary

**Total Items:** 1
**Completed:** 0
**In Progress:** 1 (TL creating spec)

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
- [ ] Background service successfully running
- [ ] Progress monitoring confirmed working

---

**Last Updated:** 2026-01-01 21:57 by PO
