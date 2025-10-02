# XojoDoc Native - Design Document

**Version:** 2.0  
**Platform:** Xojo Console Application  
**Target:** Windows (expandible a macOS/Linux)

## 🎯 Objetivos

Reescribir XojoDoc en Xojo nativo para:
- Build instantáneo (5s vs 40s)
- Ejecutable ligero (2 MB vs 18 MB)
- Cero dependencias externas
- Sin problemas de packaging
- La herramienta de Xojo, hecha en Xojo

## 📐 Arquitectura

### 1. XojoDocDatabase (Clase)
**Responsabilidad:** Manejo de SQLite y FTS5

**Propiedades:**
- `db As SQLiteDatabase`
- `dbPath As String`

**Métodos:**
```xojo
Sub Constructor(dbPath As String)
Sub CreateSchema()
Function InsertClass(name As String, module As String, description As String, ...) As Integer
Sub InsertProperty(classId As Integer, name As String, type As String, ...)
Sub InsertMethod(classId As Integer, name As String, parameters As String, ...)
Sub UpdateSearchIndex(classId As Integer)
Function SearchClasses(query As String) As RowSet
Function GetClassInfo(className As String) As Dictionary
Function GetProperties(classId As Integer) As RowSet
Function GetMethods(classId As Integer) As RowSet
```

**Schema SQLite:**
```sql
-- Classes table
CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    module TEXT,
    description TEXT,
    sample_code TEXT,
    file_path TEXT,
    file_mtime REAL,
    indexed_at REAL
);

-- Properties table
CREATE TABLE properties (
    id INTEGER PRIMARY KEY,
    class_id INTEGER,
    name TEXT NOT NULL,
    type TEXT,
    read_only INTEGER DEFAULT 0,
    shared INTEGER DEFAULT 0,
    description TEXT,
    FOREIGN KEY (class_id) REFERENCES classes(id)
);

-- Methods table
CREATE TABLE methods (
    id INTEGER PRIMARY KEY,
    class_id INTEGER,
    name TEXT NOT NULL,
    parameters TEXT,
    return_type TEXT,
    shared INTEGER DEFAULT 0,
    description TEXT,
    sample_code TEXT,
    FOREIGN KEY (class_id) REFERENCES classes(id)
);

-- FTS5 search index
CREATE VIRTUAL TABLE search_index USING fts5(
    class_name,
    module,
    description,
    content
);
```

### 2. HTMLParser (Clase)
**Responsabilidad:** Parsear HTML de Xojo

**Propiedades:**
- `htmlRoot As FolderItem`

**Métodos:**
```xojo
Sub Constructor(htmlRoot As FolderItem)
Function ParseClass(htmlFile As FolderItem) As Dictionary
Function ParseProperties(htmlFile As FolderItem) As Dictionary()
Function ParseMethods(htmlFile As FolderItem) As Dictionary()
Function ExtractDescription(html As String, sectionId As String) As String
```

**Estrategias de parsing:**
1. **HTMLViewer + ExecuteJavaScript** - Usar DOM nativo
2. **Regex** - Patrones para extraer sections
3. **String manipulation** - Buscar `<hr id="...">` y `<blockquote>`

### 3. Indexer (Clase)
**Responsabilidad:** Coordinar indexación

**Propiedades:**
- `db As XojoDocDatabase`
- `parser As HTMLParser`
- `htmlRoot As FolderItem`

**Métodos:**
```xojo
Sub Constructor(db As XojoDocDatabase, htmlRoot As FolderItem)
Sub IndexAll(verbose As Boolean = True)
Function IndexClass(htmlFile As FolderItem) As Boolean
Function DiscoverClasses() As FolderItem()
```

**Flujo:**
1. Recorrer `htmlRoot` recursivamente
2. Para cada `.html`:
   - ParseClass → InsertClass
   - ParseProperties → InsertProperty (loop)
   - ParseMethods → InsertMethod (loop)
   - UpdateSearchIndex
3. Mostrar progreso en consola

### 4. ConfigManager (Clase)
**Responsabilidad:** Leer/escribir config

**Métodos:**
```xojo
Function GetHtmlRoot() As FolderItem
Function GetDatabasePath() As String
Sub CreateDefaultConfig()
Function ConfigExists() As Boolean
```

**xojodoc.conf (formato INI):**
```ini
[paths]
html_root = C:\Program Files\Xojo\Xojo 2025r2.1\Xojo Resources\Language Reference\html
database = xojo.db
```

