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

### Features

✨ **1405 Xojo Classes Indexed** - Complete documentation coverage
� **Full Descriptions** - Property and method documentation with examples
�🔍 **Smart FTS5 Search** - Fast full-text search with prefix matching
🎨 **Interactive TUI** - man/less-style browser with Textual
⚡ **Incremental Indexing** - 100x faster updates (0.2s vs 10+ min)
🚫 **Filter Deprecated** - Toggle deprecated classes with `d` key
📦 **Simple CLI** - Intuitive man-like syntax
🔧 **Configurable** - Point to your Xojo installation for faster indexing
💾 **SSD Optimized** - Builds database on fast storage for better performance

### Installation

```bash
# Clone the repository
git clone https://github.com/mbuchichio/xojodocs.git
cd xojodocs

# Install dependencies
pip install -e .

# Build index (fast - builds on SSD then moves to project)
python reindex.py

# Or use the standard indexer
python -m xojodoc.indexer

# Or force rebuild entire index
python -m xojodoc.indexer --force
```

### Quick Start

```bash
# Launch interactive browser (recommended)
python -m xojodoc.cli

# Search for classes
python -m xojodoc.cli Graphics

# Show class details
python -m xojodoc.cli -c DesktopWindow

# Show specific method
python -m xojodoc.cli -c Graphics -m DrawString

# Show all properties and methods
python -m xojodoc.cli -c Graphics -a
```

### CLI Usage

The CLI follows a simple, man-like syntax:

```bash
xojodoc                      # Launch interactive TUI
xojodoc QUERY                # Search for classes
xojodoc -c CLASS             # Show class details
xojodoc -c CLASS -m METHOD   # Show method details
xojodoc -c CLASS -a          # Show all properties and methods
```

**Examples:**

```bash
# Interactive browser
python -m xojodoc.cli

# Search for "Graphics"
python -m xojodoc.cli Graphics

# Show DesktopWindow class
python -m xojodoc.cli -c DesktopWindow

# Show specific method
python -m xojodoc.cli -c Graphics -m DrawString

# Show Color with all details
python -m xojodoc.cli -c Color -a
```

### Interactive TUI

Launch the TUI for a full browsing experience:

```bash
python -m xojodoc.cli
# or
python -m xojodoc.tui
```

**Keyboard Shortcuts:**

- `/` - Focus search box
- `↑` `↓` - Navigate results
- `Enter` - View selected class
- `d` - Toggle deprecated classes (hidden by default)
- `Escape` - Clear search
- `?` - Show help
- `q` - Quit

**TUI Features:**

- 🔍 Real-time search with 500ms debouncing
- 📋 Shows all 1405 classes (deprecated hidden by default)
- 🎯 Prefix matching (type "Desk" finds "DesktopWindow")
- 📖 Full class details with properties, methods, and examples
- 🚫 Toggle deprecated classes on/off
- ⌨️ Keyboard-driven navigation

### Indexing

The indexer supports incremental updates for fast performance:

```bash
# Incremental indexing (default - only changed files)
python -m xojodoc.indexer

# Force rebuild (after Xojo updates)
python -m xojodoc.indexer --force

# Specify custom HTML location
python -m xojodoc.indexer --html-root "C:\Path\To\Xojo\html"

# Specify custom database location
python -m xojodoc.indexer --db-path custom.db
```

**Configuration:**

Edit `DEFAULT_HTML_ROOT` in `src/xojodoc/indexer.py`:

```python
# Default: Points to Xojo installation
DEFAULT_HTML_ROOT = r"C:\Program Files\Xojo\Xojo 2025r2.1\Xojo Resources\Language Reference\html"
```

**Performance:**

- Full indexing: ~5-10 minutes (1405 classes)
- Incremental: ~0.2 seconds (skips unchanged files)
- 100x performance improvement with incremental indexing

### Search Features

**FTS5 Full-Text Search:**

- ✅ Prefix matching - "Desk" finds "DesktopWindow"
- ✅ Module.class format - "desktop.window"
- ✅ No duplicates - DISTINCT results
- ✅ Alphabetically sorted
- ✅ Special character sanitization
- ✅ 500ms debouncing in TUI

**Examples:**

```bash
# Prefix search
python -m xojodoc.cli Desk     # Finds DesktopWindow, DesktopButton, etc.

# Module.class search
python -m xojodoc.cli -c desktop.DesktopWindow

# Multi-word search
python -m xojodoc.cli "Desktop Window"
```

### Architecture

**Stack:**
- Python 3.8+ with BeautifulSoup4 for HTML parsing
- SQLite with FTS5 for indexed full-text search
- Rich + Textual for terminal UI
- Click for CLI argument parsing

**Database Schema:**
```sql
classes (id, name, module, description, sample_code, compatibility, notes, file_path, file_mtime)
properties (id, class_id, name, type, access_flags, description)
methods (id, class_id, name, parameters, return_type, shared, description, sample_code)
search_index (FTS5 virtual table for fast full-text search)
```

**Components:**
```
src/xojodoc/
├── cli.py         # Command-line interface
├── tui.py         # Interactive TUI with Textual
├── parser.py      # HTML parser (BeautifulSoup)
├── database.py    # SQLite + FTS5 operations
├── indexer.py     # Incremental indexing logic
└── models.py      # Data models (XojoClass, XojoProperty, XojoMethod)
```

### Development Roadmap

**Completed (Sprint 1-4):**
- ✅ HTML parser with BeautifulSoup
- ✅ SQLite database with FTS5 indexing
- ✅ Incremental indexing (100x faster)
- ✅ CLI with search/class/method commands
- ✅ Interactive TUI with Textual
- ✅ Recursive directory parsing (1405 classes)
- ✅ Deprecated filter toggle
- ✅ Smart search (prefix matching, module.class)
- ✅ Configurable documentation path

**Future Plans:**
- 📦 PyInstaller packaging (standalone .exe)
- 🤖 AI context export for LLMs
- 🔌 Editor integration (VS Code, Sublime)
- 📊 Usage analytics (most-used classes)
- 🌐 Web API for remote access
- 🔄 Auto-update on Xojo releases

### Contributing

Contributions are welcome! Areas for improvement:

- Additional export formats (JSON, Markdown)
- Enhanced TUI features (bookmarks, history)
- LSP integration for editors
- Performance optimizations
- Documentation improvements
- Test coverage

### License

MIT License - See [LICENSE](LICENSE) for details.

### Credits

**Author:** Mario Buchichio  
**Repository:** [github.com/mbuchichio/xojodocs](https://github.com/mbuchichio/xojodocs)  
**Documentation Source:** Xojo Language Reference (HTML)

---

**Note:** XojoDoc is an independent project and is not affiliated with or endorsed by Xojo, Inc.