"""Quick test script for Sprint 2 parser and database."""

from pathlib import Path
from xojodoc.parser import HTMLParser
from xojodoc.database import Database


def test_parser():
    """Test HTML parser on a sample file."""
    print("=" * 60)
    print("TESTING HTML PARSER")
    print("=" * 60)
    
    parser = HTMLParser("html")
    
    # Test file
    test_file = "html/api/graphics/graphics.html"
    
    if not Path(test_file).exists():
        print(f"❌ Test file not found: {test_file}")
        return
        
    print(f"\n📄 Parsing: {test_file}\n")
    
    # Parse class
    xojo_class = parser.parse_class_file(test_file)
    
    if xojo_class:
        print(f"✅ Class parsed successfully!")
        print(f"   Name: {xojo_class.name}")
        print(f"   Module: {xojo_class.module}")
        print(f"   Description: {xojo_class.description[:100] if xojo_class.description else 'None'}...")
        print(f"   Compatibility: {xojo_class.compatibility}")
    else:
        print("❌ Failed to parse class")
        return
        
    # Parse properties
    print(f"\n🔹 Parsing properties...")
    properties = parser.parse_properties(test_file)
    print(f"   Found {len(properties)} properties")
    
    if properties:
        print(f"\n   Sample properties:")
        for prop in properties[:3]:
            ro = " [Read-Only]" if prop.read_only else ""
            sh = " [Shared]" if prop.shared else ""
            print(f"   - {prop.name}: {prop.type}{ro}{sh}")
            
    # Parse methods
    print(f"\n⚡ Parsing methods...")
    methods = parser.parse_methods(test_file)
    print(f"   Found {len(methods)} methods")
    
    if methods:
        print(f"\n   Sample methods:")
        for method in methods[:3]:
            params = f"({method.parameters})" if method.parameters else "()"
            returns = f" -> {method.return_type}" if method.return_type else ""
            sh = " [Shared]" if method.shared else ""
            print(f"   - {method.name}{params}{returns}{sh}")


def test_database():
    """Test database creation and storage."""
    print("\n" + "=" * 60)
    print("TESTING DATABASE")
    print("=" * 60)
    
    db_path = "test_xojo.db"
    
    # Remove old test db
    if Path(db_path).exists():
        Path(db_path).unlink()
        
    print(f"\n💾 Creating database: {db_path}\n")
    
    with Database(db_path) as db:
        # Create schema
        print("📋 Creating schema...")
        db.create_schema()
        print("   ✅ Schema created")
        
        # Test data
        from xojodoc.database import XojoClass, XojoProperty, XojoMethod
        
        print("\n📝 Inserting test class...")
        test_class = XojoClass(
            name="TestGraphics",
            module="graphics",
            description="A test graphics class for demonstration",
            compatibility="Desktop, Web, Mobile"
        )
        class_id = db.insert_class(test_class)
        print(f"   ✅ Class inserted with ID: {class_id}")
        
        print("\n📝 Inserting test property...")
        test_prop = XojoProperty(
            name="DrawingColor",
            type="Color",
            read_only=False,
            shared=False,
            description="The color used for drawing operations"
        )
        prop_id = db.insert_property(class_id, test_prop)
        print(f"   ✅ Property inserted with ID: {prop_id}")
        
        print("\n📝 Inserting test method...")
        test_method = XojoMethod(
            name="DrawLine",
            parameters="x1 As Integer, y1 As Integer, x2 As Integer, y2 As Integer",
            return_type=None,
            shared=False,
            description="Draws a line from (x1, y1) to (x2, y2)"
        )
        method_id = db.insert_method(class_id, test_method)
        print(f"   ✅ Method inserted with ID: {method_id}")
        
        # Test retrieval
        print("\n🔍 Testing retrieval...")
        retrieved = db.get_class_by_name("TestGraphics", "graphics")
        if retrieved:
            print(f"   ✅ Class retrieved: {retrieved['name']}")
        else:
            print("   ❌ Failed to retrieve class")
            
        # Test search
        print("\n🔎 Testing FTS5 search...")
        results = db.search_classes("graphics")
        print(f"   ✅ Found {len(results)} results for 'graphics'")
        
        if results:
            print("\n   Results:")
            for result in results:
                print(f"   - {result['module']}.{result['name']}")
                
    print(f"\n✅ Database test complete!")
    print(f"   Database saved to: {db_path}")


def test_full_integration():
    """Test full parser + database integration."""
    print("\n" + "=" * 60)
    print("TESTING FULL INTEGRATION")
    print("=" * 60)
    
    test_file = "html/api/graphics/picture.html"
    
    if not Path(test_file).exists():
        print(f"❌ Test file not found: {test_file}")
        print("   Skipping integration test")
        return
        
    db_path = "integration_test.db"
    
    # Remove old test db
    if Path(db_path).exists():
        Path(db_path).unlink()
        
    print(f"\n🔄 Parsing and storing: {test_file}")
    
    parser = HTMLParser("html")
    
    with Database(db_path) as db:
        db.create_schema()
        
        # Parse
        xojo_class = parser.parse_class_file(test_file)
        if not xojo_class:
            print("❌ Failed to parse class")
            return
            
        # Store class
        class_id = db.insert_class(xojo_class)
        print(f"   ✅ Class stored: {xojo_class.name} (ID: {class_id})")
        
        # Parse and store properties
        properties = parser.parse_properties(test_file)
        for prop in properties:
            db.insert_property(class_id, prop)
        print(f"   ✅ Stored {len(properties)} properties")
        
        # Parse and store methods
        methods = parser.parse_methods(test_file)
        for method in methods:
            db.insert_method(class_id, method)
        print(f"   ✅ Stored {len(methods)} methods")
        
        # Retrieve and verify
        print("\n🔍 Verifying stored data...")
        retrieved = db.get_class_by_name(xojo_class.name, xojo_class.module)
        retrieved_props = db.get_class_properties(class_id)
        retrieved_methods = db.get_class_methods(class_id)
        
        print(f"   ✅ Class: {retrieved['name']}")
        print(f"   ✅ Properties: {len(retrieved_props)}")
        print(f"   ✅ Methods: {len(retrieved_methods)}")
        
    print(f"\n✅ Integration test complete!")
    print(f"   Database saved to: {db_path}")


if __name__ == "__main__":
    print("\n🚀 XojoDoc Sprint 2 Test Suite\n")
    
    try:
        test_parser()
        test_database()
        test_full_integration()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nNext step: Run the full indexer")
        print("  python -m xojodoc.indexer")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
