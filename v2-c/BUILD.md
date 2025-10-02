# XojoDoc v2.0-c Build Instructions

## Windows (MinGW/MSYS2)

### Option 1: Dynamic Linking (Recommended for development)

1. Install SQLite3:
   ```bash
   # In MSYS2/MinGW terminal
   pacman -S mingw-w64-x86_64-sqlite3
   ```

2. Build:
   ```powershell
   # In PowerShell or CMD
   .\build.bat
   ```

### Option 2: Static Build (No dependencies)

1. Download SQLite amalgamation:
   - Visit: https://www.sqlite.org/download.html
   - Download: `sqlite-amalgamation-XXXXXXX.zip`
   - Extract `sqlite3.c` and `sqlite3.h` to `v2-c/` folder

2. Build:
   ```powershell
   .\build-static.bat
   ```

   This creates a **fully static binary** (~600 KB) with zero dependencies!

---

## Linux/macOS

### Install SQLite3 development files:

**Ubuntu/Debian:**
```bash
sudo apt-get install libsqlite3-dev
```

**Fedora/RHEL:**
```bash
sudo dnf install sqlite-devel
```

**macOS (Homebrew):**
```bash
brew install sqlite3
```

### Build:
```bash
make
```

### Static build (optional):
```bash
make static
```

### Install system-wide:
```bash
sudo make install
```

---

## Testing

1. Copy database from Python indexer:
   ```powershell
   # Windows
   copy ..\v1-python\xojo.db .

   # Linux/macOS
   cp ../v1-python/xojo.db .
   ```

2. Run:
   ```bash
   ./xojodoc timer
   ./xojodoc -c Timer
   ./xojodoc -c Timer -m RunMode
   ```

---

## Troubleshooting

### MinGW Path Issues (Windows)

If you get "cannot find -lsqlite3" error:

1. Check SQLite3 installation:
   ```bash
   # In MSYS2 terminal
   pacman -Qs sqlite
   ```

2. Try static build instead:
   ```powershell
   .\build-static.bat
   ```

### Permission Denied (Linux/macOS)

```bash
chmod +x xojodoc
```

### Database Not Found

Make sure `xojo.db` is in the same folder as the executable, or use:
```bash
./xojodoc --db /path/to/xojo.db timer
```

(Note: `--db` flag needs to be added to `main.c` if you want custom paths)
