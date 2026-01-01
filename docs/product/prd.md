# GitHub Project Search (gh-search) - Product Requirements Document

**Version:** 1.0
**Date:** 2026-01-01
**Status:** In Development
**Owner:** Development Team

---

## 1. Executive Summary

The **GitHub Project Search (gh-search)** MCP server enables semantic search across 55,000+ high-quality GitHub repositories. It serves as a discovery tool for developers, architects, and builders to find reference implementations, component libraries, and starter projects when building new applications.

The server bridges the gap between "I need to build X technology" and "Here are 10 proven GitHub projects doing exactly that."

---

## 2. Problem Statement

### Current Challenges

**For Developers:**
- When starting a new project (game, finance app, data tool), developers must manually search GitHub
- Generic GitHub search returns irrelevant results or misses similar implementations
- No semantic understanding of project purpose - only keyword matching
- Hard to find components to adapt/customize for new projects

**For AI Assistants (Claude):**
- Cannot assist with "find similar projects" requests
- Limited ability to recommend reference implementations
- No structured database of high-quality, popular repositories

### Use Cases

1. **Game Developer:** "Find Tower Defense and Plants vs Zombies-like games in JavaScript"
   - Needs: Similar game mechanics, frameworks (Phaser, Godot), implementation examples

2. **Finance Engineer:** "Find Python libraries for US macroeconomic data analysis"
   - Needs: Data sources, APIs, analysis frameworks, examples

3. **Startup CTO:** "We're building a real-time chat app with React - show me similar architectures"
   - Needs: Reference implementations, tech stack examples, patterns

4. **ML Engineer:** "Find open-source transformer implementations in PyTorch"
   - Needs: Research implementations, code examples, papers

---

## 3. Solution Overview

### What is gh-search?

**gh-search** is an MCP server that provides semantic search over a curated database of 55,000+ high-quality GitHub repositories (1000+ stars, public, active).

**Key Capabilities:**

1. **Semantic Search** - Understand intent, not just keywords
   - Query: "Tower Defense game engine" → Finds Phaser/Godot game examples
   - Query: "REST API boilerplate with auth" → Finds Express/FastAPI templates

2. **Intelligent Filtering** - Multiple filter dimensions
   - Language: Python, JavaScript, Go, Rust, etc.
   - Stars: 1000+ (default), 5000+, 10000+
   - Topics: Game development, Finance, Web, ML, etc.
   - Active: Recently updated projects

3. **Semantic Similarity** - Find variants of projects
   - Query: "Bitcoin transaction analyzer"
   - Results: Similar crypto analysis tools, blockchain explorers, etc.

4. **Rich Context** - Get actionable information
   - Repository name, owner, GitHub URL
   - Stars, forks, last updated
   - Primary language, technologies used
   - Description and topics
   - Topics and related projects

---

## 4. Target Users

| User | Goal | Example Query |
|------|------|----------------|
| **Solo Developer** | Find working implementations to learn from | "Multiplayer WebSocket game in Node.js" |
| **Startup CTO** | Discover proven tech stacks | "Authentication system with OAuth2 and JWT" |
| **ML Researcher** | Find open-source implementations | "Vision transformer architecture PyTorch" |
| **Web Developer** | Locate component libraries | "Headless CMS with GraphQL API" |
| **Data Engineer** | Identify data pipeline frameworks | "ETL pipeline Airflow alternative" |
| **Game Dev** | Find engine examples and resources | "Procedural generation roguelike" |

---

## 5. Key Features

### 5.1 Semantic Project Search

**Feature:** Natural language search over GitHub repository database

**User Story:**
> As a developer starting a new project, I want to search for similar projects using natural language so I can find reference implementations and understand common approaches.

**Capability:**
- Accept free-form queries: "Find games like Plants vs Zombies in JavaScript"
- Return 10-20 most relevant repositories
- Rank by relevance + popularity (stars)
- Explain why each project matches

