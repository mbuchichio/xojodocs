# Changelog - XojoDoc

All notable changes to this project will be documented in this file.

## [2025-10-02] - Sprint 6: Polish & Release 🚀

### 🎉 Added
- **Simplified configuration system** - `xojodoc.conf` auto-generated
- **config.py** - Module to read configuration without editing code
- **xojodoc --reindex** - Integrated rebuild command (replaces reindex.py)
- **Simplified README** - Concise, direct, professional language
- **INSTALLATION.md** - Practical guide without verbosity
- **Test framework** - tests/test_parser.py initial structure
- **Version bump** - 0.1.0-alpha preparing for release

### 📝 Documentation
- xojodoc.conf: Created automatically if missing
- Minimalist config file (only html_root and database)
- Removed unnecessary complexity (temp paths, multiple locations)
- Simplified README and docs: focus on essentials

### 🔧 Changed
- pyproject.toml - Version 0.1.0-alpha
- Development Status - Pre-Alpha → Alpha
- reindex.py - Uses simple config system, doesn't delete DB
- indexer.py - Removed temp_db_path logic
- config.py - Searches only in app directory, auto-generates if missing

### 🐛 Fixed
- reindex.py no longer deletes existing DB (indexer updates records)
- Encoding errors with emojis on Windows (removed)
- Unnecessary imports removed
- **PyInstaller compatibility** - Relative imports converted to absolute
- **Error messages** - No longer mention Python, use `xojodoc --reindex`

### 📦 Packaging
- **PyInstaller** - Spec file created for standalone build
- **xojodoc.exe** - 18 MB executable with everything included
- **xojodoc.conf.template** - Packaged as data file
- **Functional build** - Tested end-to-end with config auto-generation

### 💡 Design Decisions
- **Single config location** - Only next to the app (not CWD, not home)
- **No temp path** - Performance difference doesn't justify complexity
- **Auto-generation** - First run creates config with defaults
- **macOS/Linux paths omitted** - Better not to provide incorrect info
- **Unified CLI** - `xojodoc --reindex` instead of separate script

### 🔮 Future (v2.0)
- **Rewrite in Xojo** - v2.0 will be native Xojo
  - Instant build (~5s vs 40s)
  - Lighter executable (~2 MB vs 18 MB)
  - Zero dev configuration (no pip, no Python)
  - The Xojo tool, made in Xojo 🎯

---

## [2025-10-02] - Full Descriptions ✅

### 🎉 Added
- **Full descriptions** - Properties and methods now have complete documentation with code examples
- **CLI with descriptions** - `-a` flag now shows full descriptions of each property/method
- **Code examples** - Methods include code examples with indentation and color
- **SSD-optimized indexing** - Database built in C:\temp for speed, then moved to project
- **reindex.py script** - Facilitates complete database rebuild
- **1405 classes indexed** - Full coverage with recursive parsing (vs 717 before)
- **Prefix matching** - Searching "Desk" finds "DesktopWindow", "DesktopButton", etc.
- **Deprecated filter** - Toggle with `d` key in TUI (hidden by default)
- **500ms debouncing** - Reduces queries during typing
- **Search module.class** - "desktop.window" format supported
- **Simplified CLI** - `xojodoc` = TUI, `xojodoc Graphics` = search (no subcommands)

### 🔧 Changed
- **HTML Parser** - Rewritten to extract from `<blockquote>` after `<hr id="...">` (previously searched `<section>` incorrectly)
- **TUI Sidebar** - Increased to 40 characters (vs 35)
- **Sorting** - Alphabetical results in all searches

### ✅ Fixed
- **NULL descriptions** - Parser now correctly navigates HTML structure with `next_siblings`
- **Duplicates** - Added `DISTINCT` to FTS5 queries
- **Missing classes** - Recursive parsing with `rglob()` finds subdirectories
- **FTS5 errors** - Special character sanitization with regex

### 🔨 Technical Details
- Methods `_extract_property_description()` and `_extract_method_description()` completely rewritten
- Indexer supports `temp_db_path` with auto-move on completion
- DB schema: `description` and `sample_code` fields now correctly populated

---

## [Sprints 1-4] - Core MVP Completed

### Sprint 1 - Analysis & Architecture ✅
- Project structure
- Xojo HTML analysis
- SQLite + FTS5 schema design

### Sprint 2 - Parser & Indexer ✅
- HTML parser with BeautifulSoup
- SQLite database with FTS5
- Incremental indexing (100x faster: 0.2s vs 10+ min)
- `file_mtime` tracking for changes

### Sprint 3 - Basic CLI ✅
- CLI with Click framework
- Search, class, method commands
- Formatted output with Rich
- 6 tests passing

### Sprint 4 - Interactive TUI ✅
- TUI with Textual framework
- Two-panel layout
- Real-time search
- man/less-style navigation (q, /, ?, hjkl)
- 6 tests passing

---

## [2025-10-02] - Project Start

### Creation
- XojoDoc project initiated
- README with vision and architecture
- Basic project structure

### Objective
Reduce friction in Xojo development with AI assistants from 80% to ~30% of time wasted fixing incorrect code.
