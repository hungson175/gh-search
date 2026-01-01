# Technical Specification: Resumable Background Service for 55K READMEs

**Sprint:** sprint-2
**Priority:** P0 (Highest)
**Estimated Effort:** 2-3 hours development + ~27 hours runtime
**Created by:** Tech Lead
**Date:** 2026-01-01

---

## Overview

Enhance the existing `fetch_readmes.py` script to run as a long-running background service that fetches all remaining ~54,900 READMEs (105 already fetched). The service must be resumable, rate-limited, and provide comprehensive progress monitoring for the estimated 27-hour runtime.

**Key Insight:** The existing script is ALREADY resumable - it queries `WHERE readme_text IS NULL` and handles interrupts gracefully. We need to enhance it for long-running background execution.

## Requirements Analysis

### Functional Requirements
- Fetch all ~54,900 remaining READMEs from GitHub
- Resume from interruption without duplicate fetches
- Run in background (detached from terminal)
- Respect GitHub API rate limits (5,000 req/hour authenticated)
- Provide real-time progress monitoring
- Log all activities with timestamps
- Calculate and display ETA

### Non-Functional Requirements
- **Runtime:** ~27 hours for 55K repos (based on Phase 2 metrics)
- **Availability:** Can check status without interrupting process
- **Reliability:** No data loss on interruption
- **Rate Limiting:** Stay under 5,000 API calls/hour
- **Resumability:** Can restart anytime from last checkpoint

## Progressive Development Plan ⚡ CRITICAL

**NEVER jump straight to 55K repos. Validate at each scale:**

### Phase 1: Validate Resume with 1,000 Repos (~30 min)
- **Goal:** Test resume logic works correctly
- **Scope:**
  - Run for 500 repos
  - Interrupt (Ctrl+C)
  - Resume and complete to 1,000
  - Verify no duplicates
  - Validate progress tracking
- **Success:** Resume picks up exactly where stopped, no duplicates
- **Time:** ~30 minutes total

### Phase 2: Large-Scale Test with 10,000 Repos (~5 hours)
- **Goal:** Validate background execution and monitoring at scale
- **Scope:**
  - Run via nohup in background
  - Monitor via status checks
  - Test interruption after 2 hours
  - Resume and complete
  - Verify rate limiting works
- **Success:** Completes 10K repos, stays under rate limits, monitoring works
- **Dependencies:** Phase 1 validates resume logic

### Phase 3: Full Production Run (~27 hours)
- **Goal:** Complete all remaining READMEs
- **Scope:**
  - Launch background service for all ~54,900 remaining
  - Monitor periodically (15min → 30min → hourly)
  - Let run to completion
  - Final validation
- **Success:** All READMEs fetched, >75% success rate maintained
- **Dependencies:** Phase 2 validates large-scale execution

**CRITICAL:** Each phase must complete successfully before proceeding to next.

## Technical Approach

### Current Script Analysis

**File:** `scripts/fetch_readmes.py`

**Already has:**
- ✅ Resumability: Queries `WHERE readme_text IS NULL`
- ✅ Interrupt handling: `KeyboardInterrupt` → saves progress
- ✅ Database checkpointing: Updates after each repo
- ✅ Rate limiting: 1-second delay between requests
- ✅ Progress stats: Shows counts and estimates
- ✅ Error handling: Graceful failures

**Needs enhancement:**
- ❌ Background execution wrapper
- ❌ Comprehensive logging to file
- ❌ Status check without interrupting
- ❌ Progress monitoring at intervals
- ❌ Rate limit calculation (ensure <5,000/hour)
- ❌ Batch-based progress reporting

### Architecture

```
┌─────────────────────────────────────────┐
│  Background Service (nohup)             │
│  scripts/fetch_readmes.py               │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Main Loop                         │ │
│  │ • Query WHERE readme_text IS NULL │ │
│  │ • Fetch README from GitHub        │ │
│  │ • Update database                 │ │
│  │ • Log progress                    │ │
│  │ • Rate limit (1.0s delay)         │ │
│  └───────────────────────────────────┘ │
│                                         │
│  Logs to: logs/readme_fetch.log         │
└─────────────────────────────────────────┘
           ↓
    PostgreSQL Database
    (Progress Checkpoint)
           ↓
┌─────────────────────────────────────────┐
│  Status Monitor (separate script)       │
│  scripts/check_fetch_status.py          │
│  • Query database stats                │
│  • Read log file                       │
│  • Calculate ETA                       │
│  • Display progress                    │
└─────────────────────────────────────────┘
```

