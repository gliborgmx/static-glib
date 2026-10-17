+++
title = "GStreamer Conference 2026 en Praga: GstVulkan y GstVA"
slug = "20261017154858700"
date = "2026-10-17T15:49:00.727072+02:00"
[taxonomies]
autor = ["Víctor Manuel Jáquez Leal"]
tema = ["articulos"]
+++

El fin de semana del 10 y 11 de octubre de 2026 se llevó a cabo la decimocuarta
edición de la `GStreamer Conference`, esta vez en Praga, República Checa, en las
instalaciones del `Impact Hub` de Smíchov. Tuve la fortuna de asistir y, además,
de presentar una charla sobre los dos temas a los que dedico buena parte de mi
trabajo: GstVulkan y GstVA.

<!-- pyml disable-next-line line-length-->
{{ <figure page src="gstconf2026.jpg" alt="GStreamer Conference 2026" caption="Foto grupal de la GStreamer Conference 2026. Foto de Francisco Velázquez
([origen](https://social.cologne/@francisv/117428836279859596))" /> }}

## ¿Qué es GStreamer?

Antes de entrar en materia, vale la pena una breve explicación.
[GStreamer](https://es.wikipedia.org/wiki/GStreamer) es un [entorno de
trabajo](https://es.wikipedia.org/wiki/Framework) de código abierto para
construir aplicaciones multimedia: reproducir, grabar, transmitir o convertir
audio y video. Su idea central es la de una
[tubería](https://es.wikipedia.org/wiki/Tuber%C3%ADa_(inform%C3%A1tica)): el
flujo de datos pasa por una cadena de elementos (leer un archivo, decodificar el
video, aplicar un filtro, mostrarlo en pantalla), y las aplicaciones arman sus
propias tuberías conectando los elementos que necesitan. Es la base multimedia
de proyectos como [GNOME](https://es.wikipedia.org/wiki/GNOME), de navegadores
web y de incontables dispositivos, desde cámaras hasta automóviles.

Cada año la comunidad que lo desarrolla se reúne en una conferencia para
presentar avances, discutir problemas y, sobre todo, verse las caras.

## La conferencia

Esta edición ocurrió justo después de la [*Embedded Linux Conference
Europe*](https://events.linuxfoundation.org/embedded-linux-conference-europe/) y
[*Linux Plumbers*](https://lpc.events/event/20/page/266-lpc-2026-overview), lo
que facilitó que mucha gente se quedara el fin de semana en Praga. El programa
fue de dos días intensos, con charlas sobre inteligencia artificial en tuberías
de video, códecs, herramientas de análisis y, por supuesto, el estado del
proyecto. Después de la conferencia hubo un `hackfest` los días 12 y 13 de
octubre, en el mismo lugar, abierto a quien quisiera quedarse a programar y
discutir diseño junto con otros desarrolladores.

Entre las charlas relacionadas con mi trabajo destaco `GstVulkan in Production:
Lessons from the Real World`, de Anders Hellerup Madsen, de la empresa `Veo
Technologies`, donde contó la experiencia de llevar GstVulkan a un producto
real. Es siempre valioso escuchar a quien usa en producción lo que uno
desarrolla de manera más bien teórica.

## Mi charla: GstVA y GstVulkan

El domingo 11 de octubre, a las 11:45, presenté mi charla [*GstVA and GstVulkan
updates*](https://vjaquez.pages.igalia.com/gstreamer-conference-2026/), de
veinte minutos, en la sala 2 del evento. Es una tradición de cada año: repasar
lo ocurrido en los dos complementos que dan acceso a la aceleración por hardware
en GStreamer.

Para situarlos: [Vulkan](https://es.wikipedia.org/wiki/Vulkan_(API)) es la
interfaz de programación moderna del grupo Khronos para trabajar con la [unidad
de procesamiento
gráfico](https://es.wikipedia.org/wiki/Unidad_de_procesamiento_gr%C3%A1fico), y
GstVulkan es la biblioteca de GStreamer que la usa para procesar, decodificar y
codificar video en la GPU. Por su parte, GstVA es el complemento que usa
[VA-API](https://es.wikipedia.org/wiki/Video_Acceleration_API), la interfaz de
Linux para acelerar la codificación y decodificación de video en hardware
dedicado, presente en muchas tarjetas gráficas y procesadores actuales.

Repasé algo más de un año de actividad. En cifras: en GstVulkan hubo 245
*commits* de 23 contribuyentes, que modificaron 110 archivos; en GstVA fueron
80 *commits* de 20 contribuyentes, sobre 43 archivos. Todo esto se integró en
las series 1.26, 1.28 y la rama de desarrollo 1.29.

En el frente de GstVulkan lo más relevante fue:

- `vulkanh264enc`, el codificador de H.264 usando Vulkan Video, integrado en
  julio de 2025 y publicado en la versión 1.28.
- Nuevos decodificadores de [VP9](https://es.wikipedia.org/wiki/VP9)
  (`vulkanvp9dec`) y [AV1](https://es.wikipedia.org/wiki/AOMedia_Video_1)
  (`vulkanav1dec`), cortesía de Stéphane Cerveau y Daniel Almeida.
- Las capacidades de los codificadores y decodificadores ahora se generan
  dinámicamente a partir de lo que reporta el *driver*, en vez de listas fijas.
- Una reescritura profunda de la sincronización en la biblioteca de núcleo, con
  `GstVulkanOperation`, semáforos binarios y de tiempo, y detección de
  características de Vulkan 1.4.
- Mejoras en `vulkancolorconvert`, soporte de `AHardwareBuffer` en Android y
  enlace directo con MoltenVK en macOS y iOS.

Sobre lo que falta en GstVulkan: el codificador H.265 (`vulkanh265enc`) ya está
en proceso de revisión, así como la exportación de memoria externa para
interoperar con VA-API, EGL y CUDA.

En el caso de GstVA, las novedades principales fueron:

- `vaoverlaycompositor`, un nuevo elemento de Jakub Adam para componer video
  superpuesto con aceleración por hardware.
- Una reorganización interna de los codificadores, con mejor manejo de los
  *buffers* de salida y mayor robustez frente a *buffers* corruptos o
  desbordados.
- Mejoras en el manejo de [`dmabuf`](https://en.wikipedia.org/wiki/DMA-BUF), con
  mapeo persistente y detección de modificadores lineales.
- Numerosas correcciones en `vapostproc` (metadatos HDR, color de fondo) y en
  `vacompositor`.

Cerré la charla señalando un patrón que me alegra: cada vez más trabajo se
comparte entre ambas pilas. Por ejemplo, hay una propuesta para mover la clase
base de codificadores H.264 a la biblioteca de códecs, de modo que tanto VA como
Vulkan la reutilicen, y quienes revisan un complemento suelen revisar el otro.

## En resumen

Salgo de Praga con la impresión de que el ecosistema multimedia de código
abierto sigue muy vivo: aceleración por hardware que madura, códecs modernos que
se integran, y una comunidad que conversa cara a cara después de meses de
correos y *merge requests*. Agradezco a los organizadores, a los patrocinadores
(Igalia, Centricular, Pexip, Axi, Collabora, fluendo, por mencionar algunos) y a
todas las personas que contribuyen código y revisión.

Si te interesa el detalle, todas las charlas, con sus materiales, están
registradas en el portal del evento, y las láminas de mi presentación están
disponibles públicamente.

## Referencias

- [GStreamer Conference
  2026](https://gstreamer.freedesktop.org/conference/2026/)
- [Programa del evento en Indico](https://indico.freedesktop.org/event/14/)
- [GstVA and GstVulkan
  updates](https://indico.freedesktop.org/event/14/contributions/584/)
- [Transparencias de la
  presentación](https://indico.freedesktop.org/event/14/contributions/584/attachments/414/591/GStreamer_Vulkan_VA.pdf)
