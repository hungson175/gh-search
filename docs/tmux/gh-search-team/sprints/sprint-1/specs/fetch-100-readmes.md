# Technical Specification: Fetch 100 READMEs (Progressive Validation)

**Sprint:** sprint-1
**Priority:** P0 (Highest)
**Estimated Effort:** 30 minutes
**Created by:** Tech Lead
**Date:** 2026-01-01

---

## Overview

Run `fetch_readmes.py` script to fetch 100 READMEs as the second phase of progressive development. This validates the approach at medium scale before proceeding to 1,000 and eventually 55,000 repos.

**Progressive Approach:**
1. ✅ **Phase 1 (DONE):** 10 READMEs → 8 successful (80%)
2. **Phase 2 (THIS TASK):** 100 READMEs → Validate quality & costs
3. **Phase 3 (FUTURE):** 1,000 READMEs → If Phase 2 successful
4. **Phase 4 (FUTURE):** 55,000 READMEs → Full production run

## Requirements Analysis

### Functional Requirements
- Execute existing `scripts/fetch_readmes.py` with `--limit 100`
- Monitor execution (time, success rate, errors)
- Validate README quality (not truncated/corrupted)
- Document results in sprint folder
- Calculate estimates for full 55K dataset

### Non-Functional Requirements
- **Performance:** Complete within 5-10 minutes
- **Quality:** Success rate >75% (similar to test batch)
- **Cost:** FREE (GitHub API)
- **Validation:** Manual spot-check of 5-10 READMEs

## Progressive Development Plan ⚡ CRITICAL

**This task IS progressive development in action!**

We're NOT jumping straight to 55K repos. We're validating at medium scale first.

### Phase 1: Run Script (5 min)
- **Goal:** Execute fetch for 100 repos
- **Scope:**
  - Run `python scripts/fetch_readmes.py --limit 100`
  - Monitor console output
  - Record start/end time
- **Success:** Script completes without crashes
- **Time:** 5-10 minutes execution

### Phase 2: Validate Results (10 min)
- **Goal:** Check quality of fetched READMEs
- **Scope:**
  - Count successful vs failed fetches
  - Spot-check 5-10 READMEs for quality
  - Verify data in database
  - Look for truncation/corruption
- **Success:** >75 READMEs fetched successfully with good quality
- **Dependencies:** Phase 1 complete

### Phase 3: Calculate Estimates (10 min)
- **Goal:** Extrapolate costs and time for full dataset
- **Scope:**
  - Calculate time per repo
  - Estimate total time for 55K repos
  - Document success rate
  - Identify any issues/patterns
  - Write results report
- **Success:** Clear estimates documented, ready to proceed to 1K
- **Dependencies:** Phase 2 validates quality

## Technical Approach

### Existing Script

**File:** `scripts/fetch_readmes.py`

**What it does:**
- Fetches README content from GitHub repos
- Uses GitHub API (authenticated)
- Tries multiple README locations (README.md, readme.md, README, etc.)
- Tries both 'main' and 'master' branches
- Stores results in PostgreSQL database
- Logs successes and failures

**Command:**
```bash
python scripts/fetch_readmes.py --limit 100
```

### No Code Changes Needed

This task does NOT require writing new code. The script already exists and was tested with 10 repos. We're just running it with a higher limit.

## API Design (if applicable)

N/A - Using existing script, no new code.

## Test-Driven Development (TDD) Plan

**CRITICAL: This is NOT a coding task.**

This is an operational task (running existing script), NOT implementation. Therefore, traditional TDD doesn't apply.

### Verification Steps (Instead of Tests)

**Phase 1 Verification:**
1. Script starts without errors
2. GitHub API authentication works
3. Database connection succeeds
4. Progress is logged to console

**Phase 2 Verification:**
1. Count rows in database: `SELECT COUNT(*) FROM github_repositories WHERE readme_text IS NOT NULL`
2. Check for NULL/empty READMEs
3. Spot-check 5 specific repos for README quality
4. Verify README length distribution (no all-truncated)