### Technology Choices
- **Language:** Python 3.11
- **Database:** PostgreSQL (existing, tracks progress)
- **Background:** nohup + & (simple, reliable)
- **Logging:** Python logging module to file
- **Monitoring:** Separate status check script
- **Rationale:** Keep it simple - existing script already works well

### File Structure

**New/Modified Files:**
```
scripts/
  ├── fetch_readmes.py              # ENHANCED (add logging, monitoring)
  ├── fetch_readmes_background.sh   # NEW (wrapper script for nohup)
  └── check_fetch_status.py         # NEW (status monitoring)

tests/
  ├── test_fetch_readmes.py         # NEW (TDD for resume logic)
  └── test_status_monitor.py        # NEW (status script tests)

logs/
  └── readme_fetch.log               # NEW (runtime logs)
```

## API Design (if applicable)

N/A - This is a batch processing script, not an API.

## Test-Driven Development (TDD) Plan

**CRITICAL: Test resumability logic**

### Test Suite

**Unit Tests:** `tests/test_fetch_readmes.py`

1. **test_resume_from_interruption**
   - **Input:** Database with 50 repos, 10 already fetched
   - **Expected:** Query returns only 40 unfetched repos
   - **Edge cases:** All fetched, none fetched, mixed states

2. **test_no_duplicate_fetches**
   - **Input:** Run fetch twice on same set
   - **Expected:** Second run fetches 0 (all already done)
   - **Validates:** `WHERE readme_text IS NULL` works correctly

3. **test_progress_tracking**
   - **Input:** Fetch 10 repos, check stats
   - **Expected:** Stats show correct counts (fetched, failed, pending)

4. **test_rate_limiting**
   - **Input:** Fetch 10 repos with 1.0s delay
   - **Expected:** Takes ≥9 seconds (9 delays between 10 repos)
   - **Validates:** Rate limiting enforced

5. **test_interrupt_handling**
   - **Input:** Simulate KeyboardInterrupt during fetch
   - **Expected:** Progress saved, can resume
   - **Validates:** Graceful shutdown

**Integration Tests:** `tests/test_status_monitor.py`

1. **test_status_check_without_interruption**
   - **Input:** Running fetch process
   - **Expected:** Status script reads stats without affecting process

2. **test_eta_calculation**
   - **Input:** Known fetch rate, known pending count
   - **Expected:** Accurate ETA calculation

### TDD Workflow for DEV

```
For each feature:
1. Write test FIRST (red)
2. Run test - should FAIL
3. Write minimal code to pass (green)
4. Refactor if needed
5. Commit: "test: add test for X" then "feat: implement X"
```

## Implementation Steps

**For DEV to follow:**

### Phase 1: Validate Resume (1,000 repos, ~30 min)

**Step 1: Create Test for Resume Logic**

1. **Create test file:**
   ```bash
   vim tests/test_fetch_readmes.py
   ```

2. **Write resume test:**
   ```python
   def test_resume_from_interruption():
       """Test that fetch resumes from where it stopped."""
       # Setup: Create test database state
       # 100 total repos, 10 already fetched (readme_text NOT NULL)

       # Act: Query for repos without READMEs
       remaining = get_repos_without_readmes(100)

       # Assert: Should get only 90 repos
       assert len(remaining) == 90
       # Assert: None of the 10 already-fetched repos are included
   ```

3. **Run test (should FAIL):**
   ```bash
   pytest tests/test_fetch_readmes.py::test_resume_from_interruption -v
   ```

4. **Commit test:**
   ```bash
   git add tests/test_fetch_readmes.py
   git commit -m "test: add resume from interruption test"
   ```

**Step 2: Run First 500 Repos**

5. **Check current status:**
   ```bash
   python scripts/fetch_readmes.py --limit 0  # Just show stats
   ```

6. **Run 500 repos:**
   ```bash
   python scripts/fetch_readmes.py --limit 500 --delay 1.0
   ```

7. **Record stats:**
   - Note how many succeeded
   - Note how many failed
   - Record time taken

**Step 3: Interrupt and Resume Test**

8. **Run another 500, but interrupt after ~250:**
   ```bash
   python scripts/fetch_readmes.py --limit 500 --delay 1.0
   # After ~5 minutes (250 * 1.0s delay + fetch time), press Ctrl+C
   ```

9. **Verify progress saved:**
   ```bash
   # Check database stats - should show ~750 total processed
   python scripts/fetch_readmes.py --limit 0
   ```

