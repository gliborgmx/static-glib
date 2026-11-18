#!/usr/bin/env python3
"""Revisa ortografía solo de los archivos que envía pre-commit.

pre-commit invoca este script con la lista de archivos preparados para el
commit (que cumplen con el filtro `files: \\.md$` del hook). En lugar de
escanear todos los patrones `sources` de la configuración, cada archivo se
pasa de forma explícita con la opción `-S` de pyspelling, que sustituye
dichos patrones; pyspelling solo respeta `-S` cuando se solicita un único
nombre de tarea, condición que este proyecto cumple, pues su matriz tiene
una sola tarea: `ortografia`.

pyspelling compila las listas de palabras en un archivo de nombre fijo
(`dictionary.dic`) que reescribe al inicio de cada ejecución, de modo que
dos ejecuciones simultáneas se pisan el mismo archivo. Para evitarlo, el
script genera una copia temporal de la configuración cuyo diccionario
compilado vive en un directorio temporal exclusivo de la ejecución.

De este modo, el hook tarda segundos en vez de minutos, y la revisión
completa queda en manos de `pre-commit run --all-files` y del CI
(`revisar.yml`), que emplea la misma técnica.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

# Configuración y tarea de ortografía del proyecto
CONFIG = Path(".pyspelling.yml")
TAREA = "ortografia"


def preparar_config(tempdir: str) -> Path:
    """Copia la configuración con un diccionario compilado propio."""
    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    salida = str(Path(tempdir).resolve() / "dictionary.dic")
    for tarea in config.get("matrix", []):
        if tarea.get("name") == TAREA:
            tarea.setdefault("dictionary", {})["output"] = salida
    destino = Path(tempdir) / CONFIG.name
    destino.write_text(yaml.safe_dump(config, allow_unicode=True), encoding="utf-8")
    return destino


def main() -> int:
    """Revisa la ortografía de los archivos recibidos por argv."""
    archivos = sys.argv[1:]
    if not archivos:
        return 0
    with tempfile.TemporaryDirectory() as tempdir:
        comando = ["pyspelling", "-c", str(preparar_config(tempdir)), "-n", TAREA]
        for archivo in archivos:
            comando.extend(["-S", archivo])
        return subprocess.run(comando, check=False).returncode


if __name__ == "__main__":
    sys.exit(main())
