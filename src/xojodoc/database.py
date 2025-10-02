"""Database management for XojoDoc.

Handles SQLite database creation, schema management, and data storage.
"""

import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class XojoClass:
    """Represents a Xojo class."""
    name: str
    module: str
    description: str
    sample_code: Optional[str] = None
    compatibility: Optional[str] = None
    notes: Optional[str] = None
    file_path: Optional[str] = None


@dataclass
class XojoProperty:
    """Represents a class property."""
    name: str
    type: str
    read_only: bool = False
    shared: bool = False
    description: Optional[str] = None


@dataclass
class XojoMethod:
    """Represents a class method."""
    name: str
    parameters: Optional[str] = None
    return_type: Optional[str] = None
    shared: bool = False
    description: Optional[str] = None
    sample_code: Optional[str] = None


class Database:
    """Manages the SQLite database for XojoDoc."""

    def __init__(self, db_path: str = "xojo.db"):
        """Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.conn: Optional[sqlite3.Connection] = None
        
    def connect(self) -> None:
        """Connect to the database."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
    def close(self) -> None:
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            
    def create_schema(self) -> None:
        """Create database schema."""
        if not self.conn:
            raise RuntimeError("Database not connected")
            
        cursor = self.conn.cursor()
        
        # Classes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                module TEXT NOT NULL,
                description TEXT,
                sample_code TEXT,
                compatibility TEXT,
                notes TEXT,
                file_path TEXT,
                file_mtime REAL,
                indexed_at REAL,
                UNIQUE(module, name)
            )
        """)
        
        # Properties table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                type TEXT,
                read_only BOOLEAN DEFAULT 0,
                shared BOOLEAN DEFAULT 0,
                description TEXT,
                FOREIGN KEY(class_id) REFERENCES classes(id) ON DELETE CASCADE
            )
        """)
        
        # Methods table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS methods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                parameters TEXT,
                return_type TEXT,
                shared BOOLEAN DEFAULT 0,
                description TEXT,
                sample_code TEXT,
                FOREIGN KEY(class_id) REFERENCES classes(id) ON DELETE CASCADE
            )
        """)
        
        # Create indexes for better search performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_classes_name 
            ON classes(name)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_classes_module 
            ON classes(module)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_properties_name 
            ON properties(name)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_methods_name 
            ON methods(name)
        """)
        
        # Full-text search virtual table
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS search_index USING fts5(
                class_name,
                module,
                description,
                content
            )
        """)
        
        self.conn.commit()
        
    def insert_class(self, xojo_class: XojoClass, file_mtime: Optional[float] = None) -> int:
        """Insert a class into the database.
        
        Args:
            xojo_class: XojoClass object to insert
            file_mtime: File modification time (Unix timestamp)
            
        Returns:
            ID of inserted class
        """
        if not self.conn:
            raise RuntimeError("Database not connected")
            
        import time
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO classes 
            (name, module, description, sample_code, compatibility, notes, file_path, file_mtime, indexed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            xojo_class.name,
            xojo_class.module,
            xojo_class.description,
            xojo_class.sample_code,
            xojo_class.compatibility,
            xojo_class.notes,
            xojo_class.file_path,
            file_mtime,
            time.time()
        ))
        
        class_id = cursor.lastrowid
        
        # Update FTS index
        cursor.execute("""
            INSERT INTO search_index (class_name, module, description, content)
            VALUES (?, ?, ?, ?)
        """, (
            xojo_class.name,
            xojo_class.module,
            xojo_class.description or "",
            f"{xojo_class.name} {xojo_class.module} {xojo_class.description or ''}"
        ))
        
        self.conn.commit()
        return class_id
        
    def insert_property(self, class_id: int, prop: XojoProperty) -> int:
        """Insert a property into the database.
        
        Args:
            class_id: ID of the class this property belongs to
            prop: XojoProperty object to insert
            
        Returns:
            ID of inserted property
        """
        if not self.conn:
            raise RuntimeError("Database not connected")
            
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO properties 
            (class_id, name, type, read_only, shared, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            class_id,
            prop.name,
            prop.type,
            prop.read_only,
            prop.shared,
            prop.description
        ))
        
        self.conn.commit()
        return cursor.lastrowid
        
    def insert_method(self, class_id: int, method: XojoMethod) -> int:
        """Insert a method into the database.
        
        Args:
            class_id: ID of the class this method belongs to
            method: XojoMethod object to insert
            
        Returns:
            ID of inserted method
        """
        if not self.conn:
            raise RuntimeError("Database not connected")
            
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO methods 
            (class_id, name, parameters, return_type, shared, description, sample_code)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            class_id,
            method.name,
            method.parameters,
            method.return_type,
            method.shared,
            method.description,
            method.sample_code
        ))
        
        self.conn.commit()
        return cursor.lastrowid
        
    def search_classes(self, query: str) -> List[Dict[str, Any]]:
        """Search classes using FTS5 with prefix matching.
        
        Args:
            query: Search query (supports module.class format or free text with prefix matching)
            
        Returns:
            List of matching classes
        """
        if not self.conn:
            raise RuntimeError("Database not connected")
            
        cursor = self.conn.cursor()
        
        # Strip and validate query
        query = query.strip()
        if not query:
            return []
        
        # Check if query is in module.class format (e.g., "Desktop.Window")
        if '.' in query and query.count('.') == 1:
            parts = query.split('.')
            module_part = parts[0].strip()
            class_part = parts[1].strip()
            
            if module_part and class_part:
                # Direct search for module.class combination
                cursor.execute("""
                    SELECT id, name, module, description
                    FROM classes
                    WHERE (module LIKE ? OR LOWER(module) LIKE ?)
                      AND (name LIKE ? OR LOWER(name) LIKE ?)
                    ORDER BY name, module
                """, (f'%{module_part}%', f'%{module_part.lower()}%',
                      f'{class_part}%', f'{class_part.lower()}%'))
                
                results = [dict(row) for row in cursor.fetchall()]
                if results:
                    return results
                # If no direct match, fall through to FTS5 search
        
        # Regular FTS5 search
        import re
        # Remove or replace problematic characters for FTS5
        clean_query = re.sub(r'[^\w\s*]', ' ', query)
        
        # Add prefix matching support if query doesn't already have *
        if '*' not in clean_query:
            terms = clean_query.strip().split()
            if not terms:
                return []
            # Add * to each term for prefix matching
            fts_query = ' '.join(f'{term}*' for term in terms if term)
        else:
            fts_query = clean_query
        
        try:
            cursor.execute("""
                SELECT DISTINCT c.id, c.name, c.module, c.description
                FROM search_index s
                JOIN classes c ON c.name = s.class_name AND c.module = s.module
                WHERE search_index MATCH ?
                ORDER BY c.name, c.module
            """, (fts_query,))
            
            return [dict(row) for row in cursor.fetchall()]
        except Exception:
            # If FTS5 query fails, return empty results
            return []
        
    def get_class_by_name(self, name: str, module: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get a class by name.
        
        Args:
            name: Class name
            module: Optional module name to narrow search
            
        Returns:
            Class data or None if not found
        """
        if not self.conn:
            raise RuntimeError("Database not connected")
            
        cursor = self.conn.cursor()
        
        if module:
            cursor.execute("""
                SELECT * FROM classes WHERE name = ? AND module = ?
            """, (name, module))
        else:
            cursor.execute("""
                SELECT * FROM classes WHERE name = ?
            """, (name,))
            
        row = cursor.fetchone()
        return dict(row) if row else None
        
    def get_class_properties(self, class_id: int) -> List[Dict[str, Any]]:
        """Get all properties for a class.
        
        Args:
            class_id: Class ID
            
        Returns:
            List of properties
        """
        if not self.conn:
            raise RuntimeError("Database not connected")
            
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM properties WHERE class_id = ? ORDER BY name
        """, (class_id,))
        
        return [dict(row) for row in cursor.fetchall()]
        
    def get_class_methods(self, class_id: int) -> List[Dict[str, Any]]:
        """Get all methods for a class.
        
        Args:
            class_id: Class ID
            
        Returns:
            List of methods
        """
        if not self.conn:
            raise RuntimeError("Database not connected")
            
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM methods WHERE class_id = ? ORDER BY name
        """, (class_id,))
        
        return [dict(row) for row in cursor.fetchall()]
        
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
        
    def needs_reindex(self, file_path: str, file_mtime: float) -> bool:
        """Check if a file needs to be reindexed.
        
        Args:
            file_path: Path to the file
            file_mtime: Current file modification time
            
        Returns:
            True if file needs reindexing
        """
        if not self.conn:
            raise RuntimeError("Database not connected")
            
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT file_mtime FROM classes WHERE file_path = ?
        """, (file_path,))
        
        row = cursor.fetchone()
        
        # Need to index if not found or mtime changed
        if not row:
            return True
            
        stored_mtime = row[0]
        if stored_mtime is None:
            return True
            
        return file_mtime > stored_mtime
        
    def delete_class_by_path(self, file_path: str) -> None:
        """Delete a class and its related data by file path.
        
        Args:
            file_path: Path to the file
        """
        if not self.conn:
            raise RuntimeError("Database not connected")
            
        cursor = self.conn.cursor()
        
        # Get class ID
        cursor.execute("SELECT id FROM classes WHERE file_path = ?", (file_path,))
        row = cursor.fetchone()
        
        if row:
            class_id = row[0]
            
            # Delete methods and properties (cascade should handle this, but being explicit)
            cursor.execute("DELETE FROM methods WHERE class_id = ?", (class_id,))
            cursor.execute("DELETE FROM properties WHERE class_id = ?", (class_id,))
            
            # Delete class
            cursor.execute("DELETE FROM classes WHERE id = ?", (class_id,))
            
            self.conn.commit()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
