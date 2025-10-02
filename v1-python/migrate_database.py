"""Database migration script to add incremental indexing support.

Adds file_mtime and indexed_at columns to the classes table.
"""

import sqlite3
import sys


def migrate_database(db_path: str = "xojo.db"):
    """Migrate database to add incremental indexing columns."""
    
    print(f"🔧 Migrating database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(classes)")
        columns = [row[1] for row in cursor.fetchall()]
        
        needs_migration = False
        
        if 'file_mtime' not in columns:
            print("   Adding file_mtime column...")
            cursor.execute("ALTER TABLE classes ADD COLUMN file_mtime REAL")
            needs_migration = True
            
        if 'indexed_at' not in columns:
            print("   Adding indexed_at column...")
            cursor.execute("ALTER TABLE classes ADD COLUMN indexed_at REAL")
            needs_migration = True
            
        if needs_migration:
            conn.commit()
            print("✅ Migration complete!")
            print()
            print("💡 Note: Existing entries have NULL timestamps.")
            print("   Run indexer with --force to populate timestamps:")
            print("   py -m src.xojodoc.indexer --force")
        else:
            print("✅ Database already up to date!")
            
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False


if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else "xojo.db"
    success = migrate_database(db_path)
    sys.exit(0 if success else 1)
