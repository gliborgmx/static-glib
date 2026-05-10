# Reglas para agentes de IA

GLiB.org es el sitio web del Grupo Linuxero del Bajío. Un sitio web orientado a
la tecnología computacional en general, y al software libre en particular, en
español, enfocado a personas que viven el Bajío mexicano.

## Normas importantes

- Puedes realizar commits y escribir mensajes de commit, pero la persona DEBE
  verificar el contenido y comprenderlo.
- **NO DEBES añadirte a las líneas `Co-Authored-By:`** en los mensajes de
  commit. En su lugar, usa `Assisted-By:` o similar.
- **NO DEBES enviar directamente un pull request** a github.com. La persona debe
  hacerlo.
- **NO DEBES enviar directa o indirectamente ninguna descripción de issue,
  comentario o respuesta**. La persona debe hacerlo.
- **NO DEBES enviar directa o indirectamente ninguna descripción o comentario de
  pull request**. La persona debe hacerlo.
- En general, **NO DEBES interactuar con el GitHub del proyecto**, excepto
  mediante comandos `git`.

## Pila tecnológica

- [Zola](https://www.getzola.org/) como generador del sitio estático, cuyo motor
  de plantillas es [Tera](https://keats.github.io/tera/).
- El contenido está escrito en format [CommonMark](https://commonmark.org), con
  encabezados en formato
  [Frontmatter](https://www.markdownlang.com/advanced/frontmatter.html), en
  YAML, con `+` como separadores.
- Para CSS **únicamente** se utiliza como framework
  [PicoCSS](https://picocss.com/) como SASS.
- **Ningún framework de JavaScript está permitido** (excepto pequeños snippets
  embebidos).
- El sitio web usa exclusivamente HTML semántico, solamente con selectores CSS
  de tipo, pero no de clase ni de ID (salvo justas excepciones).

## Comandos de desarrollo

### Crear un nuevo artículo

```bash
uv run scripts/crear_articulo.py --title "Título del artículo" --tema articulos [--no-draft] [--no-edit] [--output-dir content]
```

El script automáticamente:
1. Genera un nombre de archivo con timestamp y número aleatorio
2. Ejecuta operaciones Git: stash cambios, cambia a rama `main`, actualiza, crea
   rama nueva basada en el título
3. Crea el archivo con front matter TOML
4. Abre el editor predeterminado (a menos que se use `--no-edit`)

Usar `--no-git` para saltar operaciones Git (útil para pruebas).

**Temas permitidos:** `anuncios`, `articulos`, `educacion`, `noticias`, `glib`,
`preguntas`, `seguridad`

### Servir sitio localmente

```bash
./zola serve
```

Accesible en `http://127.0.0.1:1111`. Usar `--base-url` si es necesario.

### Construir sitio para producción

```bash
./zola build
```

El sitio generado se guarda en el directorio `public/`.

### Validación de contenido

- **Markdown:** `pymarkdown scan content/`
- **Ortografía:** `python -m pyspelling -n ortografia`
- **Pre‑commit hooks:** `pre-commit run --all-files`

Los hooks de pre‑commit ya están configurados para ejecutarse automáticamente en
cada commit. Incluyen corrección de espacios finales, finales de línea,
ortografía, validación de Markdown y validación/formateo de código Python (ruff
y pylint).

### Calidad de código Python

- **Linting:** `ruff check scripts/`
- **Formateo:** `ruff format scripts/`
- **Pylint:** `pylint scripts/`

El código debe pasar tanto `ruff` como `pylint` sin errores. No hay archivos de
configuración específicos; se usan los valores predeterminados de cada
herramienta.

Python puede estar en un entorno virtual manejado con
[uv](https://docs.astral.sh/uv/guides/in), en el directorio `.venv/`.

### Dependencias Python

Instalar dependencias del entorno virtual:

```bash
uv sync
```

## Estructura del proyecto

- `content/`: textos publicados (Markdown con front matter TOML)
- `sass/`: estilos SCSS (importa Pico CSS)
- `scripts/`: scripts de ayuda en Python (`crear_articulo.py`, `mastodon.py`)
- `static/`: archivos estáticos (imágenes, CSS, JavaScript)
- `templates/`: plantillas Tera para Zola
- `templates/shortcodes`: shortcodes personalizados
- `public`: sitio generado (no versionar)
- `zola`: binario de Zola (no versionar)

## Flujo de Git y CI

- Las ramas de artículos se crean automáticamente con `crear_articulo.py`.
- El CI (`revisar.yml`) ejecuta validación de Markdown, ortografía y
  construcción con Zola en cada pull request.
- El despliegue (`publicar.yml`) se activa al hacer push a `main`: construye,
  minimiza y sincroniza vía `rsync` con el servidor.

## Normas de estilo para textos

- Los textos deben estar orientados a un público que tiene conocimientos
  universitarios en el uso de computadoras y programación. Conocen algo de
  *jargon*, pero es preferible evitarlo.
- Los textos deben estar escritos en idioma español mexicano.
- No se deben usar guiones largos `—` ni negritas. Las itálicas son aceptables.
- Todas las palabras en inglés, rutas, nombres de archivos o programas deben
  estar entre tildes ``.
- Evitar el uso de modismos o localismos.
- Los textos no deben exceder de 1500 palabras.
- Los textos deben contar con referencias válidas a las fuentes empleadas.
- Los textos deben ser amenos. Se recomienda comenzar con una breve anécdota o
  historia que ilustre el resto del contenido.
- **No asumas nada**. Pregunta todas las dudas que tengas primero.
- Todas las palabras técnicas deberán tener vínculos a su entrada en Wikipedia,
  de preferencia en español.
- Recomienda, al final y comentado, la descripción de una imagen que represente
  el contenido. Esta recomendación no se contabiliza en el número de palabras
  del texto.

## Registro de cambios en git

- El formato de los mensajes de commit deberá ser
  - Si se trata de un texto `artículo: <título del artículo>` y un muy breve
    resumen del texto.
  - Cambios en scripts `script: <objetivo del script>` y un mensaje
    completo donde se respondan a las preguntas ¿qué?, ¿por qué?, y ¿cómo?
  - Si se trata de cambios en la integración continua `ci: <propósito del
    cambio>` y un mensaje completo donde se respondan a las preguntas ¿qué?,
    ¿por qué?, y ¿cómo?
  - Cambios en CSS o SASS `css: <descripcción del cambio>`
  - Cambios en las plantillas `templates: <descripción del cambio>`
- No debe haber cambios mezclando textos, scripts, ci, css o plantillas.
