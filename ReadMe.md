# Sitio estático del Grupo Linuxero del Bajío

Repositorio del sitio web del [Grupo Linuxero del Bajío](https://glib.org.mx),
orientado a la tecnología computacional en general y al software libre en
particular, en español y enfocado a las personas que viven en el Bajío mexicano.

Históricamente <https://glib.org.mx> usó
[GeekLog](https://www.geeklog.net/) como manejador de contenidos (CMS). Sin
embargo, mantener un CMS exige un esfuerzo de administración constante:
actualizar el propio CMS y vigilar los agujeros de seguridad de la
infraestructura que este requiere (PHP, MySQL, etc.). La tendencia actual a usar
generadores estáticos elimina buena parte de ese trabajo.

Este repositorio contiene la migración del sitio original, con GeekLog, a
artículos en formato Markdown, que se convierten a HTML con un generador
estático escrito en [Rust](https://www.rust-lang.org):
[Zola](https://www.getzola.org).

Los comentarios también se han migrado de GeekLog al manejador de comentarios en
JavaScript [Isso comments](https://isso-comments.de/).

## Características técnicas

- Se usa únicamente [HTML
  semántico](https://es.wikipedia.org/wiki/HTML_sem%C3%A1ntico) en las
  plantillas, y los estilos se aplican con CSS *sin clases*, mediante [Pico
  CSS](https://picocss.com/) como único framework.
- El contenido está escrito en
  [CommonMark](https://spec.commonmark.org), con encabezados
  ([frontmatter](https://www.markdownlang.com/advanced/frontmatter.html)) en
  [YAML](https://yaml.org) delimitados por `+`.
- No se utiliza ningún framework de JavaScript (salvo pequeños snippets
  embebidos).

## Estructura del proyecto

- `content/`: textos publicados (Markdown con frontmatter en YAML).
- `sass/`: estilos SCSS (importa Pico CSS).
- `scripts/`: scripts de ayuda en Python.
- `static/`: archivos estáticos (imágenes, CSS, JavaScript).
- `templates/`: plantillas [Tera](https://keats.github.io/tera/) para Zola.
- `templates/shortcodes/`: scripts en Tera para Zola.

## Desarrollo

### Requisitos

- [Zola](https://www.getzola.org/): el binario incluido en el repositorio se
  puede usar directamente con `./zola`.
- [Python](https://www.python.org) 3.12+ y [uv](https://docs.astral.sh/uv/) para
  las herramientas de automatización y validación.

Instala las dependencias de Python con:

```bash
uv sync
```

### Construir el sitio para producción

```bash
./zola build
```

El sitio generado se guarda en el directorio `public/`.

También existe un `Makefile` con los objetivos `build`, `minify` y `publish`.

## Contribuir

El flujo de colaboración está documentado en
[`content/contribuir/index.md`](content/contribuir/index.md) (y publicado en
<https://glib.org.mx/contribuir/>). En resumen: se escribe en Markdown, se
comparte con Git y se propone mediante un *pull request* en
[GitHub](https://github.com/gliborgmx/static-glib).

Para crear un artículo nuevo existe el script `scripts/crear_articulo.py`:

```bash
uv run scripts/crear_articulo.py --title "Título del artículo" --tema articulos
```

El script genera un nombre de archivo con marca de tiempo, cambia a `main`, crea
una rama nueva basada en el título, crea el archivo con su *frontmatter* y abre
el editor predeterminado. Usa `--no-git` para omitir las operaciones de Git
(útil para pruebas) y `--no-editor` para no abrir el editor.

Los temas permitidos son: `anuncios`, `articulos`, `educacion`, `noticias`,
`glib`, `preguntas` y `seguridad`.

## Validación de contenido

Antes de proponer cambios, verifica el contenido:

- Markdown: `pymarkdown scan content/`
- Ortografía: `python -m pyspelling -n ortografia`
- Hooks de pre-commit: `pre-commit run --all-files`

Los hooks de pre-commit ya están configurados para ejecutarse en cada commit e
incluyen la corrección de espacios y finales de línea, la validación de
ortografía, la validación de Markdown y el formateo y verificación del código
Python (ruff y pylint).

Las palabras no encontradas por el corrector ortográfico se añaden al final de
`es-local.dic`; el archivo se ordena y actualiza automáticamente con:

```bash
uv run scripts/corregir_diccionario.py
```
