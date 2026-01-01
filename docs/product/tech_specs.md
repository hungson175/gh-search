# GitHub Project Search (gh-search) - Technical Specifications

**Version:** 1.0
**Date:** 2026-01-01
**Status:** In Development

---

## 1. System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Claude Code                        │
│              (Requests via MCP Protocol)                │
└────────────────────────┬────────────────────────────────┘
                         │
                    MCP Tool Calls
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │ Search   │  │ Similar  │  │ Filter   │
    │ Projects │  │ Projects │  │ Projects │
    └────┬─────┘  └────┬─────┘  └────┬─────┘
         │             │             │
         └─────────────┼─────────────┘
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
   ┌─────────────────┐       ┌─────────────────┐
   │   Qdrant Vector │       │   PostgreSQL    │
   │      DB         │       │   Repository    │
   │   (Embeddings)  │       │   Database      │
   └─────────────────┘       └─────────────────┘
        55K repos                55K repos
      (embeddings)              (metadata)
```

### Components

1. **MCP Server** - FastMCP/Python server exposing tools
2. **Vector Database (Qdrant)** - Semantic search via embeddings
3. **PostgreSQL** - Repository metadata storage
4. **Embedding Model** - Voyage AI (3.5-lite, 1024 dims)
5. **Search Engine** - Hybrid vector + metadata search

---

## 2. Technology Stack

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| **Language** | Python | 3.10+ | FastMCP, data science libs |
| **MCP Framework** | FastMCP | Latest | Lightweight, async MCP |
| **Vector DB** | Qdrant | Latest | Fast semantic search, local |
| **SQL DB** | PostgreSQL | 14+ | Reliable, advanced queries |
| **Embedding Model** | Voyage AI 3.5-lite | 2024 | Good performance, 1024 dims |
| **HTTP Server** | FastAPI | 0.100+ | Async, automatic OpenAPI |
| **Async Runtime** | asyncio | Native | Built-in Python |

---

## 3. Database Schema

### PostgreSQL: github_repositories

```sql
CREATE TABLE github_repositories (
    repo_name VARCHAR(255) PRIMARY KEY,    -- owner/repo
    owner VARCHAR(255) NOT NULL,
    stars INTEGER NOT NULL,
    clone_url VARCHAR(500),
    language VARCHAR(50),
    description TEXT,
    readme_text TEXT,                      -- For future README search
    topics TEXT[],                         -- Array of topic strings
    forks INTEGER,
    watchers INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_stars ON github_repositories(stars DESC);
CREATE INDEX idx_language ON github_repositories(language);
CREATE INDEX idx_owner ON github_repositories(owner);
CREATE INDEX idx_updated_at ON github_repositories(updated_at DESC);
```

### Qdrant: github-projects Collection

**Collection Configuration:**
```json
{
  "name": "github-projects",
  "vector_size": 1024,
  "distance": "cosine",
  "payload_schema": {
    "repo_name": "text",
    "owner": "text",
    "stars": "integer",
    "language": "text",
    "topics": "text_array",
    "description": "text",
    "clone_url": "text"
  }
}
```

**Payload Structure per Vector:**
```json
{
  "repo_name": "torvalds/linux",
  "owner": "torvalds",
  "stars": 175000,
  "language": "C",
  "topics": ["kernel", "operating-system", "linux"],
  "description": "Linux kernel source tree",
  "clone_url": "https://github.com/torvalds/linux"
}
```

---

## 4. Search Implementation

### 4.1 Semantic Search Pipeline

```
User Query
    │
    ├─→ [Embedding] → Generate 1024-dim vector via Voyage AI
    │
    ├─→ [Qdrant Search] → Top-50 similar vectors (cosine similarity)
    │
    ├─→ [Apply Filters] → Language, min_stars, topics, recency
    │
    ├─→ [Rank Results] → Score = (similarity * 0.7) + (stars_normalized * 0.3)
    │
    └─→ [Return Top-20] → With metadata from PostgreSQL
```

### 4.2 Search Algorithm

**Algorithm: Hybrid Vector + Metadata Search**

```python
def search_projects(query: str, language: str = None, min_stars: int = 1000,
                   topics: List[str] = None, limit: int = 10):

    # Step 1: Embed query
    query_embedding = voyage_client.embed(query)  # 1024 dims

    # Step 2: Vector search in Qdrant
    vector_results = qdrant_client.search(
        collection_name="github-projects",
        query_vector=query_embedding,
        limit=50,  # Get more candidates for filtering
        score_threshold=0.7  # Min cosine similarity
    )

    # Step 3: Apply metadata filters
    filtered_results = []
    for result in vector_results:
        payload = result.payload

        # Check language filter
        if language and payload.get("language") != language:
            continue

        # Check minimum stars
        if payload.get("stars", 0) < min_stars:
            continue

        # Check topics filter
        if topics:
            repo_topics = set(payload.get("topics", []))
            if not any(t in repo_topics for t in topics):
                continue

        filtered_results.append(result)

    # Step 4: Re-rank by combined score
    scored_results = []
    for result in filtered_results:
        vector_score = result.score  # 0-1 cosine similarity
        stars_score = min(payload["stars"] / 100000, 1.0)  # Normalize
        combined_score = (vector_score * 0.7) + (stars_score * 0.3)
        scored_results.append((result, combined_score))

    # Step 5: Sort and return
    ranked = sorted(scored_results, key=lambda x: x[1], reverse=True)
    return [r[0] for r in ranked[:limit]]
```

### 4.3 Ranking Formula

```
Final Score = (Vector_Similarity * 0.7) + (Stars_Normalized * 0.3)

Where:
- Vector_Similarity: Cosine similarity (0-1) from Qdrant
- Stars_Normalized: min(actual_stars / 100000, 1.0)
- Weight 0.7/0.3: Prioritize relevance over popularity
```

**Rationale:**
- 70% relevance: Find projects that match user's intent
- 30% popularity: Among similar projects, prefer well-tested ones
- Normalizing stars at 100K: Projects with 100K+ stars don't dominate

---

## 5. MCP Server Implementation

### 5.1 Tools Exposed

```python
@mcp.tool()
async def search_projects(
    query: str,
    language: Optional[str] = None,
    min_stars: int = 1000,
    topics: Optional[List[str]] = None,
    max_age_months: Optional[int] = None,
    limit: int = 10
) -> ProjectSearchResult:
    """
    Search GitHub projects semantically.

    Args:
        query: Natural language search query
        language: Filter by language (Python, JavaScript, etc.)
        min_stars: Minimum star count (default 1000)
        topics: Filter by topics (e.g., ["game", "phaser"])
        max_age_months: Only return projects updated in last N months
        limit: Number of results (1-20, default 10)

    Returns:
        List of matching GitHub projects with metadata
    """
    # Implementation...
```

```python
@mcp.tool()
async def similar_projects(
    repo_name: str,
    language: Optional[str] = None,
    min_stars: int = 1000,
    limit: int = 10
) -> ProjectSearchResult:
    """
    Find projects similar to a given repository.

    Args:
        repo_name: Repository (owner/name format)
        language: Filter by language
        min_stars: Minimum star count
        limit: Number of results

    Returns:
        Similar projects
    """
    # Implementation...
```

```python
@mcp.tool()
async def filter_by_language(
    language: str,
    min_stars: int = 1000,
    limit: int = 20,
    sort_by: str = "stars"
) -> ProjectSearchResult:
    """
    Browse top projects by language.

    Args:
        language: Programming language
        min_stars: Minimum star count
        limit: Number of results
        sort_by: "stars", "recent", "trending"

    Returns:
        Top projects in specified language
    """
    # Implementation...
```

### 5.2 Response Format

```python
@dataclass
class Project:
    repo_name: str
    owner: str
    stars: int
    clone_url: str
    language: str
    description: str
    topics: List[str]
    forks: int
    last_updated: str
    relevance_score: Optional[float] = None

@dataclass
class ProjectSearchResult:
    results: List[Project]
    total_results: int
    query_executed_in_ms: float
    filters_applied: Dict[str, Any]
```

---

## 6. Data Pipeline

### 6.1 Initial Indexing

```
Kaggle Dataset (4.2M repos)
    │
    ├─→ Filter: 1000+ stars → 55,421 repos
    │
    ├─→ PostgreSQL Import → github_repositories table
    │
    ├─→ Generate Embeddings:
    │   For each repo description:
    │   - Create 2-3 sentence summary
    │   - Generate 1024-dim embedding via Voyage AI
    │   - Cost: ~$0.02 per 1M tokens
    │
    └─→ Index in Qdrant → github-projects collection
```

### 6.2 Update Strategy

**Weekly Update Cycle:**
- Query GitHub API for changed repositories
- Update star counts, last_updated, forked status
- Re-embed if description changed significantly
- Update Qdrant index

**Cost Estimate:**
- GitHub API: ~100 requests (free tier)
- Voyage AI embeddings: ~$5/week (only changed repos)
- Infrastructure: ~$50/month (Qdrant + PostgreSQL)

---

## 7. Performance Specifications

### 7.1 Latency Targets

| Operation | Target | Current |
|-----------|--------|---------|
| Search embedding | < 500ms | 400ms (Voyage API) |
| Vector search (Qdrant) | < 100ms | 50-80ms |
| Metadata filtering | < 100ms | 20-50ms |
| Total latency | < 2s | 500-700ms |

### 7.2 Throughput

- **Concurrent queries:** 100+ simultaneous searches
- **QPS (queries per second):** 50+ sustained
- **Database connections:** 10 PostgreSQL connections

### 7.3 Storage

```
PostgreSQL: ~100 MB (metadata for 55K repos)
Qdrant: ~200 MB (1024-dim vectors × 55K repos)
Total: ~300 MB
```

---

## 8. API Specification

### 8.1 Tool Definitions (MCP)

```python
# Tool 1: search_projects
{
    "name": "search_projects",
    "description": "Semantic search for GitHub projects",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Natural language search query"
            },
            "language": {
                "type": "string",
                "description": "Filter by language"
            },
            "min_stars": {
                "type": "integer",
                "description": "Minimum star count",
                "default": 1000
            },
            "topics": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Filter by topics"
            },
            "limit": {
                "type": "integer",
                "description": "Results to return (1-20)",
                "default": 10
            }
        },
        "required": ["query"]
    }
}

