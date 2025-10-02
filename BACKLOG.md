# Backlog - XojoDoc

Tareas pendientes y roadmap del proyecto.

---

## 🎯 MVP - Version 0.1.0

### ✅ Completado
- [x] Sprint 1-4: Parser, Database, CLI, TUI
- [x] 1405 clases indexadas con descripciones completas
- [x] FTS5 search con prefix matching
- [x] Filtro de deprecated (toggle con 'd')
- [x] Indexación incremental (100x más rápido)
- [x] Extracción de descripciones y ejemplos de código
- [x] CLI muestra descripciones con flag `-a`
- [x] TUI con layout de dos paneles y search en tiempo real

### 🚧 En Progreso

#### Sprint 6: Polish y Release (ACTIVO)
- [ ] Tests completos
  - [x] Test structure created (tests/test_parser.py)
  - [ ] Implement parser unit tests
  - [ ] Integration tests para CLI
  - [ ] Database tests
  - [ ] TUI tests (manual)
- [x] Documentación de usuario
  - [x] README simplificado y conciso ✅
  - [x] INSTALLATION.md directo y práctico ✅
  - [x] Lenguaje sobrio y profesional ✅
- [x] Version bump to 0.1.0-alpha
- [ ] Packaging
  - [ ] PyInstaller para exe standalone (opcional)
  - [ ] Test en Windows limpio
- [ ] Release MVP 0.1.0
  - [ ] Review final de código
  - [ ] Completar tests básicos
  - [ ] Tag en Git
  - [ ] GitHub Release

---

## 🚀 Phase 2: Mejoras Post-MVP

### Opcional (Post-MVP)
- [ ] **AI Export** - Exportar top 100 métodos en formato optimizado para LLMs
  - Nota: Copilot puede ejecutar `xojodoc` directamente, así que esto puede no ser necesario

### Futuras Mejoras
- [ ] Advanced search con filtros
- [ ] Historial de búsquedas
- [ ] Favoritos/bookmarks
- [ ] Export resultados a archivo
- [ ] Syntax highlighting mejorado
- [ ] Temas de color personalizables
- [ ] Auto-update de documentación
- [ ] VS Code extension
- [ ] Análisis de proyectos del usuario
- [ ] Sugerencias de métodos relacionados

---

## 🌟 Phase 3: Comunidad y Expansión

- [ ] Preparar para release público
- [ ] CI/CD con GitHub Actions
- [ ] Publicar en PyPI
- [ ] LSP (Language Server Protocol) para Xojo
- [ ] Compartir en foro de Xojo
- [ ] Videos tutoriales
- [ ] Contribuciones de la comunidad

---

**Última actualización:** 2025-10-02  
**Estado:** MVP casi completo - Sprint 4 ✅ + Descripciones completas ✅