**Acceptance Criteria:**
- ✅ Handle multi-word semantic queries
- ✅ Return projects ranked by semantic relevance
- ✅ Include all project metadata in results
- ✅ Respond in <2 seconds for typical query

### 5.2 Smart Filtering

**Feature:** Refine results by language, stars, topics, update recency

**User Story:**
> As a developer, I want to filter results by programming language and minimum stars so I can focus on mature, proven implementations in my tech stack.

**Capability:**
- Filter by primary language (Python, JavaScript, TypeScript, Go, Rust, etc.)
- Filter by minimum stars (1000, 5000, 10000)
- Filter by topics (e.g., "game-development", "finance", "machine-learning")
- Filter by recency (last update < 1 month, 3 months, 6 months)

**Parameters:**
```
language: str (optional, e.g., "Python", "JavaScript")
min_stars: int (optional, default 1000)
topics: List[str] (optional, e.g., ["game", "phaser"])
max_age_months: int (optional, how recent)
```

### 5.3 Project Information

**Feature:** Rich, actionable project information

**User Story:**
> As a developer, I want complete information about a repository so I can quickly assess if it's relevant to my project needs.

**Returned Fields:**
- Repository name and owner
- GitHub URL (clone-able)
- Star count, forks, last updated
- Primary language
- Description
- Topics/tags
- Link to documentation (inferred from README)

**Format:**
```json
{
  "repo_name": "owner/project-name",
  "owner": "owner-username",
  "stars": 5432,
  "clone_url": "https://github.com/owner/project-name",
  "language": "Python",
  "description": "Full description from README",
  "topics": ["machine-learning", "nlp", "transformer"],
  "forks": 234,
  "last_updated": "2026-01-01T12:00:00Z"
}
```

### 5.4 Similar Projects

**Feature:** Find projects similar to a given repository

**User Story:**
> As a developer who found one good project, I want to find similar projects so I can compare approaches and choose the best fit.

**Capability:**
- Input: Repository name (e.g., "torvalds/linux")
- Output: Top 10 semantically similar repositories
- Same filtering options available

---

## 6. Non-Functional Requirements

| Requirement | Target | Rationale |
|-------------|--------|-----------|
| **Response Time** | < 2 seconds for search | Enable interactive use in Claude |
| **Query Limit** | 1000+ concurrent searches | Scale for multiple users |
| **Data Freshness** | Updated weekly | Balance freshness vs. complexity |
| **Accuracy** | > 80% relevance for top results | Useful recommendations |
| **Availability** | 99.9% uptime | Production reliability |
| **Maximum Results** | 20 repositories per query | Manageable result size |

---

## 7. Out of Scope (v1)

- ❌ README content search (phase 2)
- ❌ Code-level semantic search (phase 2)
- ❌ Automatic project categorization (phase 2)
- ❌ Real-time star/fork tracking (phase 2)
- ❌ Custom curated lists/collections (phase 2)
- ❌ Project health scoring (phase 2)

---

## 8. Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| **Query Relevance** | > 80% of top-5 results relevant | User feedback, manual review |
| **Response Time** | < 2 seconds | Logging and monitoring |
| **User Satisfaction** | > 4/5 rating | Feedback collection |
| **Search Adoption** | > 100 searches/week | Usage analytics |
| **Zero Errors** | 99.9% successful queries | Error logging |

---

## 9. Implementation Roadmap

### Phase 1: MVP (Current)
- [x] Semantic search over repository metadata
- [x] Language and star filtering
- [x] Topic-based filtering
- [x] MCP server implementation
- [ ] Integration with Claude Code

### Phase 2: Enhanced Search
- [ ] README content indexing
- [ ] Code snippet search
- [ ] Project trend analysis
- [ ] Automatic categorization

### Phase 3: Intelligence
- [ ] Project health scoring
- [ ] Technology trend detection
- [ ] Smart recommendations
- [ ] Custom collections/lists

---

## 10. API/Tool Specification

