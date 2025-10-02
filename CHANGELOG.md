# Changelog

All notable changes to the XojoDoc project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Python project structure with pyproject.toml
- MIT License
- Source package structure in `src/xojodoc/`
- HTML structure analysis document (`docs/HTML_STRUCTURE.md`)
- Database schema design for SQLite + FTS5
- HTML parser module (`parser.py`) with BeautifulSoup
- Database management module (`database.py`) with FTS5 support
- Indexer coordinator (`indexer.py`) for building documentation index
- Data models: XojoClass, XojoProperty, XojoMethod
- Test suite for Sprint 2 (`test_sprint2.py`)
- Development documentation (`docs/DEVELOPMENT.md`)

### Planned
- Basic CLI with simple search
- Interactive TUI with rich/textual
- Export mode for AI context

---

## [0.0.1] - 2025-10-02

### Added
- XojoDoc project initialization
- README.md with project vision, architecture and objectives
- CHANGELOG.md for change tracking
- BACKLOG.md for task management and timeline
- Xojo HTML source documentation in `/html/`

### Context
- Project initiated to solve lack of CLI access to Xojo documentation
- Goal: Reduce development friction with AI assistants from 80% to ~30%
- First version focused on MVP with basic functionality

---

## Version Notes

### Format
- **[Added]** for new features
- **[Changed]** for changes in existing functionality
- **[Deprecated]** for features that will be removed
- **[Removed]** for features already removed
- **[Fixed]** for bug fixes
- **[Security]** for vulnerabilities

### Enlaces
[Unreleased]: https://github.com/mbuchichio/xojodocs/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/mbuchichio/xojodocs/releases/tag/v0.0.1