**Parsing INI en Xojo:**
```xojo
Function ReadINI(file As TextInputStream) As Dictionary
  Dim config As New Dictionary
  Dim currentSection As String
  
  While Not file.EndOfFile
    Dim line As String = file.ReadLine.Trim
    
    If line.BeginsWith("[") And line.EndsWith("]") Then
      currentSection = line.Middle(2, line.Length - 2)
      config.Value(currentSection) = New Dictionary
    ElseIf line.Contains("=") Then
      Dim parts() As String = line.Split("=")
      Dim key As String = parts(0).Trim
      Dim value As String = parts(1).Trim
      config.Value(currentSection).Value(key) = value
    End If
  Wend
  
  Return config
End Function
```

### 5. ConsoleApplication (App principal)
**Responsabilidad:** CLI interface

**Eventos:**
```xojo
Sub Run(args() As String)
  Select Case args.Count
  Case 0
    ' No args → error (sin TUI por ahora)
    Print "Usage: xojodoc [OPTIONS] [QUERY]"
    Print "Try: xojodoc --help"
    
  Case 1
    If args(0) = "--help" Then
      ShowHelp()
    ElseIf args(0) = "--reindex" Then
      DoReindex()
    Else
      ' Search
      DoSearch(args(0))
    End If
    
  Case 2
    ' -c CLASS
    If args(0) = "-c" Then
      ShowClass(args(1))
    End If
    
  Case 4
    ' -c CLASS -m METHOD
    If args(0) = "-c" And args(2) = "-m" Then
      ShowMethod(args(1), args(3))
    End If
  End Select
End Sub

Sub DoReindex()
  Dim config As ConfigManager = ConfigManager.GetInstance()
  Dim htmlRoot As FolderItem = config.GetHtmlRoot()
  Dim dbPath As String = config.GetDatabasePath()
  
  Dim db As New XojoDocDatabase(dbPath)
  db.CreateSchema()
  
  Dim parser As New HTMLParser(htmlRoot)
  Dim indexer As New Indexer(db, parser)
  
  indexer.IndexAll(True) ' verbose
End Sub

Sub DoSearch(query As String)
  Dim db As New XojoDocDatabase("xojo.db")
  Dim results As RowSet = db.SearchClasses(query)
  
  Dim count As Integer = 0
  While Not results.AfterLastRow
    count = count + 1
    Print Str(count) + ". " + results.Column("name").StringValue
    Print "   " + results.Column("description").StringValue.Left(80) + "..."
    Print ""
    results.MoveToNextRow
  Wend
End Sub

Sub ShowClass(className As String)
  Dim db As New XojoDocDatabase("xojo.db")
  Dim info As Dictionary = db.GetClassInfo(className)
  
  If info = Nil Then
    Print "Class '" + className + "' not found."
    Return
  End If
  
  Print "=== " + info.Value("name") + " ==="
  Print ""
  Print info.Value("description")
  Print ""
  
  ' Properties
  Dim props As RowSet = db.GetProperties(info.Value("id"))
  If props.RowCount > 0 Then
    Print "PROPERTIES:"
    While Not props.AfterLastRow
      Print "  " + props.Column("name").StringValue + " : " + props.Column("type").StringValue
      props.MoveToNextRow
    Wend
  End If
  
  ' Methods
  Dim methods As RowSet = db.GetMethods(info.Value("id"))
  If methods.RowCount > 0 Then
    Print ""
    Print "METHODS:"
    While Not methods.AfterLastRow
      Print "  " + methods.Column("name").StringValue + "(" + methods.Column("parameters").StringValue + ")"
      methods.MoveToNextRow
    Wend
  End If
End Sub
```

## 📦 Output

**Ejecutable final:**
- `xojodoc.exe` (2 MB)
- `xojodoc.conf` (auto-generado)
- `xojo.db` (generado con --reindex)

## 🚀 Build Process

1. Abrir `XojoDoc.xojo_binary_project`
2. Build → Build Application (Windows)
3. Resultado: `dist/xojodoc.exe`
4. Tiempo: ~5 segundos

## 📋 TODO List (Sprint 7)

- [ ] Crear proyecto Xojo Console Application
- [ ] Implementar `XojoDocDatabase` clase
- [ ] Implementar `HTMLParser` clase (con regex/string parsing)
- [ ] Implementar `Indexer` clase
- [ ] Implementar `ConfigManager` clase
- [ ] Implementar CLI en App.Run()
- [ ] Testing con documentación real
- [ ] Build y verificar tamaño (~2 MB)
- [ ] README con instrucciones

## 🎯 Success Criteria

- ✅ Build en < 10 segundos
- ✅ .exe < 5 MB
- ✅ Indexa 1405 clases correctamente
- ✅ Búsqueda funciona (FTS5)
- ✅ CLI funcional (search, -c, -m, --reindex)
- ✅ Config auto-generada
- ✅ Sin dependencias externas

## 🔮 Future (v2.1)

- Desktop UI (en vez de CLI)
- WebView para mostrar HTML original
- Hyperlinks clickeables
- History/Back navigation
- Export to PDF/Markdown
