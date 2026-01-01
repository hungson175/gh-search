# Product Backlog - gh-search MCP Server

**Product Owner:** Manages and prioritizes this backlog
**Project:** GitHub Project Search MCP Server

---

## Sprint 0: Foundation & Progressive Development Setup

### P0-1: Clean Up Project Structure ⚡ HIGH PRIORITY

**Status:** Ready for Sprint
**Assigned to:** Tech Lead
**Estimated Effort:** 1-2 hours
**Sprint:** sprint-0

**Description:**
Review and reorganize project structure to follow best practices:

**Current Issues:**
- Mix of experimental/trial code and production scripts
- Unclear separation between runnable scripts and learning experiments
- Need clear distinction for TDD requirements

**Requirements:**
1. **Create `experiments/` folder** for trial/learning code
   - Move `test_connections.py` here (it was exploratory)
   - Move any other one-off exploration scripts
   - **NO TESTS REQUIRED** for experiments folder

2. **Keep `scripts/` for production-ready utilities**
   - `fetch_readmes.py` stays here (production script)
   - Future: `generate_embeddings.py`, deployment scripts
   - These MAY have tests if complex logic

3. **Ensure `src/` follows TDD**
   - All code in `src/gh_search/` MUST have tests
   - Test-Driven Development: Write tests first, then implementation
   - 100% coverage goal for production code

4. **Sprint folder structure** (Tech Lead note)
   - Each sprint gets its own folder: `docs/tmux/gh-search-team/sprints/sprint-N/`
   - Sprint-specific docs go in sprint folder
   - Template in `sprints/templates/`

**Acceptance Criteria:**
- [ ] `experiments/` folder created with exploratory code
- [ ] `scripts/` contains only production-ready utilities
- [ ] `src/` structure is clean and follows best practices
- [ ] README.md updated with folder structure explanation
- [ ] .gitignore updated if needed
- [ ] Sprint folder structure documented

**Tech Lead Tasks:**
1. Review current file organization
2. Create folder structure proposal
3. Move files to appropriate locations
4. Update documentation
5. Commit changes with clear message

---

### P0-2: Fetch 100 READMEs (Progressive Validation) ⚡ HIGH PRIORITY

**Status:** Ready for Sprint
**Assigned to:** Dev
**Estimated Effort:** 30 minutes
**Sprint:** sprint-0
**Depends on:** Test with 10 first (already done: 8/10 success)

**Description:**
**PROGRESSIVE DEVELOPMENT PRINCIPLE:**
We already tested with 10 READMEs (80% success rate). Now scale to 100 to validate at medium scale before attempting 55K.

**Progressive Approach:**
1. ✅ **Already done:** 10 READMEs (test) → 8 successful
2. **Current task:** 100 READMEs (validation)
3. **Next:** 1,000 READMEs (if 100 successful)
4. **Final:** 55,000 READMEs (if 1K successful)

**Requirements:**
- Run `fetch_readmes.py --limit 100`
- Monitor success rate (should be ~80%)
- Review quality of fetched READMEs
- Calculate cost/time estimates for full 55K
- Report results to PO

**Acceptance Criteria:**
- [ ] 100 READMEs attempted
- [ ] Success rate >75% (similar to test batch)
- [ ] README content looks valid (not truncated/corrupted)
- [ ] Time and cost per repo calculated
- [ ] Estimate for 55K repos provided
- [ ] Results documented in sprint folder

**Success Metrics:**
- Expected: ~80 successful, ~20 no README
- Time: ~2-3 minutes total
- Ready to scale to 1,000 if successful

---

### P0-3: Build Resumable Background Service for 55K READMEs ⚡ HIGH PRIORITY

**Status:** Blocked (wait for P0-2 completion)
**Assigned to:** Dev
**Estimated Effort:** 2-3 hours
**Sprint:** TBD (next sprint after P0-2 validates)
**Depends on:** P0-2 (100 README validation)

**Description:**
**CRITICAL REQUIREMENT: MUST BE RESUMABLE**

Build a background service to fetch all 55,000+ READMEs using GitHub API with the following requirements:

**Requirements:**

1. **Resumable Operation**
   - Can be interrupted at any time (Ctrl+C)
   - Resumes from exactly where it left off
   - Tracks progress in database or file
   - No duplicate fetches

