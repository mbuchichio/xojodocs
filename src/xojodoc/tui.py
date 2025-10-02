"""Interactive TUI for XojoDoc.

Provides a man/less-style interface for browsing Xojo documentation.
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Input, Static, Tree, ListView, ListItem, Label
from textual.binding import Binding
from textual.reactive import reactive
from rich.syntax import Syntax
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from xojodoc.database import Database


class ClassInfo(Static):
    """Widget to display class information."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_data = None
    
    def update_class(self, class_data: dict):
        """Update displayed class information."""
        self.class_data = class_data
        
        # Build rich content
        content = []
        
        # Title
        title = f"{class_data['module']}.{class_data['name']}"
        content.append(f"[bold blue]{title}[/bold blue]\n")
        
        # Description
        if class_data.get('description'):
            content.append("[bold]Description:[/bold]")
            content.append(class_data['description'])
            content.append("")
        
        # Sample code
        if class_data.get('sample_code'):
            content.append("[bold]Example:[/bold]")
            content.append(class_data['sample_code'])
            content.append("")
        
        # Properties
        if class_data.get('properties'):
            content.append(f"[bold]Properties ({len(class_data['properties'])}):[/bold]")
            for name, ptype, desc, read_only, shared in class_data['properties'][:10]:
                flags = []
                if read_only:
                    flags.append("RO")
                if shared:
                    flags.append("Shared")
                flag_str = f" [{', '.join(flags)}]" if flags else ""
                content.append(f"  • [cyan]{name}[/cyan]: {ptype or '?'}{flag_str}")
            
            if len(class_data['properties']) > 10:
                content.append(f"  [dim]... and {len(class_data['properties']) - 10} more[/dim]")
            content.append("")
        
        # Methods
        if class_data.get('methods'):
            content.append(f"[bold]Methods ({len(class_data['methods'])}):[/bold]")
            for name, desc, ret, params, shared, code in class_data['methods'][:10]:
                shared_str = " [Shared]" if shared else ""
                content.append(f"  • [cyan]{name}[/cyan]{params or '()'}{shared_str}")
            
            if len(class_data['methods']) > 10:
                content.append(f"  [dim]... and {len(class_data['methods']) - 10} more[/dim]")
            content.append("")
        
        # Notes
        if class_data.get('notes'):
            content.append("[bold]Notes:[/bold]")
            content.append(class_data['notes'])
            content.append("")
        
        # Compatibility
        if class_data.get('compatibility'):
            content.append(f"[dim]Compatibility: {class_data['compatibility']}[/dim]")
        
        self.update("\n".join(content))


class MethodInfo(Static):
    """Widget to display method information."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method_data = None
    
    def update_method(self, method_data: dict):
        """Update displayed method information."""
        self.method_data = method_data
        
        # Build rich content
        content = []
        
        # Title
        title = f"{method_data['module']}.{method_data['class_name']}.{method_data['name']}"
        content.append(f"[bold blue]{title}[/bold blue]\n")
        
        # Signature
        params = method_data.get('parameters') or "()"
        ret = method_data.get('return_type')
        signature = f"{method_data['name']}{params}"
        if ret:
            signature += f" As {ret}"
        
        content.append("[bold]Signature:[/bold]")
        content.append(f"  {signature}")
        content.append("")
        
        # Shared flag
        if method_data.get('shared'):
            content.append("[yellow]Shared method[/yellow]")
            content.append("")
        
        # Description
        if method_data.get('description'):
            content.append("[bold]Description:[/bold]")
            content.append(method_data['description'])
            content.append("")
        
        # Parameters details
        if method_data.get('parameters'):
            content.append("[bold]Parameters:[/bold]")
            content.append(method_data['parameters'])
            content.append("")
        
        # Return type
        if method_data.get('return_type'):
            content.append(f"[bold]Returns:[/bold] {method_data['return_type']}")
            content.append("")
        
        # Sample code
        if method_data.get('sample_code'):
            content.append("[bold]Example:[/bold]")
            content.append(method_data['sample_code'])
            content.append("")
        
        self.update("\n".join(content))


class SearchResults(ListView):
    """Widget to display search results."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.results = []