10. **Resume to complete 1,000:**
    ```bash
    # This should fetch the remaining ~250 to reach 1,000 total
    python scripts/fetch_readmes.py --limit 250 --delay 1.0
    ```

11. **Verify no duplicates:**
    ```bash
    # Run with limit 0 (fetch 0 new) - should skip all already-fetched
    python scripts/fetch_readmes.py --limit 100 --delay 1.0
    # Should immediately say "No repos to process!"
    ```

12. **Commit Phase 1 results:**
    ```bash
    git add .
    git commit -m "test: validate resume logic with 1,000 repos

    - Fetched 500 repos
    - Interrupted and resumed
    - Completed to 1,000 total
    - Verified no duplicates
    - Resume logic works correctly

    Ready for Phase 2 (background execution)."
    ```

### Phase 2: Large-Scale Test (10,000 repos, ~5 hours)

**Step 13: Create Background Wrapper**

13. **Create wrapper script:**
    ```bash
    vim scripts/fetch_readmes_background.sh
    ```

    ```bash
    #!/bin/bash
    # Background README fetching with logging

    LIMIT=${1:-55000}
    LOG_FILE="logs/readme_fetch.log"

    echo "Starting README fetch in background..."
    echo "Limit: $LIMIT repos"
    echo "Log: $LOG_FILE"
    echo "PID will be written to logs/readme_fetch.pid"

    nohup python scripts/fetch_readmes.py --limit "$LIMIT" --delay 1.0 \
        > "$LOG_FILE" 2>&1 &

    PID=$!
    echo $PID > logs/readme_fetch.pid

    echo "Background process started: PID $PID"
    echo "Monitor with: tail -f $LOG_FILE"
    echo "Check status: python scripts/check_fetch_status.py"
    echo "Stop with: kill $PID"
    ```

14. **Make executable:**
    ```bash
    chmod +x scripts/fetch_readmes_background.sh
    ```

**Step 14: Create Status Monitor**

15. **Create status check script:**
    ```bash
    vim scripts/check_fetch_status.py
    ```

    ```python
    #!/usr/bin/env python3
    """Check status of background README fetching."""

    import psycopg2
    from datetime import datetime
    import os

    DB_CONFIG = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'postgres',
        'database': 'github_projects'
    }

    def get_stats():
        """Get current stats."""
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) as total,
                COUNT(*) FILTER (WHERE readme_text IS NOT NULL AND readme_text != '') as fetched,
                COUNT(*) FILTER (WHERE readme_text = '') as failed,
                COUNT(*) FILTER (WHERE readme_text IS NULL) as pending
            FROM github_repositories
        """)

        total, fetched, failed, pending = cursor.fetchone()
        cursor.close()
        conn.close()

        return {
            'total': total,
            'fetched': fetched,
            'failed': failed,
            'pending': pending
        }

    def check_process():
        """Check if background process is running."""
        pid_file = "logs/readme_fetch.pid"
        if not os.path.exists(pid_file):
            return None

        with open(pid_file) as f:
            pid = int(f.read().strip())

        try:
            os.kill(pid, 0)  # Check if process exists
            return pid
        except OSError:
            return None

    def estimate_completion(stats, avg_rate=1.74):
        """Estimate time to completion."""
        remaining = stats['pending']
        if remaining == 0:
            return "Complete!"

        # avg_rate is seconds per repo (from Phase 2 results)
        seconds = remaining * avg_rate
        hours = seconds / 3600

        if hours < 1:
            return f"{seconds/60:.1f} minutes"
        else:
            return f"{hours:.1f} hours"

    if __name__ == '__main__':
        print("=" * 80)
        print(f"README Fetch Status - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print()

        # Check if process running
        pid = check_process()
        if pid:
            print(f"✅ Background process RUNNING (PID: {pid})")
        else:
            print(f"⚠️  Background process NOT running")
        print()

        # Get stats
        stats = get_stats()

        print("Database Status:")
        print(f"  Total repos:    {stats['total']:,}")
        print(f"  With README:    {stats['fetched']:,} ({stats['fetched']/stats['total']*100:.1f}%)")
        print(f"  No README:      {stats['failed']:,}")
        print(f"  Pending:        {stats['pending']:,}")
        print()

        # ETA
        if stats['pending'] > 0:
            eta = estimate_completion(stats)
            print(f"Estimated time to completion: {eta}")
            print()

        # Recent log
        log_file = "logs/readme_fetch.log"
        if os.path.exists(log_file):
            print("Recent log (last 10 lines):")
            print("-" * 80)
            os.system(f"tail -n 10 {log_file}")
    ```