2. **Background Execution**
   - Runs via `nohup` or similar
   - Logs progress to file
   - Can check status without interrupting
   - Shows ETA for completion

3. **Progressive Batching**
   - Fetch in batches of 100-1000
   - Commit progress after each batch
   - Log success/failure rates per batch
   - Alert if success rate drops <70%

4. **Rate Limiting**
   - Respect GitHub API limits
   - Don't exceed 5,000 req/hour (authenticated)
   - Add delays between requests (1-2 sec)
   - Exponential backoff on errors

5. **Monitoring & Reporting**
   - Progress bar or percentage
   - Current batch stats
   - Overall stats (fetched, failed, remaining)
   - ETA calculation
   - Log file with timestamps

**Implementation Approach (Tech Lead will spec):**
```bash
# Start background fetch
nohup python scripts/fetch_readmes_background.py --limit 55000 > logs/readme_fetch.log 2>&1 &

# Check status (without interrupting)
tail -f logs/readme_fetch.log

# Or dedicated status check
python scripts/check_fetch_status.py
```

**Acceptance Criteria:**
- [ ] Service runs in background (nohup)
- [ ] Resumable after interruption
- [ ] Progress tracked persistently
- [ ] Batch-based with commits
- [ ] Rate limiting implemented
- [ ] Status monitoring available
- [ ] Logs all activities
- [ ] TDD: Tests for resume logic
- [ ] Successfully fetches 55K+ READMEs

**Success Criteria:**
- Can interrupt at any time and resume
- Completes 55K READMEs in ~25-30 hours
- Success rate >75%
- No duplicate fetches on resume

---

## Backlog Items (Not Yet Prioritized)

### Phase -1: Complete README Fetching

**Status:** In Progress (8/55,015 fetched)
**Dependencies:** None
**Estimated Effort:** ~25 hours runtime

**Tasks:**
- [ ] Fetch 1,000 READMEs (validation batch)
- [ ] Analyze success rate and quality
- [ ] Fetch remaining ~54K READMEs
- [ ] Validate >80% completion rate

### Phase 0: Database Setup

**Status:** Blocked by Phase -1
**Dependencies:** READMEs must be >80% fetched
**Estimated Effort:** 2-3 hours

**Tasks:**
- [ ] Install pgvector extension in PostgreSQL
- [ ] Add new columns (synthesized_description, embedding, etc.)
- [ ] Create vector index (ivfflat)
- [ ] Create full-text search index
- [ ] Test index performance

### Phase 1: Generate Embeddings (Progressive)

**Status:** Blocked by Phase 0
**Estimated Effort:** Variable by batch size

**Batch 1: 10 repos**
- [ ] Generate LLM summaries using Grok
- [ ] Create embedding text
- [ ] Generate Voyage AI embeddings
- [ ] Validate quality
- [ ] Calculate costs

**Batch 2: 1,000 repos**
- [ ] Scale up if Batch 1 successful
- [ ] Monitor costs closely

**Full Dataset: 55K repos**
- [ ] Only after successful small batches

### Phase 2: Implement Search Engine

**Status:** Blocked by Phase 1
**Estimated Effort:** 1 week

**Tasks:**
- [ ] Implement vector search query
- [ ] Implement BM25 full-text search
- [ ] Implement hybrid ranking (70/30)
- [ ] Test search quality
- [ ] Optimize query performance

### Phase 3: Build MCP Server

**Status:** Blocked by Phase 2
**Estimated Effort:** 1-2 weeks

**Tools to Implement:**
- [ ] `search_projects` tool
- [ ] `fetch_project` tool
- [ ] `batch_fetch_projects` tool
- [ ] Error handling
- [ ] Logging and monitoring
- [ ] MCP Inspector testing

### Phase 4: Testing & Documentation

**Status:** Blocked by Phase 3

**Tasks:**
- [ ] Integration tests
- [ ] Performance tests
- [ ] User documentation
- [ ] API documentation
- [ ] Deployment guide

---

## Notes

**Progressive Development Philosophy:**
- Always start small (10 items)
- Validate quality and costs
- Scale gradually (1,000 → full)
- Never jump to full dataset without validation

**Definition of Done:**
- Code follows TDD (tests written first)
- All tests passing
- Code reviewed by Tech Lead
- PO approved
- Documented
- Committed to Git with clear message
