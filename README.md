## XojoDoc - CLI Documentation System for Xojo

[![GitHub](https://img.shields.io/badge/GitHub-xojodocs-blue?logo=github)](https://github.com/mbuchichio/xojodocs)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

### Project Vision
**XojoDoc** is an independent CLI documentation tool for the Xojo language, inspired by Unix's `man` command. It solves a critical problem in the Xojo ecosystem: the lack of quick terminal access to documentation and the friction this creates when using AI assistants for development.

**Repository:** [github.com/mbuchichio/xojodocs](https://github.com/mbuchichio/xojodocs)

### Problem It Solves
- No CLI tool exists to query Xojo documentation
- Developers waste ~80% of time fixing AI-generated code that doesn't know Xojo syntax
- Documentation is only accessible via IDE or web, not optimized for modern development workflow
- AI assistants (Claude, GPT, Copilot) generate incorrect code due to lack of context about Xojo

### Proposed Technical Architecture

**Stack:**
- Python with BeautifulSoup for HTML parsing
- SQLite with FTS5 for indexed full-text search
- TUI with rich/textual for interactive mode
- Source documentation: Local Xojo HTML (already available)

**Components:**
```
xojodoc/
├── xojodoc.py         # Main CLI and entry point
├── indexer.py         # HTML Parser → SQLite with FTS5
├── tui.py             # Interactive man/less-like interface
├── exporter.py        # AI context generator
└── xojo.db            # Indexed database
```

### Operation Modes

1. **Interactive Mode** (`xojodoc`)
   - Navigable TUI with class/method panel
   - Real-time search
   - man/less-style navigation

2. **Query Mode** (`xojodoc Graphics.DrawString`)
   - Direct terminal output
   - Scriptable and workflow-integrable

3. **Export Mode** (`xojodoc --export-for-ai`)
   - Generate markdown file with Xojo context for AI
   - Include correct syntax, common patterns, gotchas

### Expected Impact
- Reduce Xojo development friction from 80% to ~30%
- Benefit the entire Xojo community (no competition exists)
- Dramatically improve AI-generated code quality
- Accelerate Xojo application development

### MVP - First Version
- Parse basic HTML documentation (classes, methods, syntax)
- Simple command-line search
- Export of top 100 most common methods
- Basic TUI for navigation

### Future Expansion
- User code analysis for personalized context
- Editor integration via LSP
- Share with Xojo community as open source project
- Auto-update when documentation changes