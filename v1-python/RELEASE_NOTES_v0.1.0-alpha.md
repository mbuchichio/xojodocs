# XojoDoc v0.1.0-alpha

First alpha release of XojoDoc - Command-line documentation browser for Xojo.

## 📥 Installation

1. Download `xojodoc.exe` from the release assets
2. Place it in a directory of your choice
3. Run `xojodoc.exe` - it will create `xojodoc.conf`
4. Edit `xojodoc.conf` to point to your Xojo installation:
   ```ini
   [paths]
   html_root = C:\Program Files\Xojo\Xojo 2025r2.1\Xojo Resources\Language Reference\html
   database = xojo.db
   ```
5. Run `xojodoc --reindex` to build the documentation database

## 🚀 Quick Start

```bash
# First time: index your Xojo documentation
xojodoc --reindex

# Search for classes
xojodoc Button

# Show class details
xojodoc -c DesktopWindow

# Show class with all properties and methods
xojodoc -c Graphics -a

# Show specific method
xojodoc -c Graphics -m DrawString

# Launch interactive TUI browser
xojodoc
```

## ✨ Features

- 🔍 **Full-text search** - Search across 1,405 Xojo classes, properties, and methods
- 📖 **Complete descriptions** - Properties and methods include full documentation with code examples
- 💻 **Interactive TUI** - Textual-based terminal UI with real-time search
- ⚡ **Fast SQLite FTS5** - Instant search with full-text indexing
- 🎯 **Deprecated filter** - Toggle deprecated classes on/off (hidden by default)
- 🔄 **Auto-configuration** - Generates config file on first run
- 📝 **Syntax highlighting** - Code examples with proper formatting

## 🎮 TUI Controls

- `↑/↓` or `j/k` - Navigate results
- `/` - Focus search box
- `d` - Toggle deprecated classes filter
- `Enter` - Show class details
- `Esc` - Back to search results
- `q` - Quit

## ⚠️ Alpha Release Notes

This is an **alpha release** with some limitations:

- **Windows only** - PyInstaller build (18 MB executable)
- **Python runtime included** - No Python installation required, but larger file size
- **Requires Xojo installation** - Needs access to Xojo's HTML documentation
- **Cannot redistribute database** - Legal/licensing reasons - users must generate their own

## 🐛 Known Issues

- No macOS/Linux builds yet (Windows only)
- TUI hyperlinks not implemented
- Unit tests incomplete (framework in place)
- Large executable size (18 MB due to Python runtime)

## 🔮 Roadmap (v2.0)

v2.0 will be **rewritten in native Xojo**:

- ✨ Instant build (~5s vs 40s)
- 💪 Lighter executable (~2 MB vs 18 MB)
- 🎯 Zero dev dependencies (no pip, no Python)
- 🏗️ The Xojo tool, made in Xojo

## 📊 Statistics

- **1,405 classes** indexed
- **~15,000 properties** documented
- **~20,000 methods** documented
- **Search time**: < 0.1s for most queries
- **Index time**: ~2 minutes (one-time operation)

## 🙏 Requirements

- Windows 10/11
- Local Xojo installation (any recent version)
- ~20 MB disk space (5 MB database + 18 MB executable)

## 📝 Configuration

The `xojodoc.conf` file uses INI format:

```ini
[paths]
# Path to Xojo's HTML documentation
html_root = C:\Program Files\Xojo\Xojo 2025r2.1\Xojo Resources\Language Reference\html

# Path to the SQLite database (relative or absolute)
database = xojo.db
```

## 🐞 Bug Reports

Found a bug? Please report it on [GitHub Issues](https://github.com/mbuchichio/xojodocs/issues).

## 📄 License

See [LICENSE](LICENSE) file for details.

---

**Note**: This tool parses your local Xojo installation's documentation. It does not redistribute Xojo's proprietary documentation files.

See [CHANGELOG.md](CHANGELOG.md) for complete version history.
