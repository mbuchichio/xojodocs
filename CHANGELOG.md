# Changelog - XojoDoc

Historial de cambios del proyecto.

## [2025-10-02] - Sprint 6: Polish y Release 🚀

### 🎉 Agregado
- **Sistema de configuración simplificado** - `xojodoc.conf` auto-generado
- **config.py** - Módulo para leer configuración sin editar código
- **xojodoc --reindex** - Comando integrado para rebuild (reemplaza reindex.py)
- **README simplificado** - Conciso, directo, lenguaje sobrio
- **INSTALLATION.md** - Guía práctica sin verbosidad
- **Test framework** - tests/test_parser.py estructura inicial
- **Version bump** - 0.1.0-alpha preparando release

### 📝 Documentación
- xojodoc.conf: Se crea automáticamente si no existe
- Archivo de configuración minimalista (solo html_root y database)
- Eliminada complejidad innecesaria (temp paths, múltiples locations)
- README y docs simplificados: foco en lo esencial

### 🔧 Modificado  
- pyproject.toml - Version 0.1.0-alpha
- Development Status - Pre-Alpha → Alpha
- reindex.py - Usa sistema de configuración simple, no borra DB
- indexer.py - Eliminada lógica de temp_db_path
- config.py - Busca solo en directorio de la app, auto-genera si falta

### 🐛 Corregido
- reindex.py ya no borra la DB existente (el indexer actualiza registros)
- Encoding errors con emojis en Windows (removidos)
- Imports innecesarios eliminados

### 💡 Decisiones de Diseño
- **Una sola ubicación de config** - Solo junto a la app (no CWD, no home)
- **Sin temp path** - Diferencia de performance no justifica complejidad
- **Auto-generación** - Primera ejecución crea config con defaults
- **Rutas macOS/Linux omitidas** - Mejor no poner info incorrecta
- **CLI unificado** - `xojodoc --reindex` en vez de script separado

---

## [2025-10-02] - Descripciones Completas ✅

### 🎉 Agregado
- **Descripciones completas** - Properties y methods ahora tienen documentación completa con ejemplos de código
- **CLI con descripciones** - Flag `-a` ahora muestra descripciones completas de cada property/method
- **Ejemplos de código** - Methods incluyen code examples con indentación y color
- **Indexación optimizada en SSD** - Database se construye en C:\temp para mayor velocidad, luego se mueve al proyecto
- **Script reindex.py** - Facilita reconstrucción completa de base de datos
- **1405 clases indexadas** - Cobertura completa con parsing recursivo (vs 717 anterior)
- **Prefix matching** - Buscar "Desk" encuentra "DesktopWindow", "DesktopButton", etc.
- **Filtro deprecated** - Toggle con tecla `d` en TUI (ocultos por defecto)
- **Debouncing 500ms** - Reduce queries durante escritura
- **Search module.class** - Formato "desktop.window" soportado
- **CLI simplificado** - `xojodoc` = TUI, `xojodoc Graphics` = search (sin subcomandos)

### 🔧 Modificado  
- **Parser HTML** - Reescrito para extraer de `<blockquote>` después de `<hr id="...">` (antes buscaba `<section>` incorrectamente)
- **Sidebar TUI** - Aumentado a 40 caracteres (vs 35)
- **Ordenamiento** - Resultados alfabéticos en todas las búsquedas

### ✅ Corregido
- **Descripciones NULL** - Parser ahora navega correctamente la estructura HTML con `next_siblings`
- **Duplicados** - Agregado `DISTINCT` a queries FTS5
- **Classes faltantes** - Parsing recursivo con `rglob()` encuentra subdirectorios
- **Errores FTS5** - Sanitización de caracteres especiales con regex

### 🔨 Detalles Técnicos
- Métodos `_extract_property_description()` y `_extract_method_description()` completamente reescritos
- Indexer soporta `temp_db_path` con auto-movimiento al finalizar
- Schema BD: campos `description` y `sample_code` ahora populados correctamente

---

## [Sprints 1-4] - MVP Core Completado

### Sprint 1 - Análisis y Arquitectura ✅
- Estructura del proyecto
- Análisis de HTML de Xojo
- Diseño de schema SQLite + FTS5

### Sprint 2 - Parser e Indexer ✅
- Parser HTML con BeautifulSoup
- Database SQLite con FTS5
- Indexación incremental (100x más rápido: 0.2s vs 10+ min)
- Tracking de `file_mtime` para cambios

### Sprint 3 - CLI Básico ✅  
- CLI con Click framework
- Search, class, method commands
- Output formateado con Rich
- 6 tests passing

### Sprint 4 - TUI Interactivo ✅
- TUI con Textual framework
- Layout de dos paneles
- Search en tiempo real
- Navegación estilo man/less (q, /, ?, hjkl)
- 6 tests passing

---

## [2025-10-02] - Inicio del Proyecto

### Creación
- Proyecto XojoDoc iniciado
- README con visión y arquitectura
- Estructura básica del proyecto

### Objetivo
Reducir fricción en desarrollo Xojo con AI assistants de 80% a ~30% de tiempo perdido corrigiendo código incorrecto.
