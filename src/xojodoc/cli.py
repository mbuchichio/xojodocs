"""CLI module for XojoDoc.

Provides command-line interface for querying Xojo documentation.
"""

import sys
import click
from pathlib import Path
from typing import Optional, List, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.text import Text

from .database import Database


console = Console()


class XojoDocCLI:
    """Command-line interface for XojoDoc."""
    
    def __init__(self, db_path: str = "xojo.db"):
        """Initialize CLI.
        
        Args:
            db_path: Path to SQLite database
        """
        self.db = Database(db_path)
        
        # Check if database exists
        if not Path(db_path).exists():
            console.print("[red]Error: Database not found![/red]")
            console.print(f"Expected location: {db_path}")
            console.print("\nPlease run the indexer first:")
            console.print("  python -m src.xojodoc.indexer")
            sys.exit(1)
    
    def search_classes(self, query: str, limit: int = 10) -> List[Tuple]:
        """Search for classes by name.
        
        Args:
            query: Search query
            limit: Maximum results to return
            
        Returns:
            List of (id, name, module, description) tuples
        """
        with self.db:
            results = self.db.search_classes(query)
            # Convert dict results to tuples and limit
            return [(r['id'], r['name'], r['module'], r['description']) 
                    for r in results[:limit]]
    
    def get_class_info(self, class_name: str) -> Optional[dict]:
        """Get detailed information about a class.
        
        Args:
            class_name: Name of the class
            
        Returns:
            Dictionary with class info or None if not found
        """
        with self.db:
            cursor = self.db.conn.cursor()
            
            # Try exact match first
            cursor.execute("""
                SELECT id, name, module, description, sample_code, 
                       compatibility, notes, file_path
                FROM classes 
                WHERE name = ? COLLATE NOCASE
            """, (class_name,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            class_id, name, module, desc, code, compat, notes, path = row
            
            # Get properties
            cursor.execute("""
                SELECT name, type, description, read_only, shared
                FROM properties
                WHERE class_id = ?
                ORDER BY name
            """, (class_id,))
            properties = cursor.fetchall()
            
            # Get methods
            cursor.execute("""
                SELECT name, description, return_type, parameters, shared, sample_code
                FROM methods
                WHERE class_id = ?
                ORDER BY name
            """, (class_id,))
            methods = cursor.fetchall()
            
            return {
                'id': class_id,
                'name': name,
                'module': module,
                'description': desc,
                'sample_code': code,
                'compatibility': compat,
                'notes': notes,
                'file_path': path,
                'properties': properties,
                'methods': methods
            }
    
    def get_method_info(self, class_name: str, method_name: str) -> Optional[dict]:
        """Get detailed information about a method.
        
        Args:
            class_name: Name of the class
            method_name: Name of the method
            
        Returns:
            Dictionary with method info or None if not found
        """
        with self.db:
            cursor = self.db.conn.cursor()
            
            # Find the class first
            cursor.execute("""
                SELECT id, name, module FROM classes 
                WHERE name = ? COLLATE NOCASE
            """, (class_name,))
            
            class_row = cursor.fetchone()
            if not class_row:
                return None
            
            class_id, class_name_actual, module = class_row
            
            # Find the method
            cursor.execute("""
                SELECT name, description, return_type, parameters, sample_code, shared
                FROM methods
                WHERE class_id = ? AND name = ? COLLATE NOCASE
            """, (class_id, method_name))
            
            method_row = cursor.fetchone()
            if not method_row:
                return None
            
            name, desc, ret, params, code, shared = method_row
            
            return {
                'class_name': class_name_actual,
                'module': module,
                'name': name,
                'description': desc,
                'return_type': ret,
                'parameters': params,
                'sample_code': code,
                'shared': shared
            }
    
    def display_class(self, class_info: dict, show_all: bool = False):
        """Display class information.
        
        Args:
            class_info: Dictionary with class information
            show_all: Show all properties and methods
        """
        # Header
        title = f"{class_info['module']}.{class_info['name']}"
        console.print(Panel(title, style="bold blue", expand=False))
        console.print()
        
        # Description
        if class_info['description']:
            console.print("[bold]Description:[/bold]")
            console.print(class_info['description'])
            console.print()
        
        # Sample code
        if class_info['sample_code']:
            console.print("[bold]Example:[/bold]")
            console.print(Panel(class_info['sample_code'], border_style="green"))
            console.print()
        
        # Properties
        if class_info['properties']:
            console.print(f"[bold]Properties ({len(class_info['properties'])}):[/bold]")
            
            prop_table = Table(show_header=True, header_style="bold cyan")
            prop_table.add_column("Name", style="cyan")
            prop_table.add_column("Type", style="yellow")
            prop_table.add_column("Flags", style="magenta")
            
            props_to_show = class_info['properties'] if show_all else class_info['properties'][:5]
            
            for name, ptype, desc, read_only, shared in props_to_show:
                flags = []
                if read_only:
                    flags.append("RO")
                if shared:
                    flags.append("Shared")
                flag_str = ", ".join(flags) if flags else "-"
                prop_table.add_row(name, ptype or "?", flag_str)
            
            console.print(prop_table)
            
            if not show_all and len(class_info['properties']) > 5:
                console.print(f"[dim]... and {len(class_info['properties']) - 5} more[/dim]")
            
            console.print()
        
        # Methods
        if class_info['methods']:
            console.print(f"[bold]Methods ({len(class_info['methods'])}):[/bold]")
            
            method_table = Table(show_header=True, header_style="bold cyan")
            method_table.add_column("Name", style="cyan")
            method_table.add_column("Parameters", style="yellow", overflow="fold")
            method_table.add_column("Returns", style="green")
            method_table.add_column("Shared", style="magenta")
            
            methods_to_show = class_info['methods'] if show_all else class_info['methods'][:5]
            
            for name, desc, ret, params, shared, code in methods_to_show:
                shared_str = "Yes" if shared else ""
                ret_str = ret or "void"
                params_str = params if params else "()"
                method_table.add_row(name, params_str, ret_str, shared_str)
            
            console.print(method_table)
            
            if not show_all and len(class_info['methods']) > 5:
                console.print(f"[dim]... and {len(class_info['methods']) - 5} more[/dim]")
            
            console.print()
        
        # Notes
        if class_info['notes']:
            console.print("[bold]Notes:[/bold]")
            console.print(class_info['notes'])
            console.print()
        
        # Compatibility
        if class_info['compatibility']:
            console.print(f"[dim]Compatibility: {class_info['compatibility']}[/dim]")
    
    def display_method(self, method_info: dict):
        """Display method information.
        
        Args:
            method_info: Dictionary with method information
        """
        # Header
        title = f"{method_info['module']}.{method_info['class_name']}.{method_info['name']}"
        console.print(Panel(title, style="bold blue", expand=False))
        console.print()
        
        # Signature (constructed from parameters and return type)
        params = method_info['parameters'] or "()"
        ret = method_info['return_type']
        signature = f"{method_info['name']}{params}"
        if ret:
            signature += f" As {ret}"
        
        console.print("[bold]Signature:[/bold]")
        console.print(f"  {signature}")
        console.print()
        
        # Shared flag
        if method_info.get('shared'):
            console.print("[yellow]Shared method[/yellow]")
            console.print()
        
        # Description
        if method_info['description']:
            console.print("[bold]Description:[/bold]")
            console.print(method_info['description'])
            console.print()
        
        # Parameters details
        if method_info['parameters']:
            console.print("[bold]Parameters:[/bold]")
            console.print(method_info['parameters'])
            console.print()
        
        # Return type
        if method_info['return_type']:
            console.print(f"[bold]Returns:[/bold] {method_info['return_type']}")
            console.print()
        
        # Sample code
        if method_info['sample_code']:
            console.print("[bold]Example:[/bold]")
            console.print(Panel(method_info['sample_code'], border_style="green"))
            console.print()
    
    def display_search_results(self, results: List[Tuple]):
        """Display search results.
        
        Args:
            results: List of (id, name, module, description) tuples
        """
        if not results:
            console.print("[yellow]No results found.[/yellow]")
            return
        
        console.print(f"[bold]Found {len(results)} result(s):[/bold]\n")
        
        for idx, (class_id, name, module, desc) in enumerate(results, 1):
            console.print(f"[cyan]{idx}. {module}.{name}[/cyan]")
            if desc:
                # Truncate long descriptions
                short_desc = desc[:100] + "..." if len(desc) > 100 else desc
                console.print(f"   {short_desc}")
            console.print()


@click.group(invoke_without_command=True)
@click.option('--db-path', default='xojo.db', help='Path to database')
@click.pass_context
def main(ctx, db_path):
    """XojoDoc - CLI Documentation System for Xojo.
    
    Query Xojo documentation from the command line.
    
    Examples:
        xojodoc search Graphics
        xojodoc class Graphics
        xojodoc method Graphics DrawString
    """
    ctx.ensure_object(dict)
    ctx.obj['CLI'] = XojoDocCLI(db_path)
    
    # If no command, show help
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())


@main.command()
@click.argument('query')
@click.option('--limit', '-n', default=10, help='Maximum results to show')
@click.pass_context
def search(ctx, query, limit):
    """Search for classes by name.
    
    Example: xojodoc search Graphics
    """
    cli = ctx.obj['CLI']
    results = cli.search_classes(query, limit)
    cli.display_search_results(results)


@main.command()
@click.argument('class_name')
@click.option('--all', '-a', is_flag=True, help='Show all properties and methods')
@click.pass_context
def cls(ctx, class_name, all):
    """Show detailed information about a class.
    
    Example: xojodoc class Graphics
    """
    cli = ctx.obj['CLI']
    class_info = cli.get_class_info(class_name)
    
    if not class_info:
        console.print(f"[red]Class '{class_name}' not found.[/red]")
        console.print("\nTry searching:")
        console.print(f"  xojodoc search {class_name}")
        sys.exit(1)
    
    cli.display_class(class_info, show_all=all)


@main.command()
@click.argument('class_name')
@click.argument('method_name')
@click.pass_context
def method(ctx, class_name, method_name):
    """Show detailed information about a method.
    
    Example: xojodoc method Graphics DrawString
    """
    cli = ctx.obj['CLI']
    method_info = cli.get_method_info(class_name, method_name)
    
    if not method_info:
        console.print(f"[red]Method '{class_name}.{method_name}' not found.[/red]")
        console.print("\nTry showing the class:")
        console.print(f"  xojodoc class {class_name}")
        sys.exit(1)
    
    cli.display_method(method_info)


if __name__ == "__main__":
    main()
