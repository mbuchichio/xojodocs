"""Script to rebuild the XojoDoc database.

DEPRECATED: Use 'xojodoc --reindex' instead.

This script is kept for backwards compatibility and simply
calls the CLI with --reindex flag.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from xojodoc.cli import main as cli_main

if __name__ == "__main__":
    print("Note: 'python reindex.py' is deprecated.")
    print("      Use 'xojodoc --reindex' instead.\n")
    
    # Call CLI with --reindex
    sys.argv = ['xojodoc', '--reindex']
    cli_main()