16. **Make executable:**
    ```bash
    chmod +x scripts/check_fetch_status.py
    ```

**Step 15: Run 10K Background Test**

17. **Start background fetch for 10,000:**
    ```bash
    ./scripts/fetch_readmes_background.sh 10000
    ```

18. **Monitor immediately (first 15 minutes):**
    ```bash
    # Check every 5 minutes
    watch -n 300 python scripts/check_fetch_status.py
    ```

19. **After 2 hours (~4,000 repos), test interruption:**
    ```bash
    # Get PID
    cat logs/readme_fetch.pid

    # Kill process
    kill <PID>

    # Check stats
    python scripts/check_fetch_status.py
    # Should show ~4,000 fetched, ~6,000 pending
    ```

20. **Resume to complete 10K:**
    ```bash
    ./scripts/fetch_readmes_background.sh 6000
    ```

21. **Monitor to completion:**
    ```bash
    # Check every 30 minutes
    python scripts/check_fetch_status.py
    ```

22. **Validate results:**
    ```bash
    # Final stats
    python scripts/check_fetch_status.py

    # Should show:
    # - ~10,000 total processed (fetched + failed)
    # - Success rate >75%
    # - ~44,900 pending for Phase 3
    ```

23. **Commit Phase 2:**
    ```bash
    git add scripts/fetch_readmes_background.sh scripts/check_fetch_status.py
    git commit -m "feat: add background execution and status monitoring

    - Created fetch_readmes_background.sh wrapper for nohup
    - Created check_fetch_status.py for non-intrusive monitoring
    - Tested with 10K repos over 5 hours
    - Validated interrupt/resume works in background
    - Rate limiting maintained (<5K/hour)

    Phase 2 complete. Ready for Phase 3 (full 55K)."
    ```

### Phase 3: Full Production Run (~27 hours)

**Step 16: Launch Full Run**

24. **Final pre-flight check:**
    ```bash
    python scripts/check_fetch_status.py
    # Note current stats - should have ~44,900 pending
    ```

25. **Launch full background run:**
    ```bash
    ./scripts/fetch_readmes_background.sh 55000

    # Record start time
    date > logs/start_time.txt
    ```

26. **Initial monitoring (first hour):**
    ```bash
    # Check every 15 minutes
    watch -n 900 python scripts/check_fetch_status.py
    ```

27. **Regular monitoring schedule:**
    - **Hours 0-2:** Check every 15 minutes
    - **Hours 2-8:** Check every 30 minutes
    - **Hours 8-27:** Check every hour

    ```bash
    # Example check command
    python scripts/check_fetch_status.py

    # Save snapshots
    python scripts/check_fetch_status.py >> logs/progress_snapshots.txt
    echo "---" >> logs/progress_snapshots.txt
    ```

28. **Wait for completion (~27 hours)**

29. **Final validation:**
    ```bash
    # Check final stats
    python scripts/check_fetch_status.py

    # Verify counts
    psql -h localhost -p 5432 -U postgres -d github_projects -c "
    SELECT
        COUNT(*) as total,
        COUNT(*) FILTER (WHERE readme_text IS NOT NULL AND readme_text != '') as fetched,
        COUNT(*) FILTER (WHERE readme_text = '') as failed,
        COUNT(*) FILTER (WHERE readme_text IS NULL) as pending
    FROM github_repositories;
    "
    ```

30. **Create completion report:**
    ```bash
    # Create report file
    vim docs/tmux/gh-search-team/sprints/sprint-2/results/full-readme-fetch-report.md
    ```

31. **Commit completion:**
    ```bash
    git add docs/tmux/gh-search-team/sprints/sprint-2/results/
    git commit -m "docs: complete 55K README fetch

    - Total processed: ~55,000 repos
    - Success rate: X%
    - Runtime: ~27 hours
    - No data loss on interruptions
    - Rate limiting maintained

    Phase 3 complete. All READMEs fetched."
    ```

## Acceptance Criteria

**Definition of Done:**
- [x] Background execution script created and tested
- [x] Status monitoring script created and works non-intrusively
- [x] Phase 1: Resume logic validated with 1,000 repos
- [x] Phase 2: Background execution validated with 10,000 repos
- [x] Phase 3: Full 55K fetch completed
- [x] Success rate >75% maintained
- [x] Rate limiting <5,000 requests/hour verified
- [x] No duplicate fetches on resume
- [x] Tests written for resume logic (TDD)
- [x] All tests passing
- [x] Comprehensive logging implemented
- [x] Progress monitoring validated
- [x] Completion report created
- [x] Committed to git with clear messages
- [x] Tech Lead reviewed and approved

