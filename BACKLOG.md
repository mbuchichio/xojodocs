# Backlog - XojoDoc

Timeline y tareas pendientes para el desarrollo de XojoDoc.

---

## 🎯 MVP - Versión 0.1.0 (Meta: 2-3 semanas)

### Sprint 1: Análisis y Arquitectura (Días 1-3)
- [x] Crear estructura inicial del proyecto
- [x] Documentar visión y arquitectura en README
- [x] Configurar changelog y backlog
- [ ] Analizar estructura de HTML fuente
  - [ ] Identificar patrones en archivos HTML
  - [ ] Mapear estructura de clases, métodos, propiedades
  - [ ] Documentar formato de ejemplos de código
- [ ] Diseñar esquema de base de datos SQLite
  - [ ] Tabla de clases
  - [ ] Tabla de métodos/propiedades
  - [ ] Índices FTS5 para búsqueda
- [ ] Definir estructura de proyecto Python
  - [ ] Configurar pyproject.toml / requirements.txt
  - [ ] Definir módulos principales

### Sprint 2: Parser e Indexador (Días 4-7)
- [ ] Implementar `indexer.py`
  - [ ] Parser HTML con BeautifulSoup
  - [ ] Extracción de clases y métodos
  - [ ] Extracción de descripciones y ejemplos
  - [ ] Limpieza de HTML a texto plano/markdown
- [ ] Implementar base de datos SQLite
  - [ ] Crear esquema inicial
  - [ ] Configurar FTS5 para búsqueda full-text
  - [ ] Scripts de migración
- [ ] Testear indexación completa
  - [ ] Verificar todas las clases se indexan
  - [ ] Validar calidad de extracción
  - [ ] Medir tiempos de indexación

### Sprint 3: CLI Básico (Días 8-10)
- [ ] Implementar `xojodoc.py`
  - [ ] Entry point con argumentos CLI
  - [ ] Búsqueda básica por nombre de clase/método
  - [ ] Output formateado a terminal
  - [ ] Manejo de errores básico
- [ ] Modo query simple
  - [ ] `xojodoc NombreClase` → mostrar info de clase
  - [ ] `xojodoc NombreClase.Metodo` → mostrar info de método
  - [ ] Búsqueda fuzzy si no hay match exacto
- [ ] Tests básicos de CLI

### Sprint 4: TUI Interactivo (Días 11-14)
- [ ] Implementar `tui.py`
  - [ ] Interfaz básica con rich/textual
  - [ ] Panel de navegación de clases
  - [ ] Panel de contenido con scroll
  - [ ] Búsqueda en tiempo real
- [ ] Navegación estilo man/less
  - [ ] Atajos de teclado (q, /, hjkl)
  - [ ] Scroll suave
  - [ ] Highlighting de sintaxis
- [ ] Pulir UX interactivo

### Sprint 5: Export para AI (Días 15-17)
- [ ] Implementar `exporter.py`
  - [ ] Modo `--export-for-ai`
  - [ ] Selección de top 100 métodos más comunes
  - [ ] Generación de markdown optimizado
  - [ ] Incluir patrones comunes y gotchas
- [ ] Documentar uso para AI assistants
  - [ ] Instrucciones de integración con Claude/GPT
  - [ ] Ejemplos de prompts efectivos

### Sprint 6: Pulido y Documentación (Días 18-21)
- [ ] Tests completos
  - [ ] Unit tests para parser
  - [ ] Integration tests para CLI
  - [ ] Tests de TUI (manual)
- [ ] Documentación de usuario
  - [ ] Guía de instalación
  - [ ] Ejemplos de uso
  - [ ] Troubleshooting
- [ ] Packaging
  - [ ] Configurar setup.py / pyproject.toml
  - [ ] Scripts de instalación
  - [ ] Verificar dependencias
- [ ] Release MVP 0.1.0

---

## 🚀 Fase 2: Mejoras Post-MVP (1-2 meses)

### Funcionalidades Mejoradas
- [ ] Búsqueda avanzada con filtros
- [ ] Historial de búsquedas
- [ ] Favoritos/bookmarks
- [ ] Exportar resultados a archivo
- [ ] Sintaxis highlighting mejorado
- [ ] Temas de color personalizables

### Integración y Automatización
- [ ] Auto-actualización de documentación
- [ ] Detección de versión de Xojo
- [ ] Múltiples versiones de docs en paralelo
- [ ] Integración con VS Code vía extension
- [ ] Integración con otros editores

### Análisis de Código Usuario
- [ ] Escanear proyectos Xojo del usuario
- [ ] Generar contexto personalizado basado en uso
- [ ] Sugerencias de métodos relacionados
- [ ] Detección de patrones comunes en proyectos

---

## 🌟 Fase 3: Comunidad y Expansión (3+ meses)

### Open Source
- [ ] Preparar para release público
- [ ] Licencia y contribución guidelines
- [ ] CI/CD con GitHub Actions
- [ ] Publicar en PyPI
- [ ] Website/landing page

### LSP (Language Server Protocol)
- [ ] Implementar Xojo Language Server
- [ ] Autocompletado con contexto
- [ ] Hover documentation
- [ ] Go to definition
- [ ] Integración universal con editores

### Comunidad
- [ ] Compartir con foro Xojo
- [ ] Tutorial videos
- [ ] Blog posts sobre el proyecto
- [ ] Recopilar feedback de usuarios
- [ ] Roadmap guiado por comunidad

---

## 📊 Métricas de Éxito

### MVP
- [ ] Indexar 100% de clases core de Xojo
- [ ] Tiempo de búsqueda < 100ms
- [ ] TUI responsive y estable
- [ ] Export genera contexto útil para AI

### Post-MVP
- [ ] 50+ usuarios activos
- [ ] Reducción medible de errores en código generado por AI
- [ ] Feedback positivo de comunidad Xojo
- [ ] Contributors externos al proyecto

---

## 🐛 Bugs Conocidos

_(Ninguno todavía - proyecto en fase inicial)_

---

## 💡 Ideas Futuras (Icebox)

- [ ] Plugin para Xojo IDE
- [ ] Modo offline completo con cache
- [ ] Sincronización de notas/anotaciones personales
- [ ] Integración con Stack Overflow para ejemplos
- [ ] Generador de snippets desde documentación
- [ ] Modo tutorial interactivo para aprender Xojo
- [ ] Comparador de versiones de API entre versiones Xojo
- [ ] AI local para responder preguntas sobre docs

---

**Última actualización:** 2025-10-02  
**Estado actual:** Sprint 1 - Análisis y Arquitectura
