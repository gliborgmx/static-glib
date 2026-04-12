#!/usr/bin/env python3

"""Publish a Tooth given an MD file"""

from typing import Optional

import os
import re
import sys
import uuid
import requests

MESSAGE = "¡Hemos publicado un nuevo texto!"
BASE_BLOG_URL = "https://glib.org.mx/"
BASE_URL = "https://floss.social/api/v1/statuses"

URI = "urn:ietf:wg:oauth:2.0:oob"

META_RE = re.compile(
    r"^[ ]{0,3}(?P<key>[A-Za-z0-9_-]+)\s*=\s*(?P<value>.*?)\s*(?:#.*)?$"
)
BEGIN_RE = re.compile(r"^\+{3}(\s.*)?")
END_RE = re.compile(r"^(\+{3}|\.{3})(\s.*)?")

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


def publish(meta: dict) -> bool:  # pylint: disable=too-many-return-statements
    """HTTP post message to mastodon server with message to publish"""
    if not ACCESS_TOKEN:
        print("Error: ACCESS_TOKEN no configurado o vacío", file=sys.stderr)
        return False

    # Validate required fields
    try:
        title = meta["title"][0]
        slug = meta["slug"][0]
    except (LookupError, IndexError):
        print("Error: Metadata no contiene título o slug", file=sys.stderr)
        return False

    # Check if article is draft
    try:
        if meta.get("draft") and meta["draft"][0].lower() in ["true", "yes", "1"]:
            print(f"Artículo {slug} es un borrador - no se publica", file=sys.stderr)
            return True
    except (LookupError, IndexError):
        pass

    # https://docs.joinmastodon.org/methods/statuses/#headers
    headers: dict = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Idempotency-Key": str(uuid.uuid4()),
    }

    status = f"{MESSAGE}\n\n{title}\n\n{BASE_BLOG_URL}{slug}"

    # https://docs.joinmastodon.org/methods/statuses/#form-data-parameters
    form_data: dict = {
        "status": status,
        "visibility": "public",
        "language": "es",
    }

    try:
        response = requests.post(BASE_URL, headers=headers, data=form_data, timeout=10)
        response.raise_for_status()
        print(f"✓ Publicado en Mastodon: {title}", file=sys.stderr)
        return True
    except requests.exceptions.Timeout:
        print(f"Error: Timeout al conectar con Mastodon ({BASE_URL})", file=sys.stderr)
        return False
    except requests.exceptions.ConnectionError:
        print(f"Error: No se pudo conectar con Mastodon ({BASE_URL})", file=sys.stderr)
        return False
    except requests.exceptions.HTTPError as e:
        print(
            f"Error HTTP {response.status_code if 'response' in locals() else 'N/A'}: {e}",
            file=sys.stderr,
        )
        if "response" in locals() and response.text:
            print(f"Respuesta del servidor: {response.text}", file=sys.stderr)
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}", file=sys.stderr)
        return False


def get_meta(fname: str) -> Optional[dict]:  # pylint: disable=too-many-return-statements
    """Gets meta information of the post"""
    meta: dict[str, list[str]] = {}
    try:
        with open(fname, encoding="utf-8") as fn:
            try:
                line = next(fn).strip()
            except StopIteration:
                print(f"Error: Archivo vacío: {fname}", file=sys.stderr)
                return None

            if not BEGIN_RE.match(line):
                print(
                    f"Error: No se encontró front matter (+++) en {fname}",
                    file=sys.stderr,
                )
                return None

            while True:
                try:
                    line = next(fn).strip()
                except StopIteration:
                    print(f"Error: Front matter sin cerrar en {fname}", file=sys.stderr)
                    return None

                if END_RE.match(line):
                    return meta

                m1 = META_RE.match(line)
                if m1:
                    key = m1.group("key").lower().strip()
                    value = m1.group("value").strip()
                    # Remove surrounding double quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    try:
                        meta[key].append(value)
                    except LookupError:
                        meta[key] = [value]
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado: {fname}", file=sys.stderr)
        return None
    except PermissionError:
        print(f"Error: Permiso denegado para leer: {fname}", file=sys.stderr)
        return None
    except IOError as e:
        print(f"Error de E/S al leer {fname}: {e}", file=sys.stderr)
        return None

    print(f"No metadata encontrada en {fname}", file=sys.stderr)
    return None


def process(filename: str) -> int:
    """Gets article's meta and publish the link in mastodon"""
    meta = get_meta(filename)
    if meta is None:
        return -1

    return 0 if publish(meta) else -1


def main() -> int:
    """Main function"""
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <archivo.md>", file=sys.stderr)
        print("  Publica en Mastodon un enlace al artículo", file=sys.stderr)
        print("  Requiere variable de entorno ACCESS_TOKEN", file=sys.stderr)
        return -1

    if not ACCESS_TOKEN:
        print("Error: Variable de entorno ACCESS_TOKEN no configurada", file=sys.stderr)
        print("  Configurar con: export ACCESS_TOKEN='tu_token'", file=sys.stderr)
        return -1

    return process(sys.argv[1])


if __name__ == "__main__":
    sys.exit(main())
