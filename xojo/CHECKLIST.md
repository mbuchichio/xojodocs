# XojoDoc Native - Sprint 7 Checklist

## 🎯 Goal
Build XojoDoc v2.0 in native Xojo - lightweight, fast, no Python BS.

---

## Phase 1: Project Setup ✅
- [ ] Create Xojo Console Application project
- [ ] Name: "XojoDoc"
- [ ] Save as: `xojodoc/xojo/XojoDoc.xojo_binary_project`
- [ ] Set build target: Windows 64-bit
- [ ] Test basic "Hello World" build

---

## Phase 2: Database Layer
- [ ] Create `XojoDocDatabase` class
- [ ] Add `db As SQLiteDatabase` property
- [ ] Implement `Constructor(dbPath As String)`
- [ ] Implement `CreateSchema()` with all tables
- [ ] Implement `InsertClass()` method
- [ ] Implement `InsertProperty()` method
- [ ] Implement `InsertMethod()` method
- [ ] Implement `UpdateSearchIndex()` method (FTS5)
- [ ] Implement `SearchClasses(query As String)` method
- [ ] Implement `GetClassInfo(className As String)` method
- [ ] Test with sample data

---

## Phase 3: HTML Parser
- [ ] Create `HTMLParser` class
- [ ] Add `htmlRoot As FolderItem` property
- [ ] Implement `Constructor(htmlRoot As FolderItem)`
- [ ] Implement `ParseClass(file As FolderItem)` - extract name, module, description
- [ ] Implement `ParseProperties(file As FolderItem)` - extract all properties
- [ ] Implement `ParseMethods(file As FolderItem)` - extract all methods
- [ ] Implement `ExtractDescription(html As String, sectionId As String)` helper
- [ ] Test with real Xojo HTML files (Button.html, Timer.html, etc.)
- [ ] Verify descriptions are complete with examples

---

## Phase 4: Indexer
- [ ] Create `Indexer` class
- [ ] Add `db As XojoDocDatabase` property
- [ ] Add `parser As HTMLParser` property
- [ ] Implement `Constructor(db, parser)`
- [ ] Implement `DiscoverClasses()` - recursive folder scan
- [ ] Implement `IndexClass(file As FolderItem)` - index single class
- [ ] Implement `IndexAll(verbose As Boolean)` - index all classes
- [ ] Add progress output (1/1405, 2/1405, etc.)
- [ ] Test full indexing of Xojo docs

---

## Phase 5: Configuration Manager
- [ ] Create `ConfigManager` class
- [ ] Implement `ReadINI(file As TextInputStream)` parser
- [ ] Implement `GetHtmlRoot()` method
- [ ] Implement `GetDatabasePath()` method
- [ ] Implement `CreateDefaultConfig()` method
- [ ] Implement `ConfigExists()` method
- [ ] Test config creation and reading

---

## Phase 6: CLI Implementation
- [ ] Implement `App.Run(args() As String)` handler
- [ ] Implement `ShowHelp()` - display usage
- [ ] Implement `DoReindex()` - rebuild database
- [ ] Implement `DoSearch(query As String)` - search classes
- [ ] Implement `ShowClass(className As String)` - display class details
- [ ] Implement `ShowMethod(className, methodName)` - display method details
- [ ] Add `-a` flag for "show all" properties/methods
- [ ] Test all CLI commands

---

## Phase 7: Build & Package
- [ ] Build for Windows 64-bit
- [ ] Verify .exe size (should be ~2 MB)
- [ ] Test .exe on clean machine (no Xojo IDE)
- [ ] Test --reindex creates xojodoc.conf
- [ ] Test search works correctly
- [ ] Test class details display correctly
- [ ] Verify FTS5 searches properties/methods

---

## Phase 8: Documentation
- [ ] Create README.md for xojo/ folder
- [ ] Document build process
- [ ] Document testing process
- [ ] Create CHANGELOG entry for v2.0
- [ ] Update main README with deprecation notice for Python version

---

## Phase 9: Testing
- [ ] Test: Search "Button" finds DesktopButton, PushButton, etc.
- [ ] Test: Search "runmode" finds Timer.RunMode property
- [ ] Test: `-c Timer` shows Timer class with all properties/methods
- [ ] Test: `-c Timer -m Constructor` shows specific method
- [ ] Test: --reindex completes without errors
- [ ] Performance: Index time < 3 minutes
- [ ] Performance: Search time < 0.1s

---

## Phase 10: Release
- [ ] Git tag v2.0.0
- [ ] GitHub release with xojodoc.exe
- [ ] Archive Python version (tag v1.0-alpha-deprecated)
- [ ] Celebrate! 🎉

---

## Notes

**Why this will be better:**
- No Python runtime (18 MB → 2 MB)
- No PyInstaller headaches
- No import issues
- Build in 5 seconds vs 40 seconds
- Native SQLite support
- Easy to debug and extend

**Start here:**
1. Open Xojo
2. New → Console Application
3. Save in `xojodoc/xojo/`
4. Add first class: `XojoDocDatabase`
5. Code and test incrementally

Let's do this! 💪
