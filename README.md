# XojoDoc

Fast, offline documentation browser for Xojo programming language.

## Overview

XojoDoc provides instant access to Xojo's documentation directly from the command line. Built with a hybrid architecture: Python for indexing HTML documentation, C for ultra-fast searching.

### Why XojoDoc?

- **⚡ Blazing Fast**: <10ms search response vs 3-5s browser load
- **📴 Offline**: No internet required
- **🎯 Fuzzy Search**: Auto-prefix matching finds what you need
- **🔍 Granular Filtering**: Show only properties, methods, or descriptions
- **🚫 API2 Compatible**: Deprecated classes hidden by default
- **📦 Tiny**: 50 KB binary + SQLite

## Architecture

- **v1-python**: HTML scraper and FTS5 database indexer
- **v2-c**: Native C binary for instant searches (current main tool)

## Installation

### Prerequisites

- Python 3.x (for indexing)
- SQLite3
- GCC/MinGW (for building C version)

### Setup

1. **Index the documentation** (one-time):
   ```bash
   cd v1-python
   pip install -r requirements.txt
   xojodoc --reindex  # or python -m xojodoc --reindex
   ```

2. **Build C version**:
   ```bash
   cd v2-c
   # Windows (MSYS2/MinGW):
   gcc -O2 -Wall -Wextra -o xojodoc.exe src/main.c src/database.c src/display.c -lsqlite3 -s
   
   # Copy to PATH:
   cp xojodoc.exe /path/to/bin/
   ```

3. **Copy database**:
   ```bash
   cp v1-python/xojo.db v2-c/
   # Or place next to xojodoc.exe
   ```

## Usage

### Basic Search

```bash
# Fuzzy prefix search (auto-wildcard)
xojodoc timer          # Finds Timer, WebTimer, iOSTimer, etc.
xojodoc desktop        # Finds DesktopWindow, DesktopButton, etc.

# List all classes (API2 only)
xojodoc "*"

# Include deprecated classes
xojodoc -dep timer
xojodoc --deprecated "*"
```

### Class Details

```bash
# Full class documentation
xojodoc -c Timer

# Filter sections (D=Description, P=Properties, M=Methods, S=Sample)
xojodoc -c Timer -P       # Only properties
xojodoc -c Timer -M       # Only methods
xojodoc -c Timer -PM      # Properties + methods
xojodoc -c Timer -D       # Only description
xojodoc -c Timer -S       # Only sample code
```

### Member Lookup

```bash
# Find specific property or method
xojodoc -c Timer -m RunMode
xojodoc -c DesktopWindow -m Close
```

### Pagination

```powershell
# PowerShell
xojodoc "*" | Select-Object -First 20
xojodoc "*" | more

# Bash
xojodoc "*" | head -20
xojodoc "*" | less
```

## Features

### Search
- **Fuzzy prefix matching**: Automatically adds `*` suffix
- **FTS5 full-text search**: Fast SQLite-based indexing
- **No result limits**: Returns all matches (filter with `more`/`less`)
- **Deprecated filtering**: Hide old API by default (`-dep` to include)

### Display
- **Section filters**: `-DPMS` flags for granular output
- **Member search**: Direct property/method lookup
- **Color output**: Syntax highlighting in terminal (ANSI colors)
- **ASCII-safe**: No Unicode issues in Windows console

### Performance
- **Binary size**: 50 KB (stripped, optimized)
- **Startup**: <10ms
- **Search**: Instant with FTS5 index
- **Memory**: Minimal (SQLite streaming)

## Examples

```bash
# Quick reference
xojodoc timer                    # Find timer-related classes
xojodoc -c Timer -P              # List Timer properties
xojodoc -c Timer -m Period       # Show Timer.Period details
xojodoc desktop                  # Find Desktop* classes
xojodoc "*" | grep Window        # All classes with "Window"
xojodoc -dep xojo                # Include deprecated Xojo.* classes

# Piping to other tools
xojodoc "*" | wc -l              # Count all classes
xojodoc timer | Select-Object -First 10  # First 10 results
```

## Configuration

XojoDoc looks for `xojo.db` in these locations (in order):
1. Same directory as `xojodoc.exe`
2. Current working directory

## Development

### Project Structure

```
xojodoc/
├── v1-python/          # Python indexer
│   ├── xojodoc/        # Package source
│   │   ├── cli.py      # CLI entry point
│   │   ├── parser.py   # HTML parser
│   │   ├── database.py # SQLite wrapper
│   │   └── indexer.py  # FTS5 indexer
│   └── xojo.db         # Generated database
│
└── v2-c/               # C search tool (main)
    ├── src/
    │   ├── main.c      # CLI and argument parsing
    │   ├── database.c  # SQLite queries
    │   ├── display.c   # Terminal output
    │   └── *.h         # Headers
    └── xojodoc.exe     # Compiled binary
```

### Building from Source

**Windows (MSYS2/MinGW64):**
```bash
pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-sqlite3
gcc -O2 -Wall -Wextra -o xojodoc.exe src/*.c -lsqlite3 -s
```

**Linux:**
```bash
apt-get install libsqlite3-dev
gcc -O2 -Wall -Wextra -o xojodoc src/*.c -lsqlite3 -s
```

**macOS:**
```bash
brew install sqlite3
gcc -O2 -Wall -Wextra -o xojodoc src/*.c -lsqlite3 -s
```

### Updating Documentation

When Xojo releases new versions:

```bash
cd v1-python
xojodoc --reindex
cp xojo.db ../v2-c/
```

## Technical Details

### Database Schema

```sql
-- Main tables
CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    module TEXT,
    description TEXT,
    compatibility TEXT,
    sample_code TEXT
);

CREATE TABLE properties (
    class_id INTEGER,
    name TEXT,
    type TEXT,
    description TEXT,
    FOREIGN KEY(class_id) REFERENCES classes(id)
);

CREATE TABLE methods (
    class_id INTEGER,
    name TEXT,
    type TEXT,
    description TEXT,
    FOREIGN KEY(class_id) REFERENCES classes(id)
);

-- FTS5 index
CREATE VIRTUAL TABLE search_index USING fts5(
    class_name, module, description,
    content='classes'
);
```

### Search Algorithm

1. **Prefix matching**: Query `timer` → FTS5 query `timer*`
2. **Ranking**: SQLite's `rank` function orders by relevance
3. **Filtering**: `WHERE module != 'deprecated'` (unless `-dep`)
4. **No limits**: Returns all results (Unix philosophy)

## API2 Compatibility

By default, XojoDoc excludes deprecated classes and modules:
- `deprecated` module
- `deprecated_*` modules (e.g., `deprecated_class_members`)

Use `-dep` or `--deprecated` to include them for legacy code.

## Limitations

- **Read-only**: Cannot edit documentation
- **Local only**: Requires pre-indexed database
- **HTML source**: Depends on Xojo's documentation structure
- **No dynamic updates**: Must re-index for new Xojo versions

## Roadmap

- [ ] JSON output format (`--json`)
- [ ] Auto-update from Xojo website
- [ ] Cross-reference links between classes
- [ ] Interactive TUI mode (like `man` with navigation)
- [ ] VS Code extension integration
- [ ] Static binary (embedded SQLite)

## License

MIT License - see LICENSE file

## Credits

Built by frustrated developers who got tired of waiting for browsers to load documentation. 🚀

## Contributing

PRs welcome! Especially for:
- New output formats (JSON, Markdown, HTML)
- Platform-specific optimizations
- Bug fixes in parser
- Documentation improvements
