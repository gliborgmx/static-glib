# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Corrector ortográfico interactivo usando aspell.

Lee archivos Markdown listados en changed-files.txt, revisa la ortografía
con aspell y el diccionario personal es-local.dic, e interactúa con el
usuario para agregar palabras al diccionario o reemplazarlas en el texto.

Las zonas ignoradas (front matter, código, negritas, shortcodes, URLs)
no se envían a revisión ortográfica.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


# --- Constantes ---

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CHANGED_FILES = PROJECT_ROOT / "changed-files.txt"
DEFAULT_DICT = PROJECT_ROOT / "es-local.dic"

# Regex para front matter TOML delimitado por +++
FRONT_MATTER_RE = re.compile(r"^\+\+\+\s*$")

# Placeholder único para zonas ignoradas
PLACEHOLDER_PREFIX = "ZZZPLACEHOLDER"
PLACEHOLDER_SUB_RE = re.compile(r"ZZZPLACEHOLDER\d+ZZZ")


def leer_archivos_cambiados(filepath: Path) -> list[Path]:
    """Lee la lista de archivos desde changed-files.txt.

    Args:
        filepath: Ruta al archivo changed-files.txt.

    Returns:
        Lista de rutas absolutas a los archivos Markdown.
    """
    if not filepath.exists():
        print(f"Error: {filepath} no existe", file=sys.stderr)
        sys.exit(1)

    paths: list[Path] = []
    with open(filepath, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            abs_path = (PROJECT_ROOT / line).resolve()
            if abs_path.exists():
                paths.append(abs_path)
            else:
                print(f"Advertencia: {abs_path} no existe, se omite", file=sys.stderr)

    return paths


def extraer_front_matter_y_cuerpo(texto: str) -> tuple[str, str]:
    """Separa el front matter TOML del cuerpo Markdown.

    Args:
        texto: Contenido completo del archivo.

    Returns:
        Tupla (front_matter, cuerpo). Si no hay front matter,
        front_matter es cadena vacía.
    """
    lines = texto.split("\n")
    if not lines or not FRONT_MATTER_RE.match(lines[0]):
        return "", texto

    fm_lines: list[str] = [lines[0]]
    for i, line in enumerate(lines[1:], start=1):
        fm_lines.append(line)
        if FRONT_MATTER_RE.match(line):
            cuerpo = "\n".join(lines[i + 1 :])
            return "\n".join(fm_lines), cuerpo

    # Si no se cerró el front matter, devolver todo como cuerpo
    return "", texto


def _construir_patrones_filtrado() -> list[tuple[re.Pattern, str]]:  # pylint: disable=unsubscriptable-object
    """Construye los patrones de reemplazo para filtrar zonas ignorables.

    Returns:
        Lista de tuplas (patron, tipo) en orden de aplicación.
        tipo puede ser 'replace_all', 'markdown_link', 'markdown_image'.
    """
    return [
        # 1. Bloques de código ```...``` (3+ backticks, multilínea)
        (re.compile(r"(`{3,})[\s\S]*?\1", re.MULTILINE), "replace_all"),
        # 2. Shortcodes {{ ... }} (multilínea)
        (re.compile(r"\{\{[\s\S]*?\}\}"), "replace_all"),
        # 3. Imágenes Markdown ![alt](url)
        (re.compile(r"!\[([^\]]*)\]\(([^)]+)\)"), "markdown_image"),
        # 4. Enlaces Markdown [texto](url)
        (re.compile(r"\[([^\]]*)\]\(([^)]+)\)"), "markdown_link"),
        # 5. URLs sueltas
        (re.compile(r"https?://[^\s<>\"')\]]+"), "replace_all"),
        # 6. Negritas **...**
        (re.compile(r"\*\*([^*]+)\*\*"), "replace_all"),
        # 7. Código inline `...`
        (re.compile(r"`([^`]+)`"), "replace_all"),
    ]


def filtrar_zonas_ignorables(texto: str) -> tuple[str, dict[str, str]]:
    """Reemplaza zonas que no deben revisarse ortográficamente con placeholders.

    Args:
        texto: Cuerpo Markdown sin front matter.

    Returns:
        Tupla (texto_filtrado, mapa_placeholders) donde mapa_placeholders
        asocia placeholder → texto original.
    """
    placeholders: dict[str, str] = {}
    counter = 0

    def registrar(original: str) -> str:
        nonlocal counter
        placeholder = f"{PLACEHOLDER_PREFIX}{counter}ZZZ"
        placeholders[placeholder] = original
        counter += 1
        return placeholder

    for patron, tipo in _construir_patrones_filtrado():
        if tipo == "replace_all":

            def _reemplazar(m: re.Match, _patron=patron) -> str:
                return registrar(m.group(0))

        elif tipo == "markdown_image":

            def _reemplazar(m: re.Match, _patron=patron) -> str:
                alt = m.group(1)
                url = m.group(2)
                return f"![{alt}]({registrar(url)})"

        elif tipo == "markdown_link":

            def _reemplazar(m: re.Match, _patron=patron) -> str:
                texto_enlace = m.group(1)
                url = m.group(2)
                return f"[{texto_enlace}]({registrar(url)})"

        else:
            continue

        texto = patron.sub(_reemplazar, texto)

    return texto, placeholders


def restaurar_zonas_ignorables(texto: str, placeholders: dict[str, str]) -> str:
    """Restaura los placeholders al texto original.

    Args:
        texto: Texto con placeholders.
        placeholders: Mapa placeholder → texto original.

    Returns:
        Texto con zonas originales restauradas.
    """
    resultado = texto
    for placeholder, original in placeholders.items():
        resultado = resultado.replace(placeholder, original)
    return resultado


def ejecutar_aspell(  # pylint: disable=too-many-branches
    texto: str, dict_path: Path
) -> list[tuple[int, str, list[str]]]:
    """Ejecuta aspell en modo pipe y devuelve palabras mal escritas.

    Args:
        texto: Texto a revisar (ya filtrado de zonas ignorables).
        dict_path: Ruta al diccionario personal es-local.dic.

    Returns:
        Lista de tuplas (offset, palabra, sugerencias).
        offset es el byte offset en el texto original.
    """
    if not texto.strip():
        return []

    # Eliminar placeholders antes de enviar a aspell para que no los
    # tokenize como palabras.
    texto_limpio = PLACEHOLDER_SUB_RE.sub(" ", texto)

    if not texto_limpio.strip():
        return []

    try:
        proc = subprocess.run(
            [
                "aspell",
                "-d",
                "es",
                "--encoding=utf-8",
                f"--home-dir={dict_path.parent}",
                f"--personal={dict_path.name}",
                "--ignore-case",
                "--ignore=3",
                "--mode=markdown",
                "-a",
            ],
            input=texto_limpio,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except FileNotFoundError:
        print("Error: aspell no está instalado o no está en PATH", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("Error: aspell excedió el tiempo límite", file=sys.stderr)
        return []

    if proc.returncode != 0 and proc.stderr:
        print(f"Advertencia aspell: {proc.stderr.strip()}", file=sys.stderr)

    errores: list[tuple[int, str, list[str]]] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line or line == "*" or line.startswith("@") or line.startswith("#"):
            continue

        # Formato pipe: "& palabra N offset: sugerencias"
        if line.startswith("&"):
            parts = line.split(" ", 4)
            if len(parts) < 5:
                continue
            palabra = parts[1]
            resto = parts[4]
            offset_match = re.match(r"(\d+):", resto)
            offset = int(offset_match.group(1)) if offset_match else 0
            sugerencias_str = resto[resto.find(":") + 1 :] if ":" in resto else ""
            sugerencias = [s.strip() for s in sugerencias_str.split(",") if s.strip()]
            errores.append((offset, palabra, sugerencias))
        # Formato: "# palabra offset" (sin sugerencias)
        elif line.startswith("#"):
            parts = line.split(" ", 3)
            if len(parts) >= 3:
                palabra = parts[1]
                try:
                    offset = int(parts[2])
                except ValueError:
                    offset = 0
                errores.append((offset, palabra, []))

    return errores


def encontrar_contexto(lineas: list[str], palabra: str) -> tuple[int, str]:
    """Encuentra la línea que contiene la palabra y devuelve su contexto.

    Args:
        lineas: Lista de líneas del texto original.
        palabra: Palabra a buscar.

    Returns:
        Tupla (num_linea, linea_contexto). num_linea es 1-indexado.
        Retorna (-1, "") si no se encuentra.
    """
    patron = re.compile(rf"\b{re.escape(palabra)}\b", re.IGNORECASE)
    for i, linea in enumerate(lineas):
        if patron.search(linea):
            return i + 1, linea.strip()
    return -1, ""


def mostrar_error(
    palabra: str, sugerencias: list[str], num_linea: int, linea: str
) -> None:
    """Muestra el error ortográfico con contexto.

    Args:
        palabra: Palabra mal escrita.
        sugerencias: Lista de sugerencias de aspell.
        num_linea: Número de línea (1-indexado).
        linea: Línea donde aparece la palabra.
    """
    resaltada = re.sub(
        rf"\b({re.escape(palabra)})\b",
        r"\033[1;31m\1\033[0m",
        linea,
        flags=re.IGNORECASE,
    )
    print(f"\n  Línea {num_linea}: {resaltada}")
    print(f"  → \033[1;33m{palabra}\033[0m")
    if sugerencias:
        print(f"  Sugerencias: {', '.join(sugerencias[:8])}")


def _palabra_en_diccionario(palabra: str, dict_path: Path) -> bool:
    """Verifica si una palabra ya existe en el diccionario (case-insensitive).

    Args:
        palabra: Palabra a buscar.
        dict_path: Ruta al archivo de diccionario.

    Returns:
        True si la palabra ya existe.
    """
    palabra_lower = palabra.lower()
    try:
        with open(dict_path, encoding="utf-8") as fh:
            for line in fh:
                if line.strip().lower() == palabra_lower:
                    return True
    except FileNotFoundError:
        pass
    return False


def agregar_a_diccionario(palabra: str, dict_path: Path) -> None:
    """Añade una palabra al diccionario personal es-local.dic.

    Args:
        palabra: Palabra a añadir.
        dict_path: Ruta al archivo de diccionario.
    """
    if _palabra_en_diccionario(palabra, dict_path):
        print(f"  '{palabra}' ya existe en el diccionario")
        return

    with open(dict_path, "a", encoding="utf-8") as fh:
        fh.write(f"{palabra}\n")
    print(f"  ✓ '{palabra}' agregada a {dict_path.name}")


def reemplazar_en_texto(texto: str, palabra_original: str, reemplazo: str) -> str:
    """Reemplaza todas las ocurrencias de una palabra en el texto.

    Usa word boundaries para solo reemplazar palabras completas.
    Preserva la capitalización original.

    Args:
        texto: Texto donde reemplazar.
        palabra_original: Palabra a buscar.
        reemplazo: Palabra de reemplazo.

    Returns:
        Texto con los reemplazos aplicados.
    """
    patron = re.compile(rf"\b{re.escape(palabra_original)}\b", re.IGNORECASE)

    def _preservar_capitalizacion(m: re.Match) -> str:
        original = m.group(0)
        if original.isupper():
            return reemplazo.upper()
        if original[0].isupper():
            return reemplazo[0].upper() + reemplazo[1:]
        return reemplazo

    return patron.sub(_preservar_capitalizacion, texto)


def _preguntar_opcion() -> str:
    """Muestra el menú de opciones y retorna la opción elegida.

    Returns:
        La opción elegida: 'a', 'r', 'i', 'I', 's', 'q'.
    """
    return (
        input(
            "  [a]gregar dicc  [r]eemplazar  [i]gnorar  "
            "[I]gnorar todas  [s]altar archivo  [q]salir\n"
            "  > "
        )
        .strip()
        .lower()
    )


def _procesar_reemplazo(
    palabra: str,
    nueva: str,
    cuerpo: str,
    cuerpo_filtrado: str,
    lineas_originales: list[str],
) -> tuple[str, str, list[str]]:
    """Aplica un reemplazo en todas las estructuras de texto.

    Args:
        palabra: Palabra original a reemplazar.
        nueva: Palabra de reemplazo.
        cuerpo: Cuerpo Markdown original.
        cuerpo_filtrado: Cuerpo Markdown filtrado.
        lineas_originales: Líneas del cuerpo original.

    Returns:
        Tupla (nuevo_cuerpo, nuevo_cuerpo_filtrado, nuevas_lineas).
    """
    nuevo_cuerpo = reemplazar_en_texto(cuerpo, palabra, nueva)
    nuevo_filtrado = reemplazar_en_texto(cuerpo_filtrado, palabra, nueva)
    nuevas_lineas = [
        reemplazar_en_texto(linea, palabra, nueva) for linea in lineas_originales
    ]
    print(f"  ✓ '{palabra}' → '{nueva}'")
    return nuevo_cuerpo, nuevo_filtrado, nuevas_lineas


def _guardar_archivo(
    filepath: Path,
    front_matter: str,
    cuerpo: str,
    placeholders: dict[str, str],
) -> None:
    """Guarda el archivo con el contenido corregido.

    Args:
        filepath: Ruta al archivo .md.
        front_matter: Front matter TOML.
        cuerpo: Cuerpo Markdown corregido.
        placeholders: Mapa de placeholders.
    """
    cuerpo_final = restaurar_zonas_ignorables(cuerpo, placeholders)
    nuevo_contenido = front_matter + ("\n" if front_matter else "") + cuerpo_final
    if not nuevo_contenido.endswith("\n"):
        nuevo_contenido += "\n"

    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write(nuevo_contenido)
    print(f"  ✓ Archivo guardado: {filepath.relative_to(PROJECT_ROOT)}")


@dataclass
class EstadoTexto:
    """Estado mutable del texto durante la corrección."""

    cuerpo: str
    cuerpo_filtrado: str
    lineas_originales: list[str]
    ignoradas: set[str]


def _procesar_error(  # pylint: disable=too-many-return-statements
    palabra: str,
    sugerencias: list[str],
    estado: EstadoTexto,
    dict_path: Path,
) -> tuple[bool, bool]:
    """Procesa interactivamente un error ortográfico.

    Args:
        palabra: Palabra mal escrita.
        sugerencias: Sugerencias de aspell.
        estado: Estado mutable del texto.
        dict_path: Ruta al diccionario.

    Returns:
        Tupla (modificado, continuar).
        continuar=False indica que se debe detener el procesamiento del archivo.
    """
    palabra_lower = palabra.lower()
    if palabra_lower in estado.ignoradas:
        return False, True

    num_linea, linea = encontrar_contexto(estado.lineas_originales, palabra)
    mostrar_error(palabra, sugerencias, num_linea, linea)

    opcion = _preguntar_opcion()

    if opcion == "a":
        agregar_a_diccionario(palabra, dict_path)
        return True, True

    if opcion == "r":
        nueva = input("  Reemplazar por: ").strip()
        if nueva and nueva != palabra:
            (
                estado.cuerpo,
                estado.cuerpo_filtrado,
                estado.lineas_originales,
            ) = _procesar_reemplazo(
                palabra,
                nueva,
                estado.cuerpo,
                estado.cuerpo_filtrado,
                estado.lineas_originales,
            )
            return True, True
        return False, True

    if opcion == "I":
        estado.ignoradas.add(palabra_lower)
        print(f"  Ignorando todas las ocurrencias de '{palabra}'")
        return False, True

    if opcion == "s":
        print("  Saltando el resto del archivo")
        return False, False

    if opcion == "q":
        print("  Saliendo...")
        return False, False

    if opcion == "i":
        return False, True

    print("  Opción no reconocida, se omite esta palabra")
    return False, True


def _cargar_archivo(filepath: Path) -> tuple[str, EstadoTexto, dict[str, str]]:
    """Carga y prepara un archivo Markdown para corrección.

    Args:
        filepath: Ruta al archivo .md.

    Returns:
        Tupla (front_matter, estado_texto, placeholders).
    """
    with open(filepath, encoding="utf-8") as fh:
        contenido = fh.read()

    front_matter, cuerpo = extraer_front_matter_y_cuerpo(contenido)
    cuerpo_filtrado, placeholders = filtrar_zonas_ignorables(cuerpo)
    estado = EstadoTexto(
        cuerpo=cuerpo,
        cuerpo_filtrado=cuerpo_filtrado,
        lineas_originales=cuerpo.split("\n"),
        ignoradas=set(),
    )
    return front_matter, estado, placeholders


def corregir_archivo(filepath: Path, dict_path: Path) -> bool:
    """Procesa interactivamente un archivo Markdown.

    Args:
        filepath: Ruta al archivo .md.
        dict_path: Ruta al diccionario personal.

    Returns:
        True si se hicieron cambios, False en caso contrario.
    """
    print(f"\n{'=' * 60}")
    print(f"Archivo: {filepath.relative_to(PROJECT_ROOT)}")
    print(f"{'=' * 60}")

    try:
        front_matter, estado, placeholders = _cargar_archivo(filepath)
    except (FileNotFoundError, PermissionError) as exc:
        print(f"Error al leer {filepath}: {exc}", file=sys.stderr)
        return False

    modificado = False
    while True:
        errores = ejecutar_aspell(estado.cuerpo_filtrado, dict_path)
        if not errores:
            print("  ✓ Sin errores ortográficos")
            break

        for _offset, palabra, sugerencias in errores:
            cambio, continuar = _procesar_error(palabra, sugerencias, estado, dict_path)
            if cambio:
                modificado = True
                break  # re-ejecutar aspell con el texto actualizado
            if not continuar:
                if modificado:
                    _guardar_archivo(
                        filepath, front_matter, estado.cuerpo, placeholders
                    )
                    return True
                return False
        else:
            # Se procesaron todos los errores sin cambios
            break

    if modificado:
        _guardar_archivo(filepath, front_matter, estado.cuerpo, placeholders)
        return True

    return False


def main() -> None:
    """Punto de entrada principal."""
    parser = argparse.ArgumentParser(
        description="Corrector ortográfico interactivo con aspell",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  uv run scripts/corregir_ortografia.py
  uv run scripts/corregir_ortografia.py --files-list other-files.txt
  uv run scripts/corregir_ortografia.py --dict mi-diccionario.dic
        """,
    )
    parser.add_argument(
        "--files-list",
        type=Path,
        default=DEFAULT_CHANGED_FILES,
        help=f"Archivo con lista de .md a revisar (default: {DEFAULT_CHANGED_FILES.name})",
    )
    parser.add_argument(
        "--dict",
        type=Path,
        default=DEFAULT_DICT,
        help=f"Diccionario personal aspell (default: {DEFAULT_DICT.name})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Solo mostrar errores, sin modificar archivos",
    )
    args = parser.parse_args()

    os.chdir(PROJECT_ROOT)

    archivos = leer_archivos_cambiados(args.files_list)
    if not archivos:
        print("No hay archivos para revisar", file=sys.stderr)
        sys.exit(0)

    print(f"Se revisarán {len(archivos)} archivo(s)")
    print(f"Diccionario: {args.dict}")
    if args.dry_run:
        print("Modo: solo lectura (--dry-run)")
    print()

    cambios_totales = 0
    for filepath in archivos:
        if corregir_archivo(filepath, args.dict):
            cambios_totales += 1

    print(f"\n{'=' * 60}")
    print(f"Revisión completada. {cambios_totales} archivo(s) modificado(s).")


if __name__ == "__main__":
    main()
