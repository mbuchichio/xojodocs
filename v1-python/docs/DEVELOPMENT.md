# XojoDoc Development

## Setup Development Environment

### 1. Install Dependencies

```bash
# Install the package in development mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

### 2. Build the Documentation Index

```bash
# From project root
python -m xojodoc.indexer

# Or with custom paths
python -m xojodoc.indexer --html-root html --db-path xojo.db
```

### 3. Test the Parser

```python
from xojodoc.parser import HTMLParser
from xojodoc.database import Database

# Test parsing a single class
parser = HTMLParser("html")
xojo_class = parser.parse_class_file("html/api/graphics/graphics.html")
print(f"Class: {xojo_class.name}")
print(f"Module: {xojo_class.module}")
print(f"Description: {xojo_class.description[:100]}...")

# Test properties
properties = parser.parse_properties("html/api/graphics/graphics.html")
print(f"\nFound {len(properties)} properties")
for prop in properties[:3]:
    print(f"  - {prop.name}: {prop.type}")

# Test methods
methods = parser.parse_methods("html/api/graphics/graphics.html")
print(f"\nFound {len(methods)} methods")
for method in methods[:3]:
    print(f"  - {method.name}({method.parameters or ''})")
```

### 4. Test the Database

```python
from xojodoc.database import Database, XojoClass, XojoProperty, XojoMethod

# Create and initialize database
with Database("test.db") as db:
    db.create_schema()
    
    # Insert a test class
    test_class = XojoClass(
        name="Graphics",
        module="graphics",
        description="Graphics class for drawing"
    )
    class_id = db.insert_class(test_class)
    
    # Insert a property
    prop = XojoProperty(
        name="DrawingColor",
        type="Color",
        read_only=False,
        description="The color used for drawing"
    )
    db.insert_property(class_id, prop)
    
    # Search
    results = db.search_classes("Graphics")
    print(results)
```

## Project Structure

```
xojodocs/
├── src/
│   └── xojodoc/
│       ├── __init__.py        # Package initialization
│       ├── database.py        # SQLite database management
│       ├── parser.py          # HTML parser
│       ├── indexer.py         # Indexer coordinator
│       ├── cli.py             # CLI interface (TODO)
│       ├── tui.py             # TUI interface (TODO)
│       └── exporter.py        # AI export (TODO)
├── tests/                     # Test files (TODO)
├── docs/                      # Documentation
│   └── HTML_STRUCTURE.md
├── html/                      # Xojo HTML documentation
├── pyproject.toml
├── README.md
└── LICENSE
```

## Sprint 2 Progress

### Completed
- ✅ Database module with SQLite + FTS5
- ✅ HTML parser with BeautifulSoup
- ✅ Indexer coordinator
- ✅ Data models (XojoClass, XojoProperty, XojoMethod)

### Testing Checklist
- [ ] Parse Graphics class successfully
- [ ] Parse Picture class successfully
- [ ] Parse String class successfully
- [ ] Extract all properties correctly
- [ ] Extract all methods correctly
- [ ] Extract sample code
- [ ] Store in database
- [ ] Search functionality works
- [ ] FTS5 search performance

### Next Steps (Sprint 3)
- [ ] Create CLI interface with Click
- [ ] Implement query mode (`xojodoc ClassName`)
- [ ] Format output for terminal
- [ ] Add fuzzy search
- [ ] Error handling

## Common Commands

```bash
# Run indexer
python -m xojodoc.indexer

# Run with verbose output
python -m xojodoc.indexer --html-root html

# Quiet mode
python -m xojodoc.indexer --quiet

# Custom database path
python -m xojodoc.indexer --db-path custom.db
```

## Troubleshooting

### Import errors
Make sure dependencies are installed:
```bash
pip install beautifulsoup4 lxml rich textual click
```

### Database locked
Close any open connections:
```python
db.close()
```

### Parsing errors
Check HTML structure matches expectations in `docs/HTML_STRUCTURE.md`