### Tool 1: search_projects

**Purpose:** Semantic search for GitHub projects

**Parameters:**
```
query (required): str - Natural language query
language: str (optional) - Filter by language (Python, JavaScript, etc.)
min_stars: int (optional, default 1000) - Minimum star count
topics: List[str] (optional) - Filter by topics
max_age_months: int (optional) - Only recent projects
limit: int (optional, default 10, max 20) - Results to return
```

**Response:**
```json
{
  "results": [
    {
      "repo_name": "owner/project",
      "owner": "owner",
      "stars": 5000,
      "clone_url": "https://github.com/owner/project",
      "language": "Python",
      "description": "...",
      "topics": ["tag1", "tag2"],
      "relevance_score": 0.95,
      "last_updated": "2026-01-01"
    }
  ],
  "total_results": 123,
  "query_executed_in_ms": 450
}
```

### Tool 2: similar_projects

**Purpose:** Find projects similar to a given repository

**Parameters:**
```
repo_name (required): str - Repository name (owner/name)
language: str (optional) - Filter by language
min_stars: int (optional, default 1000)
limit: int (optional, default 10, max 20)
```

**Response:**
Same as search_projects

### Tool 3: filter_by_language

**Purpose:** Browse projects by language

**Parameters:**
```
language (required): str - Programming language
min_stars: int (optional, default 1000)
limit: int (optional, default 20)
sort_by: str (optional) - "stars", "recent", "relevance"
```

**Response:**
List of top projects in that language

### Tool 4: get_trending

**Purpose:** Get trending/popular projects

**Parameters:**
```
language: str (optional) - Filter by language
timeframe: str (optional) - "week", "month", "year"
limit: int (optional, default 20)
```

**Response:**
Top trending projects

---

## 11. Integration Points

### Integration with Claude Code

When users ask Claude Code questions like:
- "Find similar game projects to Phaser.js"
- "Show me REST API examples in Go"
- "Find Python ML projects with 5000+ stars"

Claude Code can use gh-search MCP server tools to:
1. Automatically search for relevant projects
2. Provide direct links and clone URLs
3. Show project metadata and statistics
4. Suggest implementations to reference

### Integration Points

1. **MCP Server Registration** - Add to Claude Code MCP server list
2. **Tool Discovery** - Claude sees available search tools
3. **Query Routing** - Claude routes project-search questions to gh-search
4. **Result Formatting** - Return structured data for Claude to interpret

---

## 12. Security & Privacy

- ✅ Public data only (GitHub public repositories)
- ✅ No authentication required
- ✅ No data storage of user queries
- ✅ Rate limiting to prevent abuse
- ✅ No API keys exposed in responses

---

## 13. Glossary

| Term | Definition |
|------|-----------|
| **Repository** | A GitHub project/codebase |
| **Stars** | GitHub's bookmark/favorite metric for repositories |
| **Topics** | User-applied tags describing a repository's purpose |
| **Semantic Search** | Search that understands meaning, not just keywords |
| **MCP Server** | Model Context Protocol server providing tools to Claude |
| **Relevance Score** | 0-1 score indicating how well a project matches query |

---

## 14. Appendix: Sample Queries

```
Query: "Tower Defense game engine"
Results:
  1. tower-defense-framework (Python) - 2.5K stars
  2. phaser-tower-defense (JavaScript) - 1.8K stars
  3. gdscript-tower-defense (GDScript) - 890 stars (filtered out < 1000)

Query: "REST API boilerplate with OAuth2"
Results:
  1. express-oauth2-api (JavaScript) - 5.2K stars
  2. fastapi-auth-template (Python) - 3.1K stars
  3. go-oauth-server (Go) - 4.5K stars

Query: "Transformer model PyTorch"
Results:
  1. pytorch-transformers (Python) - 85K stars
  2. hugging-face/transformers (Python) - 120K stars
  3. fairseq (Python) - 28K stars
```

---

**End of Document**
