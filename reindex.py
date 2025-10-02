"""Script to rebuild the XojoDoc database with all descriptions.

This script creates the database in C:\temp (SSD) for faster performance,
then moves it to the project directory when complete.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from xojodoc.indexer import Indexer, DEFAULT_HTML_ROOT

def main():
    """Rebuild the documentation database."""
    
    # Configuration
    html_root = DEFAULT_HTML_ROOT
    temp_db = r"C:\temp\xojo.db"
    final_db = "xojo.db"
    
    # Ensure temp directory exists
    temp_dir = Path(temp_db).parent
    if not temp_dir.exists():
        print(f"Creating temp directory: {temp_dir}")
        temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Delete temp database if exists
    if os.path.exists(temp_db):
        print(f"Deleting existing temp database: {temp_db}")
        os.remove(temp_db)
    
    # Delete final database if exists
    if os.path.exists(final_db):
        print(f"Deleting existing database: {final_db}")
        os.remove(final_db)
    
    print("\n" + "="*60)
    print("XojoDoc Database Rebuild")
    print("="*60)
    print(f"HTML Root: {html_root}")
    print(f"Temp DB: {temp_db}")
    print(f"Final DB: {final_db}")
    print("="*60 + "\n")
    
    # Create indexer with temp path
    indexer = Indexer(
        html_root=html_root,
        db_path=final_db,
        temp_db_path=temp_db
    )
    
    # Build index (force full reindex)
    indexer.build_index(verbose=True, force=True)
    
    print("\n✓ Reindex complete!")
    print(f"✓ Database location: {final_db}")

if __name__ == "__main__":
    main()