# Tool 2: similar_projects
# Tool 3: filter_by_language
# Tool 4: get_trending
```

---

## 9. Deployment Architecture

### 9.1 Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy server code
COPY gh_search/ ./gh_search/

# Expose MCP server port
EXPOSE 3000

# Start MCP server
CMD ["python", "-m", "gh_search.server"]
```

### 9.2 Environment Configuration

```bash
# .env
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=github-projects

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=github_projects
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

VOYAGE_API_KEY=pa-...
EMBEDDING_MODEL=voyage-3.5-lite
EMBEDDING_DIMENSION=1024

LOG_LEVEL=INFO
MAX_RESULTS=20
DEFAULT_MIN_STARS=1000
```

### 9.3 Monitoring

```
- Query latency (p50, p95, p99)
- Vector search latency
- Database connection pool usage
- Embedding API calls and costs
- Error rates by tool
- Qdrant index health
```

---

## 10. Security Considerations

### 10.1 Data Security

- ✅ No sensitive data stored (public GitHub repos only)
- ✅ Encryption in transit (HTTPS)
- ✅ Database credentials in environment variables
- ✅ API keys not exposed in responses

### 10.2 Access Control

- ✅ Public API (no authentication required for MVP)
- ✅ Rate limiting: 1000 queries/hour per IP
- ✅ Query timeout: 5 seconds max
- ✅ Result size limits: max 20 results

