+++
title = "ActivityPub: el protocolo que teje el fediverso"
slug = "20260614153340566"
date = "2026-06-14T15:33:40.870628+02:00"
draft = false
[taxonomies]
autor = ["Víctor Manuel Jáquez Leal"]
tema = ["articulos"]
+++

A mediados de 2026, si alguien pide instrucciones para abrirse una cuenta en una
red social, la respuesta ya no es unívoca. Hay quien recomienda Mastodon. Hay
quien prefiere Bluesky. Hay quien, con una ceja levantada, sugiere volver a los
blogs con RSS. Detrás de esa fragmentación hay una pregunta de fondo: ¿qué hace
que dos servidores, en dos sótanos distintos, en dos países distintos, puedan
intercambiar publicaciones como si pertenecieran al mismo sitio? La respuesta es
*ActivityPub*.

<!-- pyml disable-next-line line-length-->
{{ figure(src="activitypub.png" alt="ActivityPub" caption="ActivityPub. Hecho con <https://chat.qwen.ai/>")}}

## ¿Qué es ActivityPub?

ActivityPub es un [protocolo de
comunicación](https://es.wikipedia.org/wiki/Protocolo_de_comunicaciones)
publicado como [Recomendación del
W3C](https://es.wikipedia.org/wiki/World_Wide_Web_Consortium) en enero de 2018.
Define cómo servidores independientes pueden intercambiar contenido social, como
publicaciones, comentarios, reacciones, sin que exista una autoridad central que
coordine la comunicación.

El protocolo fue desarrollado por el Grupo de Trabajo de la Web Social del W3C,
con contribuciones de personas como Evan Prodromou, creador de GNU Social y
coautor de la especificación. Su nombre original era ActivityPump, pero terminó
como ActivityPub para evocar la idea de publicación cruzada entre plataformas.

Técnicamente, ActivityPub se apoya en dos pilares:

- [ActivityStreams 2.0](https://www.w3.org/TR/activitystreams-core/), un
  vocabulario en [JSON-LD](https://es.wikipedia.org/wiki/JSON-LD) que describe
  actores, actividades y objetos. Un actor puede ser una persona, un bot o un
  grupo; una actividad puede ser `Create`, `Follow`, `Like` o `Announce`; un
  objeto puede ser una nota, una imagen, un video o un evento.
- Dos puntos de acceso HTTP por cada actor: un `inbox` (buzón de entrada) y un
  `outbox` (buzón de salida). Para publicar algo, un cliente envía una actividad
  al `outbox` de su servidor. Para federar, el servidor entrega esa actividad a
  al `inbox` de los servidores de las personas seguidoras.

La federación ocurre de forma casi invisible para quien publica: escribe en su
instancia, y su servidor se encarga de propagar el contenido al resto del
[fediverso](https://es.wikipedia.org/wiki/Fediverso).

## El ecosistema del fediverso

ActivityPub es el estándar que articula el fediverso, una red de plataformas
independientes pero interoperables. Cada plataforma ofrece una experiencia
distinta, pero todas comparten el mismo protocolo:

- Mastodon es la implementación más conocida. Con más de 10.5 millones de
  cuentas registradas y entre 750 mil y un millón de usuarias activas mensuales
  en 2026, funciona como una alternativa federada a Twitter/X. Sigue siendo
  software libre, escrito en Ruby.
- Pixelfed es la alternativa a Instagram: compartición de imágenes, sin
  publicidad ni algoritmo de recomendación. En 2026 ronda las 104 mil usuarias
  activas mensuales.
- PeerTube ofrece alojamiento de video descentralizado, con alrededor de 44 mil
  usuarias activas.
- Lemmy compite en el espacio de agregación de noticias y foros al estilo
  Reddit, con unas 36 mil usuarias activas.
- WriteFreely y Plume cubren el mundo de los blogs federados.
- BookWyrm permite catalogar y reseñar lecturas, como un Goodreads
  descentralizado.
- Forgejo lleva la federación a las forjas de código, permitiendo que instancias
  independientes interactúen.

Según datos de FediDB y Fediverse Observer de mayo de 2026, el fediverso en su
conjunto tiene más de 12 millones de cuentas registradas y alrededor de un
millón de usuarias activas mensuales sumando todas las plataformas. Mastodon
representa aproximadamente el 73% de esa actividad.

## ¿Quién está usando ActivityPub?

El dato más llamativo de los últimos años no viene de un proyecto comunitario,
sino de Meta. [Threads](https://en.wikipedia.org/wiki/Threads_(social_network)),
la red social de microblogging de Meta lanzada en julio de 2023, adoptó
ActivityPub como capa de interoperabilidad. En 2024 habilitó la federación como
función optativa, y en junio de 2025 añadió un `feed` dedicado al fediverso y
búsqueda de perfiles federados. Con más de 350 millones de usuarias activas
mensuales, Threads es, con diferencia, la mayor implementación de ActivityPub
que existe. Sin embargo, la federación sigue siendo parcial: las respuestas
entre plataformas no están completamente sincronizadas, y la portabilidad de
cuenta pilar teórico del protocolo no existe en Threads.

Otras plataformas con integración de ActivityPub son:

- WordPress, mediante el complemento ActivityPub, permite que cualquier blog se
  convierta en un actor federado.
- Flipboard, la aplicación de agregación de noticias, federó sus cuentas y
  permite interactuar con el fediverso.
- Tumblr anunció su integración, aunque el proyecto se ha pospuesto
  indefinidamente.

Mientras tanto, el W3C formó en enero de 2026 un nuevo Grupo de Trabajo de la
Web Social para actualizar la especificación de ActivityPub. El grupo, presidido
por Darius Kazemi, trabajará hasta 2028 y tiene como objetivo publicar una
versión revisada del estándar que incorpore la experiencia acumulada en casi una
década de implementaciones.

## ¿Cómo se mide el éxito de un protocolo?

Medir el éxito de un protocolo como ActivityPub es más complejo que contar
usuarias. No se trata de una aplicación que compite por atención, sino de una
capa de interoperabilidad. Algunas métricas útiles:

Adopción de implementaciones. Según WMTips, en junio de 2026 ActivityPub está
presente en el 0.03% de todos los sitios web analizados, con 911 sitios
detectados que lo utilizan. Alemania lidera con el 22% de los sitios, seguida de
Estados Unidos (17.5%) y Francia (13.7%). El dominio `.social` concentra el 20%
de las implementaciones.

Usuarias activas. El fediverso ronda el millón de usuarias activas mensuales.
Aunque la cifra palidece frente a los cientos de millones de plataformas
centralizadas, muestra un patrón de "crecimiento en escalones": cada ola
migratoria, tras la compra de Twitter en 2022 y los cambios en la política de
datos de X en 2024-2025, asienta una base de usuarias mayor que la anterior.

Diversidad de plataformas. Un protocolo es exitoso cuando atrae implementaciones
variadas. ActivityPub lo ha conseguido: hay decenas de plataformas distintas que
lo hablan, desde microblogging hasta forjas de código, pasando por video, audio,
fotografía y lecturas. Esta diversidad es quizá el indicador más sólido de salud
del ecosistema.

Interoperabilidad real. Que Meta, con Threads, y WordPress, con su complemento,
hayan apostado por ActivityPub en lugar de crear silos propietarios adicionales
es un voto de confianza en el estándar. Sin embargo, la interoperabilidad sigue
siendo asimétrica: Threads no permite portabilidad de cuenta y mantiene la
federación como una capa optativa, no como fundamento de la plataforma.

Actividad de estandarización. La creación del nuevo Grupo de Trabajo del W3C en
2026 para actualizar ActivityPub indica que el estándar está vivo y que la
comunidad identifica áreas de mejora. Las FEP (Fediverse Enhancement Proposals)
suman decenas de propuestas que extienden el protocolo para cubrir casos como
citas, grupos y moderación.

## Luces y sombras

ActivityPub no es perfecto. La descentralización trae consigo desafíos que las
plataformas centralizadas no enfrentan: el descubrimiento de contenido es
difícil cuando las cuentas están repartidas en miles de servidores
independientes; la migración de cuenta, aunque técnicamente posible, no siempre
preserva todas las relaciones; y la moderación descentralizada depende de la
buena voluntad y la capacidad técnica de cada administradora de instancia.

Además, el protocolo compite con alternativas como el [AT
Protocol](https://en.wikipedia.org/wiki/AT_Protocol) de Bluesky, que en 2026
tiene alrededor de 5.4 millones de usuarias activas mensuales y ofrece una
experiencia de descentralización distinta: autenticación portátil y algoritmos
de recomendación componibles.

A pesar de ello, ActivityPub es el único estándar abierto de redes sociales que
ha alcanzado estatus de Recomendación W3C con un ecosistema de implementaciones
diverso y activo. No es una promesa: es una realidad que lleva ocho años
funcionando.

## Referencias

1. [ActivityPub (W3C Recommendation)](https://www.w3.org/TR/activitypub/)
2. [ActivityPub en Wikipedia](https://es.wikipedia.org/wiki/ActivityPub)
3. [ActivityPub Rocks!](https://activitypub.rocks/)
4. [Guía de ActivityPub en Descentraliza.red](https://descentraliza.red/activitypub/)
5. [Estadísticas de uso de ActivityPub (WMTips, junio 2026)](https://www.wmtips.com/technologies/standards/activitypub/)
6. [El fediverso en cifras (Fediview, 2026)](https://fediview.com/articles/fediverse-in-numbers-mastodon-stats-2026/)
7. [Estadísticas globales de Mastodon (mastoanalytics, mayo 2026)](https://mastodon.social/@mastoanalytics)
8. [Crecimiento del fediverso (PieFed, abril 2026)](https://piefed.zip/c/fedigrow/p/1433591/growth-of-the-fediverse-20260426)
9. [Threads amplía integraciones con la web social abierta (TechCrunch, junio 2025)](https://techcrunch.com/2025/06/17/threads-expands-open-social-web-integrations-with-fediverse-feed-user-profile-search/)
<!-- pyml disable-next-line line-length-->
10. [Informe del fediverso #149: gobernanza del protocolo (Connected Places, enero 2026)](https://connectedplaces.online/reports/fediverse-report-148-on-protocol-governance/)