**Phase 3 Verification:**
1. Calculate success rate: `(successful / 100) * 100%`
2. Calculate avg time per repo: `total_time / 100`
3. Estimate for 55K: `avg_time * 55000 / 3600` hours

## Implementation Steps

**For DEV to follow:**

### Phase 1: Run Script (5 min)

1. **Activate virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

2. **Verify environment variables:**
   ```bash
   # Check .env has GitHub token
   grep GITHUB_TOKEN .env
   # Should show: GITHUB_TOKEN=ghp_...
   ```

3. **Start README fetch:**
   ```bash
   # Note start time
   date

   # Run script
   python scripts/fetch_readmes.py --limit 100

   # Note end time when finished
   date
   ```

4. **Observe output:**
   - Watch for success/failure messages
   - Note any error patterns
   - Record total time taken

### Phase 2: Validate Results (10 min)

5. **Check database results:**
   ```bash
   # Connect to PostgreSQL (adjust port if needed)
   psql -h localhost -p 5432 -U postgres -d github_projects
   ```

   ```sql
   -- Count total repos
   SELECT COUNT(*) FROM github_repositories;

   -- Count with READMEs
   SELECT COUNT(*) FROM github_repositories WHERE readme_text IS NOT NULL;

   -- Count without READMEs (expected: ~20-25)
   SELECT COUNT(*) FROM github_repositories WHERE readme_text IS NULL;

   -- Check README lengths
   SELECT
       MIN(LENGTH(readme_text)) as min_length,
       AVG(LENGTH(readme_text)) as avg_length,
       MAX(LENGTH(readme_text)) as max_length
   FROM github_repositories
   WHERE readme_text IS NOT NULL;

   -- Sample 5 repos
   SELECT repo_name, owner, LENGTH(readme_text) as readme_len
   FROM github_repositories
   WHERE readme_text IS NOT NULL
   LIMIT 5;
   ```

6. **Spot-check README quality:**
   ```sql
   -- View actual README for one repo
   SELECT repo_name, LEFT(readme_text, 200) as preview
   FROM github_repositories
   WHERE readme_text IS NOT NULL
   LIMIT 1;
   ```

   Verify:
   - README has markdown formatting
   - Content looks legitimate (not error messages)
   - No obvious truncation

7. **Document findings:**
   - Total fetched: X
   - Successful: Y (with README)
   - Failed: Z (no README)
   - Success rate: Y/X * 100%
   - README quality: Good/Fair/Poor

### Phase 3: Calculate Estimates (10 min)

8. **Calculate time metrics:**
   ```bash
   # From Phase 1 start/end times
   # Example: Started 21:45, Ended 21:52 = 7 minutes

   # Time per repo
   # Example: 7 minutes / 100 repos = 0.07 min/repo = 4.2 sec/repo

   # Estimate for 1,000 repos
   # Example: 0.07 * 1000 = 70 minutes

   # Estimate for 55,000 repos
   # Example: 0.07 * 55000 = 3,850 minutes = 64 hours
   ```

9. **Create results report:**
   Create file: `docs/tmux/gh-search-team/sprints/sprint-1/results/fetch-100-readmes-report.md`

   Template:
   ```markdown
   # README Fetch Results - 100 Repos

   **Date:** 2026-01-01
   **Sprint:** sprint-1
   **Task:** P0-2 Fetch 100 READMEs

   ## Execution Summary

   - **Start Time:** HH:MM
   - **End Time:** HH:MM
   - **Total Duration:** X minutes
   - **Repos Attempted:** 100
   - **Successful:** Y
   - **Failed:** Z
   - **Success Rate:** Y%

   ## Quality Assessment

   ### README Lengths
   - Minimum: X chars
   - Average: Y chars
   - Maximum: Z chars

   ### Spot Check (5 samples)
   1. repo1: ✓ Good
   2. repo2: ✓ Good
   3. repo3: ✓ Good
   4. repo4: ⚠ Issue (describe)
   5. repo5: ✓ Good

   ## Performance Metrics

   - **Time per repo:** X seconds
   - **Estimated for 1,000 repos:** Y minutes
   - **Estimated for 55,000 repos:** Z hours

   ## Issues Found

   - None / List any issues

   ## Recommendation

   ✅ Proceed to Phase 3 (1,000 repos)
   OR
   ⚠ Address issues before scaling

   ## Next Steps

   1. If success rate >75%: Create spec for 1K fetch
   2. If issues found: Debug and re-run
   3. Document lessons learned
   ```