### 10.3 Privacy

- ✅ Query logging: Not stored
- ✅ User tracking: Disabled
- ✅ Data retention: 0 days (queries not persisted)

---

## 11. Fault Tolerance

### 11.1 Failure Modes & Mitigation

| Failure Mode | Impact | Mitigation |
|--------------|--------|-----------|
| Qdrant down | Semantic search fails | Fallback to keyword search in PostgreSQL |
| PostgreSQL down | Metadata unavailable | Return cached results from Qdrant payload |
| Voyage API down | Cannot embed new queries | Serve cached results for common queries |
| Network latency | Search slow | Implement query caching (30 min TTL) |

### 11.2 Caching Strategy

```python
# In-memory cache for frequent queries
QUERY_CACHE = {}  # {query_hash: (results, timestamp)}

def search_with_cache(query, filters):
    cache_key = hash((query, frozenset(filters.items())))

    if cache_key in QUERY_CACHE:
        results, cached_at = QUERY_CACHE[cache_key]
        if time.time() - cached_at < 1800:  # 30 min TTL
            return results

    results = perform_search(query, filters)
    QUERY_CACHE[cache_key] = (results, time.time())
    return results
```

---

## 12. Scalability Plan

### Current (Phase 1): 55K repos, local

```
Qdrant: Local or Docker (~300MB)
PostgreSQL: Local (~100MB)
MCP Server: Single process, Python
QPS: 50-100
```

