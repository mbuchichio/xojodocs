# VS Code + MSYS2 Development Setup

## Instalación de MSYS2

1. **Instalar MSYS2** (si no lo tenés):
   - Descargar: https://www.msys2.org/
   - Instalar en: `C:\msys64` (ruta por defecto)

2. **Instalar herramientas de desarrollo**:
   ```bash
   # Abrir terminal MSYS2 MINGW64
   pacman -Syu
   pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-gdb mingw-w64-x86_64-sqlite3
   ```

3. **Agregar a PATH de Windows**:
   - Ir a: Sistema → Configuración avanzada → Variables de entorno
   - Agregar: `C:\msys64\mingw64\bin`
   - Reiniciar VS Code

## Uso en VS Code

### 🔨 Compilar

**Opción 1: Atajo de teclado**
- Presionar `Ctrl+Shift+B`
- Seleccionar: "Build (MSYS2 MinGW)"

**Opción 2: Command Palette**
- Presionar `Ctrl+Shift+P`
- Escribir: "Tasks: Run Build Task"

**Opción 3: Terminal**
```powershell
# Desde terminal integrado de VS Code
gcc -g -Wall -o xojodoc.exe src/main.c src/database.c src/display.c -lsqlite3
```

### 🐛 Debugear

**Opción 1: F5 (Quick Debug)**
- Abrir `src/main.c`
- Poner breakpoint (click en margen izquierdo)
- Presionar `F5`
- Seleccionar: "Debug (MSYS2 GDB)"

**Opción 2: Run and Debug Panel**
- Click en ícono de Debug (Ctrl+Shift+D)
- Seleccionar configuración:
  - "Debug (MSYS2 GDB)" - ejecuta con args `["timer"]`
  - "Debug Class Lookup" - ejecuta con args `["-c", "Timer"]`
  - "Debug Current File" - para en entry point
- Presionar `F5`

### 📋 IntelliSense

El archivo `c_cpp_properties.json` ya está configurado para:
- ✅ Autocompletado de código
- ✅ Navegación a definiciones (F12)
- ✅ Hover para documentación
- ✅ Warnings en tiempo real

### 🎯 Configuraciones Disponibles

**tasks.json** (Ctrl+Shift+B):
- **Build (MSYS2 MinGW)** - Debug build con `-g`
- **Build Release** - Optimizado con `-O2 -s`
- **Build Static** - Con SQLite embebido
- **Clean** - Elimina binarios
- **Run** - Compila y ejecuta
- **Test Search** - Compila y busca "timer"

**launch.json** (F5):
- **Debug (MSYS2 GDB)** - Debug con búsqueda
- **Debug Class Lookup** - Debug con `-c Timer`
- **Debug Current File** - Para en main()

## Troubleshooting

### ❌ "gcc not found"

Verificar PATH:
```powershell
$env:PATH -split ';' | Select-String msys64
gcc --version
```

Si no aparece, agregar manualmente:
```powershell
$env:PATH += ";C:\msys64\mingw64\bin"
```

### ❌ "cannot find -lsqlite3"

Instalar SQLite3:
```bash
# En terminal MSYS2
pacman -S mingw-w64-x86_64-sqlite3
```

### ❌ "gdb.exe not found"

Ajustar ruta en `.vscode/launch.json`:
```json
"miDebuggerPath": "C:/msys64/mingw64/bin/gdb.exe"
```

O instalar:
```bash
pacman -S mingw-w64-x86_64-gdb
```

### ❌ IntelliSense no funciona

1. Instalar extensión: "C/C++" (ms-vscode.cpptools)
2. Recargar VS Code
3. Verificar ruta en `c_cpp_properties.json`

## Workflow Recomendado

1. **Editar código** en `src/*.c`
2. **Compilar**: `Ctrl+Shift+B`
3. **Debugear**: `F5`
4. **Ver output**: Terminal integrado muestra resultados
5. **Breakpoints**: Click en margen izquierdo
6. **Variables**: Hover sobre variables o panel "Variables"
7. **Call Stack**: Panel "Call Stack" muestra jerarquía de llamadas

## Atajos Útiles

- `Ctrl+Shift+B` - Build
- `F5` - Start debugging
- `F9` - Toggle breakpoint
- `F10` - Step over
- `F11` - Step into
- `Shift+F11` - Step out
- `Ctrl+F5` - Run without debugging
- `F12` - Go to definition
- `Shift+F12` - Find all references

¡Listo para desarrollar! 🚀
