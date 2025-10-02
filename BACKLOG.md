# Backlog - XojoDoc

Timeline and pending tasks for XojoDoc development.

**Repository:** [github.com/mbuchichio/xojodocs](https://github.com/mbuchichio/xojodocs)

---

## 🎯 MVP - Version 0.1.0 (Goal: 2-3 weeks)

### Sprint 1: Analysis and Architecture (Days 1-3) ✅ COMPLETE
- [x] Create initial project structure
- [x] Document vision and architecture in README
- [x] Setup changelog and backlog
- [x] Analyze source HTML structure
  - [x] Identify patterns in HTML files
  - [x] Map structure of classes, methods, properties
  - [x] Document code example format
- [x] Design SQLite database schema
  - [x] Classes table
  - [x] Methods/properties table
  - [x] FTS5 indexes for search
- [x] Define Python project structure
  - [x] Configure pyproject.toml / requirements.txt
  - [x] Define main modules

### Sprint 2: Parser and Indexer (Days 4-7) ✅ COMPLETE
- [x] Implement `indexer.py`
  - [x] HTML parser with BeautifulSoup
  - [x] Extract classes and methods
  - [x] Extract descriptions and examples
  - [x] Clean HTML to plain text/markdown
- [x] Implement SQLite database
  - [x] Create schema initial
  - [x] Configure FTS5 for full-text search
  - [x] Migration scripts
- [x] Test complete indexing
  - [x] Verify all classes are indexed (717/717)
  - [x] Validate extraction quality
  - [x] Measure indexing times
- [x] **Incremental indexing** (bonus)
  - [x] Track file modification times
  - [x] Only reindex changed files
  - [x] 100x performance improvement

### Sprint 3: Basic CLI (Days 8-10) ✅ COMPLETE
- [x] Implement `cli.py`
  - [x] Entry point with CLI arguments
  - [x] Basic search by class/method name
  - [x] Formatted terminal output
  - [x] Basic error handling
- [x] Simple query mode
  - [x] `xojodoc search ClassName` → show search results
  - [x] `xojodoc cls ClassName` → show class info
  - [x] `xojodoc method ClassName MethodName` → show method info
- [x] Basic CLI tests
  - [x] All 6 tests passing
  - [x] Help, search, class, method commands
  - [x] Error handling tests

### Sprint 4: Interactive TUI (Days 11-14)
- [ ] Implement `tui.py`
  - [ ] Basic interface with rich/textual
  - [ ] Class navigation panel
  - [ ] Content panel with scroll
  - [ ] Real-time search
- [ ] man/less-style navigation
  - [ ] Keyboard shortcuts (q, /, hjkl)
  - [ ] Smooth scrolling
  - [ ] Syntax highlighting
- [ ] Polish interactive UX

### Sprint 5: AI Export (Days 15-17)
- [ ] Implement `exporter.py`
  - [ ] `--export-for-ai` mode
  - [ ] Select top 100 most common methods
  - [ ] Generate optimized markdown
  - [ ] Include common patterns and gotchas
- [ ] Document usage for AI assistants
  - [ ] Integration instructions with Claude/GPT
  - [ ] Effective prompt examples

### Sprint 6: Polish and Documentation (Days 18-21)
- [ ] Complete tests
  - [ ] Unit tests for parser
  - [ ] Integration tests for CLI
  - [ ] TUI tests (manual)
- [ ] User documentation
  - [ ] Installation guide
  - [ ] Usage examples
  - [ ] Troubleshooting
- [ ] Packaging
  - [ ] Configure setup.py / pyproject.toml
  - [ ] Installation scripts
  - [ ] Verify dependencies
- [ ] Release MVP 0.1.0

---

## 🚀 Phase 2: Post-MVP Improvements (1-2 months)

### Enhanced Features
- [ ] Advanced search with filters
- [ ] Search history
- [ ] Favorites/bookmarks
- [ ] Export results to file
- [ ] Improved syntax highlighting
- [ ] Customizable color themes

### Integration and Automation
- [ ] Auto-update documentation
- [ ] Xojo version detection
- [ ] Multiple doc versions in parallel
- [ ] VS Code integration via extension
- [ ] Integration with other editors

### User Code Analysis
- [ ] Scan user's Xojo projects
- [ ] Generate personalized context based on usage
- [ ] Related method suggestions
- [ ] Common pattern detection in projects

---

## 🌟 Phase 3: Community and Expansion (3+ months)

### Open Source
- [ ] Prepare for public release
- [ ] License and contribution guidelines
- [ ] CI/CD with GitHub Actions
- [ ] Publish to PyPI
- [ ] Website/landing page

### LSP (Language Server Protocol)
- [ ] Implement Xojo Language Server
- [ ] Context-aware autocomplete
- [ ] Hover documentation
- [ ] Go to definition
- [ ] Universal editor integration

### Community
- [ ] Share with Xojo forum
- [ ] Tutorial videos
- [ ] Blog posts about the project
- [ ] Gather user feedback
- [ ] Community-driven roadmap

---

## 📊 Success Metrics

### MVP
- [ ] Index 100% of core Xojo classes
- [ ] Search time < 100ms
- [ ] Responsive and stable TUI
- [ ] Export generates useful AI context

### Post-MVP
- [ ] 50+ active users
- [ ] Measurable reduction in AI-generated code errors
- [ ] Positive feedback from Xojo community
- [ ] External project contributors

---

## 🐛 Known Bugs

_(None yet - project in initial phase)_

---

## 💡 Future Ideas (Icebox)

- [ ] Plugin for Xojo IDE
- [ ] Complete offline mode with cache
- [ ] Personal notes/annotations sync
- [ ] Stack Overflow integration for examples
- [ ] Snippet generator from documentation
- [ ] Interactive tutorial mode to learn Xojo
- [ ] API version comparator between Xojo versions
- [ ] Local AI to answer questions about docs

---

**Last updated:** 2025-10-02  
**Current status:** Sprint 1 - Analysis and Architecture
