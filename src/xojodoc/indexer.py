"""Indexer module for building the documentation database.

Coordinates parsing and storage of Xojo documentation.
"""

from pathlib import Path
from typing import Optional
from .parser import HTMLParser
from .database import Database


class Indexer:
    """Indexes Xojo documentation into database."""

    def __init__(self, html_root: str = "html", db_path: str = "xojo.db"):
        """Initialize indexer.
        
        Args:
            html_root: Root directory containing HTML documentation
            db_path: Path to SQLite database
        """
        self.parser = HTMLParser(html_root)
        self.db = Database(db_path)
        
    def build_index(self, verbose: bool = True) -> None:
        """Build complete documentation index.
        
        Args:
            verbose: Print progress information
        """
        with self.db:
            # Create schema
            if verbose:
                print("Creating database schema...")
            self.db.create_schema()
            
            # Discover all classes
            if verbose:
                print("Discovering classes...")
            classes = self.parser.discover_classes()
            
            if verbose:
                print(f"Found {len(classes)} classes to index")
                
            # Parse and store each class
            for idx, (module, file_path) in enumerate(classes, 1):
                if verbose:
                    class_name = Path(file_path).stem
                    print(f"[{idx}/{len(classes)}] Indexing {module}.{class_name}...")
                    
                try:
                    # Parse class
                    xojo_class = self.parser.parse_class_file(file_path)
                    if not xojo_class:
                        if verbose:
                            print(f"  ⚠ Skipped (no data found)")
                        continue
                        
                    # Insert class
                    class_id = self.db.insert_class(xojo_class)
                    
                    # Parse and insert properties
                    properties = self.parser.parse_properties(file_path)
                    for prop in properties:
                        self.db.insert_property(class_id, prop)
                        
                    # Parse and insert methods
                    methods = self.parser.parse_methods(file_path)
                    for method in methods:
                        self.db.insert_method(class_id, method)
                        
                    if verbose:
                        print(f"  ✓ Indexed: {len(properties)} properties, {len(methods)} methods")
                        
                except Exception as e:
                    if verbose:
                        print(f"  ✗ Error: {e}")
                    continue
                    
            if verbose:
                print(f"\n✓ Indexing complete! Database: {self.db.db_path}")
                
    def update_class(self, module: str, class_name: str, verbose: bool = True) -> bool:
        """Update a single class in the index.
        
        Args:
            module: Module name
            class_name: Class name
            verbose: Print progress information
            
        Returns:
            True if successful, False otherwise
        """
        # Find the file
        file_path = self.parser.api_root / module / f"{class_name.lower()}.html"
        
        if not file_path.exists():
            if verbose:
                print(f"✗ File not found: {file_path}")
            return False
            
        with self.db:
            try:
                if verbose:
                    print(f"Updating {module}.{class_name}...")
                    
                # Parse class
                xojo_class = self.parser.parse_class_file(str(file_path))
                if not xojo_class:
                    if verbose:
                        print(f"  ⚠ No data found")
                    return False
                    
                # Insert/update class
                class_id = self.db.insert_class(xojo_class)
                
                # Parse and insert properties
                properties = self.parser.parse_properties(str(file_path))
                for prop in properties:
                    self.db.insert_property(class_id, prop)
                    
                # Parse and insert methods
                methods = self.parser.parse_methods(str(file_path))
                for method in methods:
                    self.db.insert_method(class_id, method)
                    
                if verbose:
                    print(f"  ✓ Updated: {len(properties)} properties, {len(methods)} methods")
                    
                return True
                
            except Exception as e:
                if verbose:
                    print(f"  ✗ Error: {e}")
                return False


def main():
    """Main entry point for indexer."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build XojoDoc documentation index")
    parser.add_argument(
        "--html-root",
        default="html",
        help="Root directory containing HTML documentation (default: html)"
    )
    parser.add_argument(
        "--db-path",
        default="xojo.db",
        help="Path to SQLite database (default: xojo.db)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output"
    )
    
    args = parser.parse_args()
    
    indexer = Indexer(html_root=args.html_root, db_path=args.db_path)
    indexer.build_index(verbose=not args.quiet)


if __name__ == "__main__":
    main()
