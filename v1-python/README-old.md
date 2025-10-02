# XojoDoc

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0--WIP-orange.svg)]()

CLI documentation browser for Xojo, inspired by Unix `man` pages.

> ⚠️ **v2.0 in progress** - Being rewritten in native Xojo for better performance and smaller size.  
> The Python version (v1.0-alpha) is deprecated. See [v1-python/](v1-python/) folder.

## Why v2.0?

**v1.0-alpha (Python)** worked but had issues:
- 18 MB executable (Python runtime)
- 40+ second build times
- Packaging complexity

**v2.0 (Xojo)** will have:
- ~2 MB executable ✨
- ~5 second builds ⚡
- Zero dependencies 🎯
- Native SQLite

## Current Status

🚧 **Work in Progress** - See [xojo/](xojo/) folder for development.

## Features (v2.0)

- 🔍 Fast search across 1,400+ Xojo classes
- 📖 Full descriptions with code examples
- ⚡ SQLite FTS5 full-text search (< 0.1s)
- 🎯 Search classes, properties, and methods
- 💻 Command-line interface

## Quick Start (when v2.0 is ready)

```bash
# Download xojodoc.exe from releases
# Run it - creates xojodoc.conf automatically

# Build the index
xojodoc --reindex

# Search
xojodoc Button
```

## Usage

```bash
# Search classes
xojodoc Button

# Show class details
xojodoc -c DesktopWindow

# Show method details  
xojodoc -c Graphics -m DrawString

# Show all properties and methods
xojodoc -c Color -a

# Rebuild database
xojodoc --reindex
```

### TUI Keyboard Shortcuts

| Key     | Action            |
|---------|-------------------|
| `/`     | Focus search      |
| `↑` `↓` | Navigate          |
| `Enter` | View class        |
| `d`     | Toggle deprecated |
| `q`     | Quit              |

## Search Features

- Prefix matching: `xojodoc Desk` finds DesktopWindow, DesktopButton, etc.
- Module.class format: `xojodoc -c desktop.DesktopWindow`
- Case-insensitive search
- Deprecated classes hidden by default

## Configuration

Edit `xojodoc.conf` (created automatically on first run):

```ini
[paths]
html_root = C:\Program Files\Xojo\Xojo 2025r2.1\Xojo Resources\Language Reference\html
database = xojo.db
```

Then rebuild:

```bash
xojodoc --reindex
```

## Documentation

- [Installation Guide](docs/INSTALLATION.md) - Detailed setup and troubleshooting
- [Development](docs/DEVELOPMENT.md) - Contributing and architecture

## Tech Stack

- Python 3.8+, BeautifulSoup4, SQLite FTS5, Textual, Click

## License

MIT License - See [LICENSE](LICENSE)

## Author

Mario Buchichio - [mbuchichio](https://github.com/mbuchichio)

---

**Note:** XojoDoc is an independent project and is not affiliated with or endorsed by Xojo, Inc.