## Expected Results

### Phase 1 (1,000 repos)
- **Duration:** ~30 minutes
- **Success rate:** ~97% (based on Phase 2 results)
- **Outcome:** Resume logic confirmed working

### Phase 2 (10,000 repos)
- **Duration:** ~5 hours
- **Success rate:** >75%
- **Outcome:** Background execution and monitoring validated

### Phase 3 (55,000 repos)
- **Duration:** ~27 hours
- **Success rate:** >75%
- **Total fetched:** ~41,000-45,000 (75-82% of 55K)
- **No README:** ~10,000-14,000 (18-25% - legitimate failures)
- **Outcome:** Complete README dataset ready for embedding generation

## Rate Limiting Strategy

### GitHub API Limits
- **Authenticated:** 5,000 requests/hour
- **Our target:** Stay under 4,500/hour (safety margin)

### Current Approach
- **Delay:** 1.0 second between requests
- **Effective rate:** 3,600 requests/hour (60/min * 60 min)
- **Status:** ✅ Well under limit (80% of allowed)

### Monitoring
```python
# Track hourly rate
requests_last_hour = 0
hour_start = time.time()

# After each request
requests_last_hour += 1
if time.time() - hour_start > 3600:
    print(f"Requests last hour: {requests_last_hour}")
    if requests_last_hour > 4500:
        print("⚠️ WARNING: Approaching rate limit!")
    requests_last_hour = 0
    hour_start = time.time()
```

## Troubleshooting

### Issue: Process dies unexpectedly
**Solution:**
1. Check `logs/readme_fetch.log` for errors
2. Check database connection
3. Verify PostgreSQL is running: `pg_isready`
4. Resume with same command - will pick up where stopped

### Issue: Success rate drops below 75%
**Solution:**
1. Check GitHub API status
2. Verify authentication token valid
3. Check network connectivity
4. Review error patterns in logs
5. May need to pause and resume later

### Issue: Can't check status
**Solution:**
```bash
# Direct database query
psql -h localhost -p 5432 -U postgres -d github_projects -c "
SELECT COUNT(*) FILTER (WHERE readme_text IS NOT NULL) as done,
       COUNT(*) FILTER (WHERE readme_text IS NULL) as pending
FROM github_repositories;
"
```

### Issue: Process running but logs not updating
**Solution:**
1. Check process still alive: `ps aux | grep fetch_readmes`
2. Check disk space: `df -h`
3. Check log file permissions
4. May need to restart

## Technical Decisions

### Decision 1: Database as checkpoint vs separate state file
**Chosen:** Database
**Rationale:** Database already tracks state (`readme_text IS NULL`), no separate state file needed. Single source of truth.

### Decision 2: nohup vs systemd service
**Chosen:** nohup
**Rationale:** Simpler for one-off 27-hour job. Systemd would be overkill. nohup + shell script is sufficient.

### Decision 3: Real-time logging vs batch updates
**Chosen:** Real-time logging
**Rationale:** Need to monitor progress without interrupting. File logging allows `tail -f` monitoring.

### Decision 4: 1.0s delay vs dynamic rate limiting
**Chosen:** 1.0s delay (static)
**Rationale:** Simple, reliable, well under limits (3,600/hour vs 5,000 allowed). No need for complexity.

### Decision 5: Progressive validation (1K → 10K → 55K) vs direct to 55K
**Chosen:** Progressive
**Rationale:** Critical principle - validate resume logic and monitoring before 27-hour commitment. Catch issues early.

---

**Tech Lead Signature:** TL
**Date:** 2026-01-01

---

## Notes for DEV

**Critical Success Factors:**
1. **Test resume logic thoroughly** in Phase 1 before background run
2. **Monitor actively** in first 2 hours of each phase
3. **Don't skip phases** - each validates the next
4. **Document everything** - this is a 27-hour process
5. **Be patient** - long-running processes are normal for this scale

**When in doubt:**
- Check `python scripts/check_fetch_status.py`
- Review `logs/readme_fetch.log`
- Ask TL via PO if anything looks wrong

**Remember:** The existing script is already 90% there. We're just adding background execution, better monitoring, and validating it works for 27 hours straight.
