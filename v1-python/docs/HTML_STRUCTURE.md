# HTML Structure Analysis

This document describes the structure of the Xojo HTML documentation for parsing purposes.

## Overview

The Xojo documentation is generated using Sphinx and follows the Read the Docs theme structure.

## Directory Structure

```
html/
├── api/                    # API Reference (main target)
│   ├── graphics/          # Module/namespace
│   │   ├── index.html     # Module overview
│   │   ├── graphics.html  # Graphics class
│   │   ├── picture.html   # Picture class
│   │   └── ...
│   ├── data_types/
│   ├── databases/
│   └── ...
├── getting_started/       # Tutorials and guides
├── topics/                # Topic-based documentation
└── resources/             # Additional resources
```

## HTML Structure for Class Documentation

### File Pattern
- **Location**: `html/api/{module}/{class}.html`
- **Example**: `html/api/graphics/graphics.html`

### Key HTML Elements

#### 1. Class Header
```html
<section id="graphics">
  <h1>Graphics</h1>
  <p class="forsearch">Graphics</p>
</section>
```

#### 2. Description Section
```html
<section id="description">
  <h2>Description</h2>
  <p>Graphics class objects are used for drawing...</p>
</section>
```

#### 3. Properties Table
```html
<section id="properties">
  <h2>Properties</h2>
  <table class="table-centered-columns-3-and-4 docutils align-default">
    <thead>
      <tr>
        <th>Name</th>
        <th>Type</th>
        <th>Read-Only</th>
        <th>Shared</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><a href="#graphics-antialiased">AntiAliased</a></td>
        <td><a href="../data_types/boolean.html">Boolean</a></td>
        <td></td>
        <td></td>
      </tr>
      <!-- More properties... -->
    </tbody>
  </table>
</section>
```

#### 4. Methods Section
```html
<section id="methods">
  <h2>Methods</h2>
  <table class="table-centered-columns-2-3-4 docutils align-default">
    <thead>
      <tr>
        <th>Name</th>
        <th>Parameters</th>
        <th>Returns</th>
        <th>Shared</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><a href="#graphics-clearcache">ClearCache</a></td>
        <td></td>
        <td></td>
        <td></td>
      </tr>
      <!-- More methods... -->
    </tbody>
  </table>
</section>
```

#### 5. Property Descriptions
```html
<section id="property-descriptions">
  <h2>Property descriptions</h2>
  
  <section id="graphics-antialiased">
    <h3>Graphics.AntiAliased</h3>
    <p>AntiAliased As Boolean</p>
    <p>Enables or disables anti-aliasing for drawing...</p>
  </section>
  <!-- More property descriptions... -->
</section>
```

#### 6. Method Descriptions
```html
<section id="method-descriptions">
  <h2>Method descriptions</h2>
  
  <section id="graphics-clearcache">
    <h3>Graphics.ClearCache</h3>
    <p>ClearCache()</p>
    <p>Clears cached graphics data...</p>
    
    <!-- Optional: Sample code -->
    <div class="highlight-xojo notranslate">
      <div class="highlight">
        <pre><span class="n">g</span><span class="p">.</span><span class="n">ClearCache</span></pre>
      </div>
    </div>
  </section>
  <!-- More method descriptions... -->
</section>
```

#### 7. Sample Code Section
```html
<section id="sample-code">
  <h2>Sample code</h2>
  <p>Draw a red line...</p>
  <div class="highlight-xojo notranslate">
    <div class="highlight">
      <pre><span class="n">g</span><span class="p">.</span><span class="n">DrawingColor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Color</span><span class="p">.</span><span class="n">Red</span></pre>
    </div>
  </div>
</section>
```

#### 8. Compatibility Section
```html
<section id="compatibility">
  <h2>Compatibility</h2>
  <p>Desktop, Web, Mobile</p>
</section>
```

## Key Identifiers for Parsing

### Section IDs
- `#description` - Class description
- `#properties` - Properties table
- `#methods` - Methods table
- `#property-descriptions` - Detailed property docs
- `#method-descriptions` - Detailed method docs
- `#sample-code` - Code examples
- `#compatibility` - Platform compatibility
- `#enumerations` - Enum definitions (if applicable)
- `#notes` - Additional notes

### CSS Classes
- `.docutils` - Main content tables
- `.highlight-xojo` - Code blocks
- `.admonition` - Note/warning boxes
- `.forsearch` - Searchable class name

## Data to Extract

### For Each Class:
1. **Class Name** - From `<h1>` in main section
2. **Module/Namespace** - From file path
3. **Description** - From `#description` section
4. **Properties**:
   - Name (with anchor link)
   - Type (with link to type definition)
   - Read-only flag
   - Shared flag
   - Detailed description (from property-descriptions)
5. **Methods**:
   - Name (with anchor link)
   - Parameters
   - Return type
   - Shared flag
   - Detailed description (from method-descriptions)
   - Sample code (if available)
6. **Enumerations** (if applicable):
   - Enum name
   - Values
   - Descriptions
7. **Sample Code** - General usage examples
8. **Compatibility** - Supported platforms
9. **Notes** - Additional information

## Parsing Strategy

### Phase 1: Discovery
1. Scan `html/api/` directory recursively
2. Find all `.html` files (excluding `index.html`)
3. Build file list with module/class relationships

### Phase 2: Extraction
For each class file:
1. Parse HTML with BeautifulSoup
2. Extract class metadata (name, module)
3. Extract description
4. Parse properties table → extract details from property-descriptions
5. Parse methods table → extract details from method-descriptions
6. Extract enumerations if present
7. Extract sample code
8. Extract compatibility info
9. Extract additional notes

### Phase 3: Storage
Store in SQLite database:
```sql
-- Classes table
CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    module TEXT NOT NULL,
    description TEXT,
    sample_code TEXT,
    compatibility TEXT,
    notes TEXT,
    file_path TEXT,
    UNIQUE(module, name)
);

-- Properties table
CREATE TABLE properties (
    id INTEGER PRIMARY KEY,
    class_id INTEGER,
    name TEXT NOT NULL,
    type TEXT,
    read_only BOOLEAN,
    shared BOOLEAN,
    description TEXT,
    FOREIGN KEY(class_id) REFERENCES classes(id)
);

-- Methods table
CREATE TABLE methods (
    id INTEGER PRIMARY KEY,
    class_id INTEGER,
    name TEXT NOT NULL,
    parameters TEXT,
    return_type TEXT,
    shared BOOLEAN,
    description TEXT,
    sample_code TEXT,
    FOREIGN KEY(class_id) REFERENCES classes(id)
);

-- Full-text search
CREATE VIRTUAL TABLE search_index USING fts5(
    class_name,
    module,
    description,
    content='classes',
    content_rowid='id'
);
```

## Edge Cases & Considerations

1. **Inherited Members**: Some classes may inherit properties/methods (need to track)
2. **Overloaded Methods**: Multiple signatures for same method name
3. **Deprecated Items**: May have special markers
4. **Platform-Specific**: Some methods only available on certain platforms
5. **Code Examples**: May contain multiple languages (Xojo, JavaScript for Web)
6. **Links**: Internal links to other classes need to be preserved or resolved

## Testing Files

Good candidates for initial testing:
- `html/api/graphics/graphics.html` - Complex class with many methods
- `html/api/graphics/picture.html` - Medium complexity
- `html/api/data_types/string.html` - Core type
- `html/api/files/folderitem.html` - File handling

## Next Steps

1. Create HTML parser module
2. Test on sample files
3. Build database schema
4. Implement FTS5 indexing
5. Create query interface
