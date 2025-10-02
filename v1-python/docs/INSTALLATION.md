# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (included with Python)
- Git

## Installation Steps

### 1. Check Python

```bash
python --version
```

Should show Python 3.8 or higher. If not, download from [python.org](https://www.python.org/downloads/).

### 2. Clone Repository

```bash
git clone https://github.com/mbuchichio/xojodocs.git
cd xojodocs
```

### 3. Install Package

```bash
pip install -e .
```

### 4. Build Index

```bash
xojodoc --reindex
```

This takes 5-10 minutes and creates `xojo.db` with all documentation.

If `xojodoc.conf` doesn't exist, it will be created automatically.

### 5. Test

```bash
xojodoc
```

Should launch the interactive TUI.

## Configuration

The config file `xojodoc.conf` is created automatically on first run.

Edit `xojodoc.conf` to match your Xojo installation:

```ini
[paths]
html_root = C:\Your\Path\To\Xojo\html
database = xojo.db
```

Then rebuild:

```bash
xojodoc --reindex
```

**Note:** When packaged as .exe, `xojodoc.conf` should be next to the executable.

## Troubleshooting

### Command not found: xojodoc

Try using the full module path:

```bash
python -m xojodoc.cli
```

Or add Python's Scripts directory to your PATH.

### FileNotFoundError during indexing

Check that the Xojo HTML path in `xojodoc.conf` is correct. It should point to:

```
C:\Program Files\Xojo\Xojo 2025r2.1\Xojo Resources\Language Reference\html
```

### ModuleNotFoundError

Reinstall the package:

```bash
pip install -e .
```

### TUI display issues

Use a modern terminal:
- Windows: Windows Terminal (recommended)
- Linux: any terminal with UTF-8 support
- macOS: Terminal.app works fine

## Updating

```bash
cd xojodocs
git pull
pip install -e .
```

To rebuild index after Xojo update:

```bash
python -m xojodoc.indexer --force
```

## Uninstalling

```bash
pip uninstall xojodoc
```

## Platform Notes

### Windows
- Use Windows Terminal for best results
- Default path: `C:\Program Files\Xojo\...`

### Linux
- May need `python3` instead of `python`
- Install via package manager if needed

### macOS
- Use Homebrew for Python if needed
- Default path: `/Applications/Xojo/...`

## Getting Help

- [GitHub Issues](https://github.com/mbuchichio/xojodocs/issues)
- Email: mbuchichio@users.noreply.github.com
