# XojoDoc v1.0-alpha (Python) - DEPRECATED

⚠️ **This version is deprecated and no longer maintained.**

The Python implementation (v0.1.0-alpha) worked but had issues:
- 18 MB executable size (includes Python runtime)
- 40+ second build times with PyInstaller
- Import system complexity (relative vs absolute)
- Difficult to test and package

## Migration to v2.0

XojoDoc v2.0 is being rewritten in native Xojo. See the `/xojo` folder for the new implementation.

**v2.0 benefits:**
- ~2 MB executable
- ~5 second builds
- Zero external dependencies
- Native SQLite support
- Much easier to maintain

## What's Here

This folder contains the complete Python implementation for reference:

- `src/xojodoc/` - Python source code
- `tests/` - Test suite (incomplete)
- `docs/` - Documentation
- `pyproject.toml` - Python package configuration
- `xojodoc.spec` - PyInstaller build spec
- `RELEASE_NOTES_v0.1.0-alpha.md` - Release notes

## If You Want to Run This Version

1. Install Python 3.8+
2. `pip install -e .`
3. `xojodoc --reindex`
4. `xojodoc Button`

## Lessons Learned

This version taught us:
- SQLite FTS5 works great for documentation search
- Need to index properties/methods in FTS (not just classes)
- Configuration auto-generation is important
- Python packaging is painful for desktop apps

**The future is native Xojo.** 🎯
