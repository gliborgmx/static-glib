#!/usr/bin/env python3
"""
Script to create new articles for Zola static site.
Generates a filename with timestamp and random number, creates front matter,
and opens the file in the default editor.
"""

import os
import sys
import datetime
import random
import subprocess
import argparse
import getpass
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

# Allowed tema values
ALLOWED_TEMAS = ['anuncios',
                 'articulos',
                 'educacion',
                 'noticias',
                 'glib',
                 'preguntas',
                 'seguridad']


def get_default_author():
    """Get the user's full name from Git configuration."""
    try:
        # Try to get the name from Git configuration
        result = subprocess.run(
            ['git', 'config', '--get', 'user.name'],
            capture_output=True,
            text=True,
            check=False  # Don't raise exception on non-zero exit
        )
        if result.returncode == 0 and result.stdout.strip():
            # Successfully got name from Git
            return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        # Git not installed or other error, fall back to OS method
        pass

    # Fallback to OS method if Git doesn't provide a name
    try:
        if sys.platform == 'win32':
            # Windows: try to get full name from environment or use username
            full_name = os.getenv('USERNAME', getpass.getuser())
            return full_name
        else:
            # Unix-like systems (Linux, macOS)
            username = getpass.getuser()
            try:
                # Try to import pwd (not available on Windows)
                import pwd
                # Try to get GECOS field (full name)
                gecos = pwd.getpwnam(username).pw_gecos
                if gecos and ',' in gecos:
                    # GECOS often has comma-separated fields: full name,
                    # office, etc.
                    full_name = gecos.split(',')[0]
                else:
                    full_name = gecos or username
                return full_name
            except (KeyError, AttributeError, ImportError):
                return username
    except Exception:
        return getpass.getuser()  # Fallback to username


def generate_filename():
    """
    Generate a 17-character filename: YYYYMMDDHHMMSS + random 3-digit number.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_num = random.randint(100, 999)  # 3-digit random number
    return f"{timestamp}{random_num}.md"


@dataclass
class Metadata():
    """Class for holding article's metadata"""
    title: str
    date: str
    draft: bool
    autor: str
    slug: str
    extra_fields: Optional[dict] = None
    tema: str = 'articulos'


def create_front_matter(metadata: Metadata):
    """Create TOML front matter for Zola article."""
    if metadata.date is None:
        metadata.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    front_matter = "+++\n"

    # Required fields
    if metadata.title:
        front_matter += f'title = "{metadata.title}"\n'
    if metadata.slug:
        front_matter += f'slug = "{metadata.slug}"\n'
    front_matter += f'date = {metadata.date}\n'
    front_matter += f'draft = {str(metadata.draft).lower()}\n'

    front_matter += '[taxonomies]\n'

    # Author field (always included)
    if metadata.autor is None:
        metadata.autor = get_default_author()
    front_matter += f'autor = ["{metadata.autor}"]\n'

    # Tema field (required)
    if metadata.tema:
        front_matter += f'tema = ["{metadata.tema}"]\n'

    # Extra custom fields
    if metadata.extra_fields:
        for key, value in metadata.extra_fields.items():
            if isinstance(value, str):
                front_matter += f'{key} = "{value}"\n'
            elif isinstance(value, bool):
                front_matter += f'{key} = {str(value).lower()}\n'
            elif isinstance(value, (int, float)):
                front_matter += f'{key} = {value}\n'
            elif isinstance(value, list):
                front_matter += f'{key} = [\n'
                for item in value:
                    front_matter += f'    "{item}",\n'
                front_matter += ']\n'

    front_matter += "+++\n\n"
    return front_matter


def open_in_editor(filepath):
    """Open the file in the default editor based on the platform."""
    if sys.platform == 'win32':
        os.startfile(filepath)
    elif sys.platform == 'darwin':  # macOS
        subprocess.run(['open', filepath])
    else:  # Linux and other Unix-like
        # Try to use xdg-open, or fall back to $EDITOR
        try:
            subprocess.run(['xdg-open', filepath])
        except FileNotFoundError:
            editor = os.environ.get('EDITOR', 'vi')
            subprocess.run([editor, filepath])


def main():
    parser = argparse.ArgumentParser(description="Crear un artículo en GLiB")
    parser.add_argument("--title", "-t", help="Título de artículo")
    parser.add_argument(
        "--date", "-d", help="Fecha de publicación (YYYY-MM-DD)")
    parser.add_argument(
        "--no-draft",
        action="store_true",
        help="Marcar artículo como no borrador"
    )
    parser.add_argument(
        "--author",
        "-a",
        default=None,
        help="Nombre del autor (por defecto el nombre en git)",
    )
    parser.add_argument(
        "--tema",
        "-T",
        required=True,
        choices=ALLOWED_TEMAS,
        help=f"Tema del artículo. Debe ser uno de: {', '.join(ALLOWED_TEMAS)}",
    )
    parser.add_argument(
        "--no-edit",
        action="store_true",
        help="No abrir el editor tras la creación del archivo",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="content",
        help="Directorio de artículos (default: content)",
    )

    args = parser.parse_args()

    # Validate tema is in allowed list (argparse choices handles this, but we
    # can double-check)
    if args.tema not in ALLOWED_TEMAS:
        print(f"Error: El tema de ser uno de {ALLOWED_TEMAS}", file=sys.stderr)
        sys.exit(1)

    # Generate filename
    filename = generate_filename()
    slug = filename[:-3]  # Remove .md extension
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    filepath = output_dir / filename

    # Check if file already exists (unlikely but possible)
    if filepath.exists():
        print(f"Error: El archivo {filepath} ya existe!", file=sys.stderr)
        sys.exit(1)

    # Create front matter
    front_matter = create_front_matter(
        Metadata(
            title=args.title,
            date=args.date,
            draft=not args.no_draft,
            autor=args.author,
            tema=args.tema,
            slug=slug,
        )
    )

    # Write the file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(front_matter)
        f.write("# Título\n\n")
        f.write("Comienza a escribir tu artículo desde aquí.\n")

    print(f"Nuevo archivo creado: {filepath}")

    # Open in editor if requested
    if not args.no_edit:
        print("Abriendo texto en el editor por defecto…")
        open_in_editor(filepath)


if __name__ == '__main__':
    main()
