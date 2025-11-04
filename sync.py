import hashlib
import os
import shutil
import argparse
from pathlib import Path
from rich.console import Console

# Inicjalizacja konsoli rich
console = Console()

def calculate_hash(filepath: Path) -> str:
    """Oblicza sumę kontrolną SHA256 dla pliku."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as file:
            while chunk := file.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return ""
    except Exception as e:
        console.print(f"[bold red]BŁĄD:[/bold red] Nie można obliczyć sumy kontrolnej dla {filepath}: {e}")
        return ""

def find_files(directory: Path) -> list[Path]:
    """Znajduje wszystkie pliki w podanym katalogu i podkatalogach."""
    return [p for p in directory.rglob('*') if p.is_file()]

def print_status(action: str, relative_path: Path, dry_run: bool):
    """Wyświetla kolorowy komunikat o statusie."""
    path_str = str(relative_path)
    
    if action == "COPY":
        status = "[bold green]SKOPIOWANO[/bold green]"
    elif action == "UPDATE":
        status = "[bold yellow]ZAKTUALIZOWANO[/bold yellow]"
    elif action == "SKIP":
        status = "[bold blue]POMINIĘTO[/bold blue]"
    else:
        status = action
        
    if dry_run and action != "SKIP":
        status = f"[bold magenta]DRY-RUN[/bold magenta] {status}"
        
    console.print(f"{status}: {path_str}")

def sync_files(source_dir: Path, destination_dir: Path, dry_run: bool = False, verbose: bool = False):
    """Główna logika synchronizacji plików."""
    
    if not source_dir.is_dir():
        console.print(f"[bold red]BŁĄD:[/bold red] Katalog źródłowy nie istnieje: {source_dir}")
        return

    destination_dir.mkdir(parents=True, exist_ok=True)
    source_files = find_files(source_dir)
    
    if verbose:
        console.print(f"[bold cyan]INFO:[/bold cyan] Znaleziono {len(source_files)} plików w źródle: [yellow]{source_dir}[/yellow]")
        if dry_run:
            console.print("[bold magenta]INFO:[/bold magenta] Tryb [bold magenta]DRY-RUN[/bold magenta] jest aktywny. Żadne pliki nie zostaną zmienione.")

    for source_path in source_files:
        relative_path = source_path.relative_to(source_dir)
        destination_path = destination_dir / relative_path
        
        destination_path.parent.mkdir(parents=True, exist_ok=True)

        source_hash = calculate_hash(source_path)
        destination_hash = calculate_hash(destination_path)
        
        action = "SKIP"
        
        if not destination_path.exists():
            action = "COPY"
        elif source_hash != destination_hash:
            action = "UPDATE"
        
        if action != "SKIP":
            if not dry_run:
                try:
                    shutil.copy2(source_path, destination_path)
                except Exception as e:
                    console.print(f"[bold red]BŁĄD KOP.:[/bold red] Nie można skopiować {relative_path}: {e}")
                    continue
            
            print_status(action, relative_path, dry_run)
        elif verbose:
            print_status(action, relative_path, dry_run)

def main():
    parser = argparse.ArgumentParser(
        description="bmcode-sync: Narzędzie do synchronizacji plików logów na podstawie sum kontrolnych."
    )
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Katalog źródłowy do synchronizacji."
    )
    parser.add_argument(
        "--destination",
        type=Path,
        required=True,
        help="Katalog docelowy do synchronizacji."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Symuluje synchronizację bez faktycznego kopiowania plików."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Wyświetla szczegółowe informacje, w tym pominięte pliki."
    )
    
    args = parser.parse_args()
    
    sync_files(args.source, args.destination, args.dry_run, args.verbose)

if __name__ == "__main__":
    main()
