# Sitio estático del Grupo Linuxero del Bajío

Históricamente <https://glib.org.mx> ha usado
[GeekLog](https://www.geeklog.net/) como manejador de contenidos (CMS). Sin
embargo, mantener un CMS requiere un esfuerzo de administración que actualmente
no considero necesario, tal como actualizar el CMS, estar pendiente de agujeros
de seguridad de la infraestructura que necesita el CMS (PHP, MySQL, etc.). La
tendencia actual a usar generadores estáticos elimina mucho de este trabajo para
el administrador del servidor.

Este repositorio contiene la migración del <https://glib.org.mx> a un generador
estático en lenguaje [Rust](https://www.rust-lang.org) conocido como
[Zola](https://www.getzola.org).

Mi plan es usar únicamente [HTML
semántico](https://es.wikipedia.org/wiki/HTML_sem%C3%A1ntico) en las plantillas,
y que todo el formato esté en CSS *sin clases*, en este caso con [Pico
CSS](https://picocss.com/).

El mecanismo para colaborar con artículos está aún por definir, aunque
definitivamente la carga de trabajo se traslada a los colaboradores, ya que debe
saber Markdown/[CommonMark](https://spec.commonmark.org) para escribir
contenido, y git para compartir sus textos.

Los grandes ausentes, por lo menos al comienzo, serán los comentarios, aunque en
un futuro podríamos migrarlos y soportarlos a través de [Isso
comments](https://isso-comments.de/), pero eso hay que discutirlo porque
implicarían retornar a los costos de mantenimiento de software.
