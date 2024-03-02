+++
title = "Cómo publicar tu texto en el GLiB"
slug = "contribuir"
date = 2025-02-14T10:52:00-01:00
description = "Instrucciones para publicar un texto en el GLiB"
+++

Muchas gracias por interesarte en compartir tu texto en el sitio
del Grupo Linuxero del Bajío.

Actualmente, el [GLiB](https://glib.org.mx), es un sitio web para compartir
información sobre *Software Libre* y tecnología en general, orientado hacia la
gente del [Bajío
mexicano](https://es.wikipedia.org/wiki/Baj%C3%ADo_(M%C3%A9xico)).

El sitio web del GLiB es, en su mayoría, HTML estático. Ya no es, como antes, un
manejador de contenidos (CMS) escrito en PHP o en algún otro lenguaje ejecutado
en el servidor. No obstante, los textos no se escriben en HTML, sino en un
formato de texto plano conocido como
[Markdown](https://www.markdownguide.org/getting-started/), que es mucho más
fácil de usar y de convertir a diferentes formatos.

Los textos en Markdown son convertidos a HTML utilizando
[Zola](https://www.getzola.org/), que es un [generador de sitios
estáticos](https://es.wikipedia.org/wiki/Generador_de_sitios_est%C3%A1ticos) muy
eficiente.

Para contribuir un texto se utiliza el mismo procedimiento que para el
desarrollo de software libre: a través del sistema de control de versiones
[Git](https://git-scm.com/book/es/). Y, como servidor principal, usamos
[GitHub](https://github.com/gliborgmx/static-glib). GitHub también se encarga de
generar las páginas HTML y desplegarlas, de manera automática, en el servidor,
una vez que se ha integrado una actualización en el repositorio principal.

Entendemos que conocer y utilizar `Markdown` y `Git` para contribuir pueden
parecer baremos muy altos, sobre todo para quienes empiezan, sin embargo, los
animamos a verlo como una oportunidad para aprender a usar estas herramientas,
indispensables hoy en día en el desarrollo de software.

<!-- more -->

## Crear una cuenta en GitHub

Si no tienes ya una cuenta de usuario en GitHub, lo primero es [crear
una](https://docs.github.com/es/get-started/start-your-journey/creating-an-account-on-github).
Es gratis.

Es necesario contar con una cuenta porque, para contribuir, usamos el mecanismo
de [pull
requests](https://docs.github.com/es/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews),
que es una forma de proponer cambios y que puedan ser revisados, integrados y
desplegados. Este mecanismo requiere que el contribuidor tenga una copia del
repositorio en GitHub.

## Bifurcar repositorio original

Si ya tienes tu cuenta de GitHub, puedes entonces hacer una copia *personal* (o
bifurcación) del [repositorio del sitio del
GLiB](https://github.com/gliborgmx/static-glib), a la que se le conoce como
[fork](https://docs.github.com/es/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo).

1. Ve a la página del repositorio del sitio del GLiB
   <https://github.com/gliborgmx/static-glib>
2. Oprime el botón de *Fork*

Con esta copia puedes hacer todos los cambios que quieras, pero no serán
publicados en el sitio web hasta que sean integrados en el sitio original. Es
decir, puedes jugar con ella cuanto quieras.

<!-- pyml disable-next-line line-length-->
{{ figure(src="fork.png" alt="Captura de pantalla para copiar el repositorio original") }}

Recuerda que tu copia personal tendrá la dirección tendrá esta forma (reemplaza
`<usuario>` por tu nombre de usuario en GitHub):
`https://github.com/<usuario>/static-glib`.

## Clonar tu repositorio

Los siguientes pasos pueden evitarse, ya que se puede utilizar directamente la
interfaz de usuario web de GitHub para hacer modificaciones y crear un *pull
request*. Sin embargo, este texto no documenta esa opción. Consideramos que el
usuario bien puede descubrirlo por su propia cuenta.

Para poder empujar tus cambios locales a tu repositorio personal en GitHub, es
necesario utilizar el protocolo
[SSH](https://es.wikipedia.org/wiki/Secure_Shell) y, para eso, primero debes
[añadir claves SSH a tu cuenta de
GitHub](https://docs.github.com/es/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).
Una vez añadidas las claves, puedes clonar tu repositorio en tu computadora y
hacer modificaciones localmente.

Para conocer la dirección SSH de tu repositorio has *click* el botón de *code*.

<!-- pyml disable-next-line line-length-->
{{ figure(src="clone.png", alt="Captura de pantalla con el URL para usar Git con SSH") }}

A continuación una videografía sobre cómo clonar localmente tu repositorio:

{{ asciinema(file="clone.cast", id="clone") }}

## Activar pre-commit (opcional)

[pre-commit](https://pre-commit.com/) es un [punto de enganche de
Git](https://git-scm.com/book/es/v2/Personalizaci%C3%B3n-de-Git-Puntos-de-enganche-en-Git)
que ayuda a validar los cambios que quieres introducir.

El sitio del GLiB, cuando se abre un *pull request*, los cambios propuestos
pasan por una validación automática de:

1. Ortografía, usando [Aspell](http://aspell.net/) con un diccionario local.
2. Validamos de manera estricta el formato de Markdown del documento.
3. Que el sitio web sea generado por Zola correctamente.

Estas validaciones remotas pueden ser bastante frustrantes para los
colaboradores, ya que no son inmediatas, sino que toman tiempo. Así que estas
mismas validaciones pueden hacerse de manera local y automática al integrar los
cambios en tu repositorio local.

Para habilitar estas validaciones locales es preciso [instalar
pre-commit](https://pre-commit.com/#install) en tu sistema y configurarlo como
manejador del punto de enganche de tu repositorio local del GLiB.

## Añadir tu artículo

Ahora creamos un nuevo artículo.

El nombre del archivo es especial, debido a la compatibilidad hacia atrás con el
antiguo manejador de contenidos que usábamos, el GeekLog. El nombre de archivo
debe ser la fecha en formato "%Y%m%d%H%M%S" (año-mes-día-hora-minuto-segundo).

Lo primero que debe llevar el documento son sus metadatos:

+ `title`: título del texto.
+ `slug`: la ruta del documento en la URL, que es el mismo del nombre el
  archivo.
+ `date`: la fecha en formato YYYY-MM-DD (por ejemplo, 2025-02-14), o siguiendo
  el formato de fecha y hora para Internet, definido en el
  [RFC3339](https://datatracker.ietf.org/doc/html/rfc3339).

Y luego taxonomías obligatorias:

+ `tema`: que puede ser **uno** de los siguientes:
  + `anuncios`: para anunciar sobre algún tema a la comunidad.
  + `articulos`: un artículo. Este será el más usual.
  + `glib`: algún aviso del grupo Linuxero del Bajío.
  + `noticias`: reproducir alguna noticia del software libre o la tecnología en
    general.
  + `preguntas`: preguntas que se quieran formular.
+ `autor`: nombre **completo** del autor del texto.

Pueden leer más sobre los metadatos necesarios en la [documentación de
Zola](https://www.getzola.org/documentation/content/page/).

La siguiente videografía muestra una forma de hacerlo con `vim`:

{{ asciinema(file="edit.cast", id="edit") }}

## Integrar y empujar tus cambios

Ya que tenemos el archivo con el texto a contribuir, es momento de añadir el
archivo y registrar los cambios en el repositorio local. Finalmente empujamos el
cambio a nuestro repositorio en GitHub.

{{ asciinema(file="push.cast", id="push") }}

## Abrir pull request

Ahora vamos a solicitar a los administradores del sitio que integren y publiquen
nuestros cambios en el sitio web a través de un *pull request*. Para esto vamos
a la página de GitHub donde está nuestro *fork* del repositorio.

<!-- pyml disable-next-line line-length-->
{{ figure(src="pull.png", alt="Captura de pantalla para crear un pull request") }}

<!-- pyml disable-next-line line-length-->
{{ figure(src="pull-2.png", alt="Captura de pantalla para confirmar el pull request") }}

Ahora se ejecutarán todas las validaciones, tanto automáticas, como la
ortografía y el formato Markdown, como las manuales por parte de los
administradores del sitio del GLiB, quienes integrarán los cambios al
repositorio original y se publicarán.

## Conclusiones

Cierto, elevamos muchísimo el listón para publicar en el sitio del GLiB. Pero
estamos convencidos de que así la calidad de los artículos mejorará y que el
conocimiento técnico de nuestros colaboradores se incrementará.
