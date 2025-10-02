# XojoDoc v2.0 (C Implementation)

Ultra-fast, minimal Xojo documentation browser written in C.

## Why C?

After trying Python (v1) and Xojo native (abandoned due to $500 license cost), C offers:
- ⚡ **Instant startup** (<10ms vs Python's ~500ms)
- 📦 **Tiny binary** (50 KB vs Python's 18 MB)
- 🚀 **Native performance** for SQLite FTS5 queries
- 💰 **Free toolchain** (GCC/MinGW)
- 🔧 **Simple console I/O** (no WinAPI nightmares like Xojo Desktop)

## Architecture

```
v2-c/
├── src/
│   ├── main.c          # Entry point, CLI argument parsing
│   ├── database.c      # SQLite wrapper for FTS5 queries
│   ├── database.h
│   ├── display.c       # Terminal output formatting
│   └── display.h
├── build.bat           # Windows build script (MinGW)
├── Makefile            # Unix build (gcc/clang)
└── xojodoc.exe         # Compiled binary (50 KB)
```

## Features

✅ **Fast fuzzy search** - Auto-prefix matching with FTS5  
✅ **Class details** - Full documentation with properties/methods  
✅ **Member lookup** - Direct access to specific property/method  
✅ **Section filtering** - Show only description, properties, methods, or samples (`-DPMS`)  
✅ **API2 compatible** - Deprecated classes hidden by default (`-dep` to include)  
✅ **No limits** - Returns all results (pipe to `more`/`less` for pagination)  
✅ **Minimal deps** - Only SQLite3 (1.2 MB DLL or statically linked)  
✅ **Cross-platform** - Windows, macOS, Linux

## Build

### Windows (MSYS2/MinGW64)
```bash
# Install dependencies
pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-sqlite3

# Compile
gcc -O2 -Wall -Wextra -o xojodoc.exe src/main.c src/database.c src/display.c -lsqlite3 -s

# Copy to PATH
cp xojodoc.exe /d/Home/Apps/bin/
```

### Unix (GCC/Clang)
```bash
# Install SQLite dev libraries
apt-get install libsqlite3-dev  # Debian/Ubuntu
brew install sqlite3            # macOS

# Build
make

# Install
sudo cp xojodoc /usr/local/bin/
```

## Usage

### Search
```bash
# Fuzzy prefix search (auto-adds *)
xojodoc timer          # Finds Timer, WebTimer, iOSTimer, etc.
xojodoc desktop        # Finds DesktopWindow, DesktopButton, etc.

# List all classes (API2 only, excludes deprecated)
xojodoc "*"

# Include deprecated classes (Xojo.Core.*, deprecated modules)
xojodoc -dep timer
xojodoc --deprecated "*"
```

### Class Details
```bash
# Full class documentation (all sections)
xojodoc -c Timer

# Filter sections: -D (description), -P (properties), -M (methods), -S (sample code)
xojodoc -c Timer -P       # Only properties
xojodoc -c Timer -M       # Only methods
xojodoc -c Timer -PM      # Properties + methods (no desc/sample)
xojodoc -c Timer -D       # Only description
xojodoc -c Timer -DPS     # Desc + props + sample (no methods)
```

### Member Lookup
```bash
# Find specific property or method
xojodoc -c Timer -m RunMode
xojodoc -c Timer -m Period
xojodoc -c DesktopWindow -m Close
```

### Pagination
```powershell
# PowerShell
xojodoc "*" | Select-Object -First 20
xojodoc "*" | more

# Bash/Linux
xojodoc "*" | head -20
xojodoc "*" | less
```

## Database

Uses the same `xojo.db` SQLite database from v1-python indexer.

**Location**: XojoDoc looks for `xojo.db` in:
1. Same directory as `xojodoc.exe`
2. Current working directory

**Update**: Re-run indexer in v1-python when Xojo releases new documentation.

## Performance

| Metric | Value |
|--------|-------|
| Binary Size | 50 KB (stripped) |
| Startup Time | <10ms |
| Search Time | <50ms (FTS5) |
| Memory Usage | ~2-5 MB |
| Build Time | ~1 second |

## Design Goals

1. **Speed** - Startup <10ms, search <50ms
2. **Size** - Binary <100 KB (stripped)
3. **Simplicity** - Clean C code, minimal dependencies
4. **Zero config** - Works out of the box with xojo.db

## Comparison

| Version | Binary Size | Startup Time | Build Time | License Cost |
|---------|-------------|--------------|------------|--------------|
| v1 (Python) | 18 MB | ~500ms | 40s | Free |
| Xojo (abandoned) | ~2 MB | ~100ms | ~5s | $500/year 💀 |
| **v2 (C)** | **50 KB** | **<10ms** | **~1s** | **Free** ✅ |

## Status

✅ **Production Ready**

- [x] Project structure
- [x] Database module (FTS5 queries with deprecated filtering)
- [x] Display module (terminal formatting with ANSI colors)
- [x] Search command (fuzzy prefix, no limits)
- [x] Class details command (with -DPMS section filters)
- [x] Member lookup (-m flag)
- [x] Wildcard support (`*` for list all)
- [x] Deprecated filtering (--deprecated / -dep)
- [x] Build scripts (Windows/Unix)
- [x] Documentation
- [x] Deployed to PATH

## Examples

```bash
# Quick reference workflow
xojodoc timer                    # Search timer-related classes
xojodoc -c Timer -P              # List Timer properties
xojodoc -c Timer -m Period       # Show Timer.Period details

# Exploring Desktop API
xojodoc desktop                  # Find all Desktop* classes
xojodoc -c DesktopWindow -PM     # Properties + methods only

# Finding deprecated API
xojodoc -dep xojo                # Show deprecated Xojo.* classes
xojodoc --deprecated "*" | grep Xojo  # All deprecated Xojo.* entries

# Piping to other tools
xojodoc "*" | wc -l              # Count all API2 classes
xojodoc timer | grep -i web      # Timer classes for web projects
```

## Development

**Adding features:**
1. Edit `src/*.c` files
2. Recompile: `gcc -O2 ... -lsqlite3`
3. Test with `xojodoc <command>`

**Code structure:**
- `main.c`: Argument parsing, global flags (--deprecated)
- `database.c`: All SQLite queries (search, class info, members)
- `display.c`: Terminal output (color formatting, help text)

## License

MIT License - see ../LICENSE

## Credits

Built after frustration with Python's slow startup and Xojo's $500 price tag. 🚀

## Notes

This is a **search-only** implementation. For indexing new documentation:
1. Use v1-python indexer: `cd ../v1-python && xojodoc --reindex`
2. Copy `xojo.db` to v2-c folder
3. Use v2 for instant searches

Think of it as: **Python for indexing (slow), C for searching (fast)**.