class XojoDocTUI(App):
    """Interactive TUI for XojoDoc."""
    
    CSS = """
    Screen {
        layout: horizontal;
    }
    
    #sidebar {
        width: 40;
        border: solid $accent;
        padding: 1;
    }
    
    #content {
        width: 1fr;
        border: solid $accent;
        padding: 1;
    }
    
    #search-box {
        dock: top;
        width: 100%;
        margin-bottom: 1;
    }
    
    #results {
        height: 100%;
        overflow-y: scroll;
    }
    
    .class-item {
        padding: 0 1;
    }
    
    .class-item:hover {
        background: $boost;
    }
    """
    
    TITLE = "XojoDoc - Interactive Documentation Browser"
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("ctrl+c", "quit", "Quit"),
        Binding("/", "focus_search", "Search"),
        Binding("?", "show_help", "Help"),
        Binding("escape", "clear_search", "Clear"),
        Binding("d", "toggle_deprecated", "Toggle Deprecated"),
    ]
    
    current_view = reactive("search")
    
    def __init__(self, db_path: str = "xojo.db"):
        super().__init__()
        self.db = Database(db_path)
        self.current_class = None
        self.current_method = None
        self._search_timer = None  # Timer for debouncing search
        self.hide_deprecated = True  # Hide deprecated classes by default
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        
        with Horizontal():
            # Sidebar with search and results
            with Vertical(id="sidebar"):
                yield Input(
                    placeholder="Search classes...",
                    id="search-box"
                )
                yield ListView(id="results")
            
            # Main content area
            with ScrollableContainer(id="content"):
                yield Static("Welcome to XojoDoc!\n\nPress / to search for classes.\nUse ↑↓ to navigate results.\nPress Enter to view details.", id="main-content")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when app is mounted."""
        # Count total classes
        try:
            with self.db:
                cursor = self.db.conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM classes")
                total_classes = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM classes WHERE module NOT LIKE 'deprecated%'")
                non_deprecated = cursor.fetchone()[0]
                
                # Update welcome message
                content_widget = self.query_one("#main-content", Static)
                content_widget.update(
                    f"Welcome to XojoDoc!\n\n"
                    f"Database contains {total_classes} Xojo classes.\n"
                    f"({non_deprecated} non-deprecated, {total_classes - non_deprecated} deprecated)\n\n"
                    f"Press / to search for classes.\n"
                    f"Press d to toggle deprecated classes (currently {'hidden' if self.hide_deprecated else 'shown'}).\n"
                    f"Scroll through all classes in the sidebar.\n"
                    f"Use ↑↓ to navigate, Enter to view details.\n"
                    f"Press ? for help."
                )
        except Exception:
            pass
        
        # Initial search - show ALL classes
        self.perform_search("")
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes with debouncing."""
        if event.input.id == "search-box":
            # Cancel previous timer if exists
            if self._search_timer is not None:
                self._search_timer.stop()
            
            # Set new timer for 500ms debounce
            query = event.value.strip()
            self._search_timer = self.set_timer(
                0.5,  # 500ms delay
                lambda: self.perform_search(query)
            )
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle search submission."""
        if event.input.id == "search-box":
            # Focus on results list
            results = self.query_one("#results", ListView)
            results.focus()
    
    def perform_search(self, query: str):
        """Perform search and update results."""
        results_widget = self.query_one("#results", ListView)
        results_widget.clear()
        
        try:
            with self.db:
                # Strip whitespace and check if query is meaningful
                query = query.strip()
                
                if query:
                    # FTS5 search
                    results = self.db.search_classes(query)
                    # Limit search results to 100
                    results = results[:100]
                else:
                    # Show ALL classes when no query (sorted alphabetically)
                    cursor = self.db.conn.cursor()
                    cursor.execute("""
                        SELECT id, name, module, description
                        FROM classes
                        ORDER BY name
                    """)
                    results = [dict(row) for row in cursor.fetchall()]
                
                # Filter deprecated classes if hide_deprecated is enabled
                if self.hide_deprecated:
                    results = [r for r in results if not r['module'].startswith('deprecated')]
                
                # Add results to list
                for result in results:
                    class_name = result['name']
                    module = result['module']
                    label = f"{module}.{class_name}"
                    
                    item = ListItem(Label(label))
                    item.class_data = result
                    results_widget.append(item)
                
                if not results:
                    results_widget.append(ListItem(Label("[dim]No results found[/dim]")))
                
                # Show count in notification
                if query:
                    self.notify(f"Found {len(results)} result(s)", timeout=2)
                else:
                    deprecated_note = " (deprecated hidden)" if self.hide_deprecated else ""
                    self.notify(f"Showing all {len(results)} classes{deprecated_note}", timeout=2)
                    
        except Exception as e:
            self.notify(f"Search error: {e}", severity="error")
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle class selection from results."""
        if event.list_view.id == "results":
            item = event.item
            if hasattr(item, 'class_data'):
                self.show_class(item.class_data)
    
    def show_class(self, class_data: dict):
        """Display class details in main content area."""
        try:
            with self.db:
                cursor = self.db.conn.cursor()
                
                # Get full class info
                cursor.execute("""
                    SELECT id, name, module, description, sample_code,
                           compatibility, notes, file_path
                    FROM classes
                    WHERE id = ?
                """, (class_data['id'],))
                
                row = cursor.fetchone()
                if not row:
                    return
                
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
                
                full_data = {
                    'id': class_id,
                    'name': name,
                    'module': module,
                    'description': desc,
                    'sample_code': code,
                    'compatibility': compat,
                    'notes': notes,
                    'properties': properties,
                    'methods': methods
                }
                
                # Update content widget
                content_widget = self.query_one("#main-content", Static)
                
                # Build display text
                lines = []
                lines.append(f"[bold blue]{module}.{name}[/bold blue]\n")
                
                if desc:
                    lines.append("[bold]Description:[/bold]")
                    lines.append(desc)
                    lines.append("")
                
                if code:
                    lines.append("[bold]Example:[/bold]")
                    lines.append(code)
                    lines.append("")
                
                if properties:
                    lines.append(f"[bold]Properties ({len(properties)}):[/bold]")
                    for pname, ptype, pdesc, readonly, shared in properties[:15]:
                        flags = []
                        if readonly:
                            flags.append("RO")
                        if shared:
                            flags.append("Shared")
                        flag_str = f" [{', '.join(flags)}]" if flags else ""
                        lines.append(f"  • [cyan]{pname}[/cyan]: {ptype or '?'}{flag_str}")
                    
                    if len(properties) > 15:
                        lines.append(f"  [dim]... and {len(properties) - 15} more[/dim]")
                    lines.append("")
                
                if methods:
                    lines.append(f"[bold]Methods ({len(methods)}):[/bold]")
                    for mname, mdesc, ret, params, shared, mcode in methods[:15]:
                        shared_str = " [Shared]" if shared else ""
                        lines.append(f"  • [cyan]{mname}[/cyan]{params or '()'}{shared_str}")
                    
                    if len(methods) > 15:
                        lines.append(f"  [dim]... and {len(methods) - 15} more[/dim]")
                    lines.append("")
                
                if notes:
                    lines.append("[bold]Notes:[/bold]")
                    lines.append(notes)
                    lines.append("")
                
                if compat:
                    lines.append(f"[dim]Compatibility: {compat}[/dim]")
                
                content_widget.update("\n".join(lines))
                self.current_class = full_data
                
        except Exception as e:
            self.notify(f"Error loading class: {e}", severity="error")
    
    def action_focus_search(self) -> None:
        """Focus the search box."""
        search_box = self.query_one("#search-box", Input)
        search_box.focus()
    
    def action_clear_search(self) -> None:
        """Clear search and show welcome."""
        search_box = self.query_one("#search-box", Input)
        search_box.value = ""
        search_box.focus()
        
        content_widget = self.query_one("#main-content", Static)
        content_widget.update(
            "Welcome to XojoDoc!\n\n"
            "Press / to search for classes.\n"
            "Use ↑↓ to navigate results.\n"
            "Press Enter to view details.\n"
            "Press ? for help."
        )
    
    def action_toggle_deprecated(self) -> None:
        """Toggle display of deprecated classes."""
        self.hide_deprecated = not self.hide_deprecated
        status = "hidden" if self.hide_deprecated else "shown"
        self.notify(f"Deprecated classes {status}", timeout=2)
        
        # Refresh search results
        search_box = self.query_one("#search-box", Input)
        self.perform_search(search_box.value.strip())
    
    def action_show_help(self) -> None:
        """Show help information."""
        content_widget = self.query_one("#main-content", Static)
        help_text = """[bold blue]XojoDoc Help[/bold blue]

[bold]Keyboard Shortcuts:[/bold]

  /         Focus search box
  ↑ ↓       Navigate search results
  Enter     View selected class
  Escape    Clear search
  d         Toggle deprecated classes
  ?         Show this help
  q         Quit application
  Ctrl+C    Quit application

[bold]Navigation:[/bold]

  1. Type in the search box to find classes
  2. Use arrow keys to select a result
  3. Press Enter to view class details
  4. Scroll through the content with mouse or arrow keys

[bold]Tips:[/bold]

  • Search uses full-text indexing for fast results
  • Searches are case-insensitive
  • Press 'd' to show/hide deprecated classes
  • Empty search shows all classes (alphabetically)
"""
        content_widget.update(help_text)


def main(db_path: str = "xojo.db"):
    """Main entry point for TUI."""
    app = XojoDocTUI(db_path=db_path)
    app.run()


if __name__ == "__main__":
    main()
