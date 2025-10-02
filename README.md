# XojoDoc

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

CLI documentation browser for Xojo, inspired by Unix `man` pages.

## Features

- 🔍 Fast search across 1405 Xojo classes
- 🎨 Interactive terminal UI with keyboard navigation
- ⚡ Quick access without opening IDE or browser
- 🤖 Works with AI assistants (Copilot, Claude, GPT)

## Installation

```bash
git clone https://github.com/mbuchichio/xojodocs.git
cd xojodocs
pip install -e .
```

First time setup - build the index:

```bash
xojodoc --reindex
```

This creates `xojodoc.conf` if needed and builds the database.

## Usage

```bash
# Interactive browser
xojodoc

# Search classes
xojodoc Button

# Show class details
xojodoc -c DesktopWindow

# Show method details
xojodoc -c Graphics -m DrawString

# Show all properties and methods
xojodoc -c Color -a
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
