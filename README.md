# GitHub Project Search (gh-search)

Semantic search MCP server for discovering GitHub repositories using vector embeddings and hybrid search.

## Overview

**gh-search** is a Model Context Protocol (MCP) server that enables semantic search across 55,000+ high-quality GitHub repositories (1000+ stars). It helps developers find reference implementations, libraries, and starter projects when building new applications.

### Key Features

- 🔍 **Semantic Search** - Natural language queries like "tower defense game in JavaScript"
- 🎯 **Hybrid Ranking** - Combines vector similarity (70%) + BM25 keyword matching (30%)
- 🗄️ **PostgreSQL-Only** - Uses pgvector for embeddings, no separate vector database
- 🤖 **LLM-Enhanced** - Grok generates 2-3 sentence summaries from READMEs
- 📊 **Rich Metadata** - Technologies, stars, forks, topics, descriptions

## Architecture

```
User Query
    ↓
MCP Server (FastMCP)
    ↓
PostgreSQL with pgvector
    ├─→ Vector Search (Voyage AI embeddings, 1024-dim)
    ├─→ BM25 Full-Text Search
    └─→ Hybrid Ranking
    ↓
Search Results (Preview)
    ↓
Fetch Tool (Full Details)
```

## Tech Stack

- **Language:** Python 3.11+
- **MCP Framework:** FastMCP
- **Database:** PostgreSQL 17+ with pgvector extension
- **Embeddings:** Voyage AI 3.5-lite (1024 dimensions)
- **LLM:** Grok (xAI) for README summarization
- **Search:** Vector similarity + BM25 hybrid approach

## Project Status

### Phase -1: README Fetching ✅ IN PROGRESS
- **Status:** 8/55,015 READMEs fetched (0.01%)
- **Test batch:** 8 successful, 2 no README (80% success rate)
- **Next:** Scale to 1,000 repos, then complete all 55K

### Phase 0: Database Setup
- Install pgvector extension
- Add embedding columns
- Create indexes

### Phase 1: Generate Embeddings
- LLM-synthesized descriptions (Grok)
- Vector embeddings (Voyage AI)
- Progressive approach: 10 → 1,000 → full dataset

### Phase 2+: Build MCP Server
- Implement search tools
- Deploy and test

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL 17+ with pgvector extension
- GitHub authentication (for README fetching)
- Voyage AI API key
- xAI (Grok) API key

### Setup

```bash
# Clone repository
git clone <repo-url>
cd gh-search

# Create virtual environment
uv venv --python 3.11 .venv
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]"

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Environment Variables

Create `.env` file:

```bash
# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=github_projects
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Qdrant (legacy, will be removed)
QDRANT_URL=http://localhost:6333

# Voyage AI
VOYAGE_API_KEY=pa-your-key-here
EMBEDDING_MODEL=voyage-3.5-lite
EMBEDDING_DIMENSION=1024

# xAI (Grok)
XAI_API_KEY=xai-your-key-here

# Server
LOG_LEVEL=INFO
MAX_RESULTS=20
DEFAULT_MIN_STARS=1000
```

## Usage

### Fetch READMEs (Phase -1)

```bash
# Test with 10 repos
python scripts/fetch_readmes.py --limit 10

# Fetch 1,000 repos
python scripts/fetch_readmes.py --limit 1000

# Fetch all remaining (background)
nohup python scripts/fetch_readmes.py --limit 55000 > readme_fetch.log 2>&1 &
```

### Generate Embeddings (Phase 1)

```bash
# Coming soon - progressive embedding generation
python scripts/generate_embeddings.py --limit 10
```

### Run MCP Server (Phase 2+)

```bash
# Coming soon
python -m gh_search.server
```

## MCP Tools

### `search_projects`
Semantic search for GitHub projects with filters.

**Input:**
- `query`: Natural language search query
- `language`: Filter by programming language (optional)
- `min_stars`: Minimum star count (default: 1000)
- `limit`: Number of results (default: 10, max: 50)

**Output:**
- List of project previews with descriptions, metadata, relevance scores

### `fetch_project`
Get full details for a specific repository.

**Input:**
- `repo_name`: Repository in `owner/name` format

**Output:**
- Complete project information including README preview

### `batch_fetch_projects`
Fetch multiple projects at once (efficient bulk operation).

**Input:**
- `repo_names`: List of repository names (max: 20)

**Output:**
- List of complete project details

## Database Schema

```sql
-- Main table with vector support
CREATE TABLE github_repositories (
    repo_name VARCHAR(255) PRIMARY KEY,
    owner VARCHAR(255) NOT NULL,
    stars INTEGER NOT NULL,
    clone_url VARCHAR(500),
    language VARCHAR(50),
    description TEXT,
    readme_text TEXT,
    synthesized_description TEXT,  -- LLM-generated summary
    embedding_text TEXT,            -- Text used for embedding
    embedding vector(1024),         -- Voyage AI embedding
    topics TEXT[],
    forks INTEGER,
    watchers INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    embedding_generated_at TIMESTAMP,
    description_synthesized_at TIMESTAMP
);

-- Indexes
CREATE INDEX idx_embedding ON github_repositories
USING ivfflat (embedding vector_cosine_ops);

CREATE INDEX idx_fts ON github_repositories
USING GIN (to_tsvector('english', synthesized_description));
```

## Development

### Folder Structure

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

#### TDD Requirements by Folder

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

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gh_search --cov-report=html

# Run specific test file
pytest tests/test_search.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

## Documentation

- **[First Specs for MCP](docs/First_Specs_for_MCP.md)** - Complete implementation plan
- **[Phase -1: Fetch READMEs](docs/Phase_Minus_1_Fetch_READMEs.md)** - README fetching strategy
- **[Database Quality Report](docs/tmp/database_quality_report_v2.md)** - Data analysis

## Progressive Development Strategy

**Critical:** We use a progressive approach to control costs and quality:

1. **Test with 10 repos** - Validate approach
2. **Scale to 1,000 repos** - Check quality and costs
3. **Complete all 55K repos** - Only after validation

This prevents expensive mistakes with LLM API calls and ensures quality.

## Cost Estimates

### README Fetching (Phase -1)
- **Cost:** FREE (GitHub API)
- **Time:** ~11 hours for 55K repos (with authentication)

### LLM Summarization (Phase 1)
- **Model:** Grok (xAI)
- **Estimated:** ~$5-20 for 55K summaries (TBD, testing with 10 first)

### Embeddings (Phase 1)
- **Model:** Voyage AI 3.5-lite
- **Cost:** ~$0.02 per 1M tokens
- **Estimated:** ~$5-10 for 55K embeddings

**Total estimated cost:** ~$10-30 for complete dataset

## Contributing

This is currently a development project. Contributions welcome after initial release.

## License

MIT License - see LICENSE file for details

## Acknowledgments

- PostgreSQL + pgvector for unified vector + SQL database
- Voyage AI for high-quality embeddings
- xAI (Grok) for fast LLM summarization
- FastMCP for MCP server framework

---

**Status:** Phase -1 (README Fetching) - 0.01% complete
**Next Milestone:** Complete README fetching, proceed to Phase 0 (Database Setup)
