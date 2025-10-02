"""Configuration module for XojoDoc.

Reads configuration from xojodoc.conf file.
Auto-generates template if not found.
Falls back to sensible defaults if config file not found.
"""

import os
import sys
from pathlib import Path
from typing import Optional
import configparser


# Template configuration content
CONFIG_TEMPLATE = """# XojoDoc Configuration File
# 
# Edit the path below to match your Xojo installation.
# This file should be in the same directory as xojodoc.

[paths]
# Path to Xojo HTML documentation
# 
# Windows default:
html_root = C:\\Program Files\\Xojo\\Xojo 2025r2.1\\Xojo Resources\\Language Reference\\html

# Database file (created in same directory as this config)
database = xojo.db
"""


class Config:
    """Configuration handler for XojoDoc."""
    
    # Default values
    DEFAULT_HTML_ROOT = r"C:\Program Files\Xojo\Xojo 2025r2.1\Xojo Resources\Language Reference\html"
    DEFAULT_DATABASE = "xojo.db"
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_file: Path to config file. If None, searches in standard locations.
        """
        self.config_file = self._find_config_file(config_file)
        
        # If no config file found, create one in current directory
        if not self.config_file:
            self.config_file = self._create_default_config()
        
        self._load_config()
    
    def _find_config_file(self, config_file: Optional[str]) -> Optional[Path]:
        """Find configuration file.
        
        Search order:
        1. Provided config_file parameter
        2. xojodoc.conf in executable/script directory
        
        Args:
            config_file: Explicit config file path
            
        Returns:
            Path to config file, or None if not found
        """
        if config_file:
            path = Path(config_file)
            if path.exists():
                return path
        
        # Next to executable/script
        if getattr(sys, 'frozen', False):
            # Running as exe
            exe_dir = Path(sys.executable).parent
        else:
            # Running as script
            exe_dir = Path(__file__).parent.parent
        
        path = exe_dir / "xojodoc.conf"
        if path.exists():
            return path
        
        return None
    
    def _create_default_config(self) -> Path:
        """Create default configuration file in application directory.
        
        Returns:
            Path to created config file
        """
        # Determine where to create config
        if getattr(sys, 'frozen', False):
            # Running as exe - create next to exe
            config_dir = Path(sys.executable).parent
        else:
            # Running as script - create in project root
            config_dir = Path(__file__).parent.parent
        
        config_path = config_dir / "xojodoc.conf"
        
        print("\n" + "="*60)
        print("WARNING: Configuration file not found!")
        print("="*60)
        print(f"Creating: {config_path.absolute()}")
        print()
        print("EDIT xojodoc.conf to set your Xojo installation path")
        print()
        print("   Default: C:\\Program Files\\Xojo\\Xojo 2025r2.1\\...")
        print("="*60 + "\n")
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(CONFIG_TEMPLATE)
            print(f"Created: {config_path.absolute()}\n")
        except Exception as e:
            print(f"Error: {e}")
            print("  Using defaults.\n")
            return None
        
        return config_path
    
    def _load_config(self):
        """Load configuration from file or use defaults."""
        self.html_root = self.DEFAULT_HTML_ROOT
        self.database = self.DEFAULT_DATABASE
        
        if not self.config_file:
            return
        
        try:
            parser = configparser.ConfigParser()
            parser.read(self.config_file, encoding='utf-8')
            
            if 'paths' in parser:
                self.html_root = parser['paths'].get('html_root', self.DEFAULT_HTML_ROOT).strip()
                self.database = parser['paths'].get('database', self.DEFAULT_DATABASE).strip()
                
        except Exception as e:
            print(f"Warning: Could not read {self.config_file}: {e}")
            print("Using defaults.")
    
    def get_html_root(self) -> str:
        """Get HTML documentation root path."""
        return self.html_root
    
    def get_database_path(self) -> str:
        """Get database path."""
        return self.database
    
    def __repr__(self) -> str:
        """String representation."""
        return (f"Config(html_root={self.html_root}, "
                f"database={self.database})")


# Global config instance
_config = None


def get_config() -> Config:
    """Get global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config


if __name__ == "__main__":
    # Test configuration loading
    config = Config()
    print(f"Configuration:")
    print(f"  Config file: {config.config_file or 'Not found (using defaults)'}")
    print(f"  HTML root:   {config.get_html_root()}")
    print(f"  Database:    {config.get_database_path()}")
