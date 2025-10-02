# XojoDoc Native (Xojo)

**The sane version** - XojoDoc rewritten in native Xojo.

## Why Rewrite?

The Python version (v0.1.0-alpha) taught us what we needed, but had issues:
- 18 MB executable (Python runtime included)
- 40+ second build times (PyInstaller)
- Import issues (relative vs absolute)
- Complex packaging
- Hard to test changes

**Xojo version benefits:**
- 2 MB executable
- 5 second build time
- Zero external dependencies
- Native SQLite support
- Easy to debug and extend
- The Xojo tool, made in Xojo 🎯

## Architecture

See [DESIGN.md](DESIGN.md) for complete architecture documentation.

**Main components:**
1. `XojoDocDatabase` - SQLite + FTS5 management
2. `HTMLParser` - Parse Xojo HTML documentation
3. `Indexer` - Coordinate indexing process
4. `ConfigManager` - Read/write xojodoc.conf
5. `ConsoleApplication` - CLI interface

## Getting Started

1. Open `XojoDoc.xojo_binary_project` in Xojo IDE
2. Build → Build Application (Windows 64-bit)
3. Run `xojodoc.exe --help`

## Development Workflow

1. Make changes in Xojo IDE
2. Click Build (5 seconds)
3. Test in terminal
4. Repeat

No pip, no PyInstaller, no BS. Just code and build.

## Building

**Requirements:**
- Xojo 2024r1 or later
- Windows 10/11 (for Windows builds)

**Steps:**
1. Open project in Xojo
2. Build → Build Application
3. Result: `Builds/xojodoc.exe` (~2 MB)

## Testing

```bash
# Build database
xojodoc --reindex

# Search
xojodoc Button

# Show class
xojodoc -c Timer

# Show method
xojodoc -c Timer -m Constructor
```

## Progress

See [CHECKLIST.md](CHECKLIST.md) for detailed progress tracking.

**Status:** 🚧 Work in Progress (Sprint 7)

## Future Plans (v2.1+)

- Desktop UI instead of CLI
- WebView to show original HTML
- Hyperlinks between classes
- History/navigation
- Export to PDF/Markdown

---

**Note:** The Python version is deprecated. This is the official version going forward.