10. **Commit results:**
    ```bash
    # Create results directory
    mkdir -p docs/tmux/gh-search-team/sprints/sprint-1/results

    # Add report
    git add docs/tmux/gh-search-team/sprints/sprint-1/results/fetch-100-readmes-report.md

    git commit -m "docs: add fetch-100-readmes results report

    - Fetched 100 READMEs (Y successful, Z failed)
    - Success rate: Y%
    - Avg time: X sec/repo
    - Estimate for 55K: Z hours
    - Quality validated: Good/Fair/Poor

    Ready to proceed to 1K repos if >75% success."
    ```

11. **Report to PO:**
    Send completion message via tm-send PO with:
    - Success/failure counts
    - Success rate percentage
    - Quality assessment
    - Time estimates
    - Recommendation (proceed or debug)

## Acceptance Criteria

**Definition of Done:**
- [x] Script executed with `--limit 100`
- [x] 100 repos attempted
- [x] Success rate >75% achieved
- [x] README quality validated (spot-check 5-10)
- [x] Database counts verified
- [x] Time per repo calculated
- [x] Estimate for 55K repos documented
- [x] Results report created in sprint folder
- [x] Results committed to git
- [x] Reported to PO with recommendation

## Expected Results

**Based on Phase 1 (10 repos = 80% success):**

### Best Case
- **Successful:** 80-85 / 100
- **Failed:** 15-20 / 100 (repos without README)
- **Success Rate:** 80-85%
- **Time:** 5-7 minutes total
- **Quality:** Good (no truncation, valid markdown)
- **Recommendation:** ✅ Proceed to 1,000 repos

### Acceptable Case
- **Successful:** 75-80 / 100
- **Failed:** 20-25 / 100
- **Success Rate:** 75-80%
- **Time:** 7-10 minutes total
- **Quality:** Fair (minor issues)
- **Recommendation:** ✅ Proceed with caution

### Concerning Case
- **Successful:** <75 / 100
- **Failed:** >25 / 100
- **Success Rate:** <75%
- **Time:** >10 minutes
- **Quality:** Poor (truncation, errors)
- **Recommendation:** ⚠ Debug before scaling

## Troubleshooting

### Issue: Script crashes
**Solution:** Check logs, verify environment variables, ensure database is running

### Issue: Low success rate (<75%)
**Solution:**
1. Check GitHub API rate limits
2. Verify authentication token
3. Review error messages in console
4. Check if specific repos causing issues

### Issue: README quality poor
**Solution:**
1. Check for truncation (all READMEs same length)
2. Verify character encoding
3. Check for API errors in README text
4. Review fetch logic in script

### Issue: Database errors
**Solution:**
1. Verify PostgreSQL is running: `pg_isready`
2. Check connection: `psql -h localhost -p 5432 -U postgres -l`
3. Verify github_projects database exists
4. Check table schema

## Technical Decisions

### Decision 1: Why 100 repos (not 1,000)?
**Rationale:** Progressive development principle. We validated with 10, now 100, then 1,000. This catches issues early before expensive operations.

### Decision 2: Manual spot-check vs automated validation
**Rationale:** For Phase 2, manual checking is sufficient and faster. Automated validation can wait until we're confident in the approach.

### Decision 3: No code changes
**Rationale:** The script worked for 10 repos. Before modifying it, validate it works at 100. Don't optimize prematurely.

---

**Tech Lead Signature:** TL
**Date:** 2026-01-01

---

## Notes for DEV

- This is NOT a coding task - you're running an existing script
- Focus on observation and documentation
- Take your time with validation - quality > speed
- If success rate is low, DON'T proceed to 1K - report to PO first
- The goal is to VALIDATE, not just complete
- Document everything you observe
- When in doubt, ask TL via PO

**Remember:** Progressive development means we learn at each scale before proceeding. Don't skip validation steps!
