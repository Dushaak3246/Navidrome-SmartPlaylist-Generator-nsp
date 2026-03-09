#!/usr/bin/env python3
"""
Navidrome Smart Playlist Creator
A CLI tool to create .nsp files for Navidrome smart playlists
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# Try to import rich for better UI, fall back to basic if not available
try:
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    from rich.panel import Panel
    from rich.table import Table
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Note: Install 'rich' for better UI experience: pip install rich")

class SmartPlaylistCreator:
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.config_file = Path.home() / ".navidrome_playlist_config.json"
        self.playlist_dir = self.load_config()
        
        # Field definitions with types
        self.fields = {
            "String Fields": [
                "title", "album", "artist", "albumartist", "genre", "composer",
                "comment", "lyrics", "filepath", "filetype", "grouping",
                "discsubtitle", "albumtype", "albumcomment", "catalognumber"
            ],
            "Numeric Fields": [
                "year", "tracknumber", "discnumber", "size", "duration",
                "bitrate", "bitdepth", "bpm", "channels", "playcount", "rating",
                "library_id"
            ],
            "Boolean Fields": [
                "loved", "hascoverart", "compilation"
            ],
            "Date Fields": [
                "date", "originaldate", "releasedate", "dateadded",
                "datemodified", "dateloved", "lastplayed", "daterated"
            ]
        }
        
        self.operators = {
            "String": ["is", "isNot", "contains", "notContains", "startsWith", "endsWith"],
            "Numeric": ["is", "isNot", "gt", "lt", "inTheRange"],
            "Boolean": ["is"],
            "Date": ["is", "isNot", "before", "after", "inTheRange", "inTheLast", "notInTheLast"]
        }
        
        self.sort_fields = [
            "title", "album", "artist", "year", "dateadded", "lastplayed",
            "playcount", "rating", "random", "duration", "bitrate"
        ]

    def print(self, text: str, style: str = ""):
        """Print with or without rich formatting"""
        if RICH_AVAILABLE and self.console:
            self.console.print(text, style=style)
        else:
            print(text)

    def print_panel(self, text: str, title: str = ""):
        """Print a panel (box) around text"""
        if RICH_AVAILABLE and self.console:
            self.console.print(Panel(text, title=title, border_style="cyan"))
        else:
            print(f"\n{'='*60}")
            if title:
                print(f" {title}")
                print('='*60)
            print(text)
            print('='*60 + "\n")

    def prompt(self, question: str, default: str = "") -> str:
        """Prompt for input"""
        if RICH_AVAILABLE:
            return Prompt.ask(question, default=default)
        else:
            response = input(f"{question} [{default}]: " if default else f"{question}: ")
            return response if response else default

    def confirm(self, question: str, default: bool = True) -> bool:
        """Confirm yes/no"""
        if RICH_AVAILABLE:
            return Confirm.ask(question, default=default)
        else:
            default_str = "Y/n" if default else "y/N"
            response = input(f"{question} [{default_str}]: ").strip().lower()
            if not response:
                return default
            return response in ['y', 'yes']

    def load_config(self) -> Optional[Path]:
        """Load saved playlist directory from config"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return Path(config.get('playlist_directory', ''))
            except:
                return None
        return None

    def save_config(self, playlist_dir: Path):
        """Save playlist directory to config"""
        with open(self.config_file, 'w') as f:
            json.dump({'playlist_directory': str(playlist_dir)}, f)

    def set_playlist_directory(self):
        """Set or update the playlist directory"""
        self.print_panel(
            "Configure Smart Playlist Directory\n\n"
            "This is where your .nsp files will be saved.\n"
            "Example: /srv/.../Navidrome/SmartPlaylists",
            title="Directory Configuration"
        )
        
        if self.playlist_dir:
            self.print(f"\n[cyan]Current directory:[/cyan] {self.playlist_dir}", style="bold")
            if not self.confirm("Change directory?", default=False):
                return
        
        while True:
            dir_path = self.prompt("\nEnter playlist directory path")
            if not dir_path:
                self.print("[red]Directory path cannot be empty![/red]", style="bold")
                continue
            
            path = Path(dir_path).expanduser()
            
            if not path.exists():
                if self.confirm(f"Directory doesn't exist. Create it?", default=True):
                    try:
                        path.mkdir(parents=True, exist_ok=True)
                        self.print(f"[green]✓ Created directory: {path}[/green]", style="bold")
                    except Exception as e:
                        self.print(f"[red]✗ Error creating directory: {e}[/red]", style="bold")
                        continue
                else:
                    continue
            
            if not path.is_dir():
                self.print("[red]Path exists but is not a directory![/red]", style="bold")
                continue
            
            self.playlist_dir = path
            self.save_config(path)
            self.print(f"[green]✓ Playlist directory set to: {path}[/green]", style="bold")
            break

    def show_field_reference(self):
        """Show available fields"""
        if RICH_AVAILABLE:
            table = Table(title="Available Fields", show_header=True, header_style="bold magenta")
            table.add_column("Category", style="cyan")
            table.add_column("Fields", style="white")
            
            for category, fields in self.fields.items():
                table.add_row(category, ", ".join(fields))
            
            self.console.print(table)
        else:
            print("\n" + "="*60)
            print("AVAILABLE FIELDS")
            print("="*60)
            for category, fields in self.fields.items():
                print(f"\n{category}:")
                print(", ".join(fields))
            print("="*60 + "\n")

    def show_operator_reference(self):
        """Show available operators"""
        if RICH_AVAILABLE:
            table = Table(title="Available Operators", show_header=True, header_style="bold magenta")
            table.add_column("Field Type", style="cyan")
            table.add_column("Operators", style="white")
            
            for field_type, ops in self.operators.items():
                table.add_row(field_type, ", ".join(ops))
            
            self.console.print(table)
        else:
            print("\n" + "="*60)
            print("AVAILABLE OPERATORS")
            print("="*60)
            for field_type, ops in self.operators.items():
                print(f"\n{field_type} Fields:")
                print(", ".join(ops))
            print("="*60 + "\n")

    def get_field_type(self, field: str) -> str:
        """Determine field type"""
        for category, fields in self.fields.items():
            if field in fields:
                if "String" in category:
                    return "String"
                elif "Numeric" in category:
                    return "Numeric"
                elif "Boolean" in category:
                    return "Boolean"
                elif "Date" in category:
                    return "Date"
        return "String"  # Default

    def create_condition(self) -> Optional[Dict[str, Any]]:
        """Create a single condition interactively"""
        self.print("\n[cyan]═══ Creating New Condition ═══[/cyan]", style="bold")
        
        if self.confirm("View available fields?", default=False):
            self.show_field_reference()
        
        field = self.prompt("\nEnter field name (e.g., 'loved', 'year', 'genre')").strip()
        if not field:
            return None
        
        field_type = self.get_field_type(field)
        self.print(f"[yellow]Field type detected: {field_type}[/yellow]", style="dim")
        
        if self.confirm("View available operators?", default=False):
            self.show_operator_reference()
        
        available_ops = self.operators.get(field_type, self.operators["String"])
        self.print(f"[yellow]Available operators: {', '.join(available_ops)}[/yellow]", style="dim")
        
        operator = self.prompt("Enter operator (e.g., 'is', 'gt', 'contains')").strip()
        if not operator:
            return None
        
        # Get value based on operator and field type
        if operator in ["inTheRange"]:
            self.print("[yellow]Enter range as two values (e.g., '1980 1990' or '2024-01-01 2024-12-31')[/yellow]")
            value_str = self.prompt("Value")
            try:
                parts = value_str.split()
                if field_type == "Numeric":
                    value = [int(p) for p in parts]
                else:
                    value = parts
            except:
                value = value_str.split()
        elif operator in ["inTheLast", "notInTheLast"]:
            value = int(self.prompt("Number of days"))
        elif field_type == "Boolean":
            value = self.confirm("Value", default=True)
        elif field_type == "Numeric":
            value = int(self.prompt("Value"))
        else:
            value = self.prompt("Value")
        
        return {operator: {field: value}}

    def create_condition_group(self) -> List[Dict[str, Any]]:
        """Create a group of conditions (with ANY or ALL logic)"""
        conditions = []
        
        while True:
            condition = self.create_condition()
            if condition:
                conditions.append(condition)
                self.print(f"[green]✓ Condition added: {json.dumps(condition)}[/green]", style="dim")
            
            if not self.confirm("\nAdd another condition to this group?", default=False):
                break
        
        return conditions

    def create_smart_playlist(self) -> Optional[Dict[str, Any]]:
        """Create a complete smart playlist"""
        self.print_panel(
            "Smart Playlist Creator\n\n"
            "You'll be guided through creating rules, sorting, and limits.",
            title="Create New Playlist"
        )
        
        # Basic info
        name = self.prompt("\nPlaylist name", default="My Smart Playlist")
        comment = self.prompt("Description/comment (optional)", default="")
        
        playlist = {}
        if name:
            playlist["name"] = name
        if comment:
            playlist["comment"] = comment
        
        # Conditions
        self.print("\n[cyan]═══ Creating Playlist Rules ═══[/cyan]", style="bold")
        self.print("Rules determine which songs are included.\n")
        
        conditions = self.create_condition_group()
        
        if conditions:
            logic = self.prompt("Combine conditions with 'all' or 'any'", default="all")
            playlist[logic] = conditions
        
        # Sorting
        self.print(f"\n[cyan]═══ Sorting Options ═══[/cyan]", style="bold")
        self.print(f"Available sort fields: {', '.join(self.sort_fields)}\n")
        
        sort = self.prompt("Sort by (e.g., 'year', '-rating,title', 'random')", default="random")
        if sort:
            playlist["sort"] = sort
            
            if sort != "random" and "," not in sort and not sort.startswith("-") and not sort.startswith("+"):
                order = self.prompt("Sort order: 'asc' or 'desc'", default="desc")
                if order:
                    playlist["order"] = order
        
        # Limit
        if self.confirm("\nSet a limit on number of songs?", default=True):
            limit = int(self.prompt("Maximum number of songs", default="100"))
            playlist["limit"] = limit
        
        return playlist

    def preview_playlist(self, playlist: Dict[str, Any]):
        """Show a preview of the playlist JSON"""
        self.print_panel(
            json.dumps(playlist, indent=2),
            title="Playlist Preview"
        )

    def save_playlist(self, playlist: Dict[str, Any]):
        """Save playlist to .nsp file"""
        if not self.playlist_dir:
            self.print("[red]No playlist directory set! Please configure it first.[/red]", style="bold")
            return
        
        # Suggest filename from playlist name
        default_name = playlist.get("name", "playlist").lower().replace(" ", "-")
        default_name = "".join(c for c in default_name if c.isalnum() or c in ['-', '_'])
        
        filename = self.prompt(f"\nFilename (without .nsp)", default=default_name)
        if not filename.endswith('.nsp'):
            filename += '.nsp'
        
        filepath = self.playlist_dir / filename
        
        if filepath.exists():
            if not self.confirm(f"File {filename} already exists. Overwrite?", default=False):
                self.print("[yellow]Save cancelled.[/yellow]")
                return
        
        try:
            with open(filepath, 'w') as f:
                json.dump(playlist, f, indent=2)
            self.print(f"\n[green]✓ Playlist saved successfully to:[/green]", style="bold")
            self.print(f"[green]  {filepath}[/green]", style="bold")
        except Exception as e:
            self.print(f"[red]✗ Error saving playlist: {e}[/red]", style="bold")

    def show_examples(self):
        """Show example playlists"""
        examples = {
            "Recently Played": {
                "name": "Recently Played",
                "comment": "Tracks played in the last 30 days",
                "all": [{"inTheLast": {"lastPlayed": 30}}],
                "sort": "lastPlayed",
                "order": "desc",
                "limit": 100
            },
            "80s Favorites": {
                "name": "80s Favorites",
                "all": [
                    {"any": [{"is": {"loved": True}}, {"gt": {"rating": 3}}]},
                    {"inTheRange": {"year": [1980, 1989]}}
                ],
                "sort": "year",
                "order": "desc",
                "limit": 50
            },
            "High Quality Tracks": {
                "name": "High Quality",
                "comment": "Lossless tracks only",
                "all": [
                    {"gt": {"bitrate": 900}},
                    {"is": {"filetype": "flac"}}
                ],
                "sort": "random",
                "limit": 200
            }
        }
        
        self.print("\n[cyan]═══ Example Playlists ═══[/cyan]", style="bold")
        for title, playlist in examples.items():
            self.print(f"\n[yellow]{title}:[/yellow]", style="bold")
            self.print(json.dumps(playlist, indent=2))
        print()

    def main_menu(self):
        """Main menu loop"""
        while True:
            self.print("\n" + "="*60, style="cyan")
            self.print("  NAVIDROME SMART PLAYLIST CREATOR", style="bold cyan")
            self.print("="*60, style="cyan")
            
            if self.playlist_dir:
                self.print(f"\n[green]✓ Playlist Directory:[/green] {self.playlist_dir}", style="dim")
            else:
                self.print("\n[red]⚠ No playlist directory configured![/red]", style="bold")
            
            self.print("\n[cyan]Options:[/cyan]", style="bold")
            self.print("  [1] Set/Change Playlist Directory")
            self.print("  [2] Create New Smart Playlist")
            self.print("  [3] View Field Reference")
            self.print("  [4] View Operator Reference")
            self.print("  [5] Show Example Playlists")
            self.print("  [6] Exit")
            
            choice = self.prompt("\nSelect option", default="2")
            
            if choice == "1":
                self.set_playlist_directory()
            elif choice == "2":
                playlist = self.create_smart_playlist()
                if playlist:
                    self.preview_playlist(playlist)
                    if self.confirm("\nSave this playlist?", default=True):
                        self.save_playlist(playlist)
                    if self.confirm("Create another playlist?", default=False):
                        continue
            elif choice == "3":
                self.show_field_reference()
            elif choice == "4":
                self.show_operator_reference()
            elif choice == "5":
                self.show_examples()
            elif choice == "6":
                self.print("\n[cyan]Goodbye! 👋[/cyan]", style="bold")
                break
            else:
                self.print("[red]Invalid option![/red]", style="bold")

def main():
    """Entry point"""
    try:
        creator = SmartPlaylistCreator()
        creator.main_menu()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