### Phase 2: 500K repos, regional

```
Qdrant: Managed cloud service (Qdrant Cloud)
PostgreSQL: Cloud PostgreSQL (AWS RDS)
MCP Server: Containerized, multiple instances
Load Balancer: Distribute queries
QPS: 1000+
```

### Phase 3: 5M+ repos, global

```
Architecture: Distributed Qdrant cluster
Replication: Multi-region
Database: Sharded PostgreSQL
CDN: Cache popular results globally
```

---

## 13. Development Timeline

### Sprint 1 (Week 1-2): Core MCP Server
- [ ] Qdrant setup and indexing
- [ ] PostgreSQL schema and population
- [ ] Basic search_projects tool
- [ ] FastMCP server scaffolding
- [ ] Unit tests

### Sprint 2 (Week 3-4): Enhanced Search
- [ ] similar_projects tool
- [ ] filter_by_language tool
- [ ] Advanced ranking algorithm
- [ ] Integration tests
- [ ] Performance optimization

### Sprint 3 (Week 5-6): Polish & Deploy
- [ ] Error handling and logging
- [ ] Documentation and examples
- [ ] Docker deployment
- [ ] Claude Code integration
- [ ] Monitoring and alerting

---

## 14. Testing Strategy

### 14.1 Unit Tests
```python
test_embedding_generation()
test_vector_search_accuracy()
test_metadata_filtering()
test_ranking_algorithm()
test_response_serialization()
```

### 14.2 Integration Tests
```python
test_search_projects_e2e()
test_similar_projects_e2e()
test_filter_by_language_e2e()
test_concurrent_searches()
```

### 14.3 Performance Tests
```python
test_latency_p95_under_2s()
test_throughput_100_concurrent()
test_memory_usage_under_500mb()
```

---

## 15. Glossary

| Term | Definition |
|------|-----------|
| **MCP** | Model Context Protocol - standard for LLM tool integration |
| **Qdrant** | Vector database for semantic search |
| **Embedding** | 1024-dimensional vector representation of text |
| **Cosine Similarity** | Measure of how similar two vectors are (0-1) |
| **Payload** | Metadata stored alongside vectors in Qdrant |
| **FastMCP** | Lightweight Python framework for MCP servers |

---

**End of Document**
