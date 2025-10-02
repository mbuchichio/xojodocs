## XojoDoc - Sistema de Documentación CLI para Xojo

### Visión del Proyecto
**XojoDoc** es una herramienta de documentación CLI independiente para el lenguaje Xojo, inspirada en `man` de Unix. Resuelve un problema crítico en el ecosistema Xojo: la falta de acceso rápido a documentación desde terminal y la fricción que esto genera al usar AI assistants para desarrollo.

### Problema que Resuelve
- No existe herramienta CLI para consultar documentación de Xojo
- Desarrolladores pierden ~80% del tiempo corrigiendo código generado por AI que no conoce la sintaxis Xojo
- La documentación solo es accesible vía IDE o web, no optimizada para workflow de desarrollo moderno
- AI assistants (Claude, GPT, Copilot) generan código incorrecto por falta de contexto sobre Xojo

### Arquitectura Técnica Propuesta

**Stack:**
- Python con BeautifulSoup para parsing HTML
- SQLite con FTS5 para búsqueda full-text indexada  
- TUI con rich/textual para modo interactivo
- Documentación fuente: HTML local de Xojo (ya disponible)

**Componentes:**
```
xojodoc/
├── xojodoc.py         # CLI principal y entry point
├── indexer.py         # Parser HTML → SQLite con FTS5
├── tui.py             # Interfaz interactiva tipo man/less
├── exporter.py        # Generador de contexto para AI
└── xojo.db            # Base de datos indexada
```

### Modos de Operación

1. **Modo Interactivo** (`xojodoc`)
   - TUI navegable con panel de clases/métodos
   - Búsqueda en tiempo real
   - Navegación tipo man/less

2. **Modo Query** (`xojodoc Graphics.DrawString`)
   - Output directo a terminal
   - Integrable en scripts y workflows

3. **Modo Export** (`xojodoc --export-for-ai`)
   - Genera archivo markdown con contexto Xojo para AI
   - Incluye sintaxis correcta, patrones comunes, gotchas

### Impacto Esperado
- Reducir fricción de desarrollo con Xojo de 80% a ~30%
- Beneficiar a toda la comunidad Xojo (no existe competencia)
- Mejorar dramáticamente la calidad del código generado por AI
- Acelerar desarrollo de aplicaciones Xojo

### MVP - Primera Versión
- Parsear documentación HTML básica (clases, métodos, sintaxis)
- Búsqueda por comando simple
- Export de los 100 métodos más comunes
- TUI básica para navegación

### Expansión Futura
- Análisis de código del usuario para contexto personalizado
- Integración con editores vía LSP
- Compartir con comunidad Xojo como proyecto open source
- Auto-actualización cuando cambie la documentación