+++
title = "John Carmack: el programador que redefinió los videojuegos"
slug = "20260629071242974"
date = "2026-06-29T07:13:01.771503+02:00"
[taxonomies]
autor = ["Víctor Manuel Jáquez Leal"]
tema = ["articulos"]
+++

En 1991, cuatro jóvenes programadores fundaron en Madison, Wisconsin, una
compañía llamada `id Software`. Su primera oficina era un pequeño apartamento
sobre un consultorio médico. Ninguno de ellos imaginaba que, dos años después,
el mundo de la computación cambiaría para siempre. El responsable técnico de ese
cambio fue [John Carmack](https://es.wikipedia.org/wiki/John_Carmack), el más
joven del equipo, con apenas 21 años.

<!-- pyml disable-next-line line-length-->
{{ figure(src="JohnCarmack.jpg" alt="John Carmack" caption="John Carmack en el GDC del 2010 <https://commons.wikimedia.org/wiki/File:John_Carmack_GDC_2010.jpg>")}}

Carmack nació el 20 de agosto de 1970 en [Shawnee
Mission](https://en.wikipedia.org/wiki/Shawnee_Mission,_Kansas),
[Kansas](https://es.wikipedia.org/wiki/Kansas). Desde niño mostró un interés
inusual por las computadoras. Durante la preparatoria mantuvo un promedio
perfecto de 4.0, pero la rigidez del sistema escolar no le resultaba atractiva.
Tras un breve paso de dos semestres por la [Universidad de Missouri en Kansas
City](https://en.wikipedia.org/wiki/University_of_Missouri–Kansas_City), donde
solo tomó clases de [ciencias de la
computación](https://es.wikipedia.org/wiki/Ciencias_de_la_computaci%C3%B3n),
decidió abandonar la carrera para dedicarse de lleno a la programación.

En la empresa [`Softdisk`](https://en.wikipedia.org/wiki/Softdisk), en
Shreveport, Luisiana, conoció a [John
Romero](https://es.wikipedia.org/wiki/John_Romero), [Tom
Hall](https://en.wikipedia.org/wiki/Tom_Hall) y [Adrian
Carmack](https://es.wikipedia.org/wiki/Adrian_Carmack) (sin parentesco). Juntos
crearon el juego `Commander Keen`, publicado bajo el modelo
[*shareware*](https://es.wikipedia.org/wiki/Shareware) en 1990. Este modelo de
distribución, donde una porción del juego se regalaba y el resto se vendía, se
convertiría en el sello comercial de `id Software`.

## El nacimiento del disparo en primera persona

El primer gran hito técnico de Carmack llegó con `Wolfenstein 3D` en 1992. El
juego implementaba un [motor
gráfico](https://es.wikipedia.org/wiki/Motor_de_videojuego) capaz de renderizar
entornos tridimensionales en tiempo real usando una técnica conocida como [*ray
casting*](https://es.wikipedia.org/wiki/Ray_casting). Aunque el motor limitaba
el movimiento a planos bidimensionales, lograba algo que parecía imposible en
una computadora personal de la época: simular la experiencia de caminar dentro
de un espacio tridimensional.

Pero fue `Doom`, lanzado en 1993, lo que transformó la industria. Carmack
escribió un motor completamente nuevo que introdujo varias innovaciones:

- [*Binary Space
  Partitioning*](https://es.wikipedia.org/wiki/Partici%C3%B3n_binaria_del_espacio)
  (BSP): una estructura de datos que dividía el mapa en árboles binarios para
  determinar qué superficies debían dibujarse y en qué orden, resolviendo
  eficientemente el problema de la visibilidad.
- Iluminación por sectores: cada zona del mapa podía tener su propio nivel de
  luz, creando atmósferas oscuras que contribuían a la sensación de inmersión.
- Texturas en pisos y techos: a diferencia de `Wolfenstein 3D`, que solo
  mostraba colores sólidos, `Doom` aplicaba imágenes a cada superficie,
  multiplicando el realismo visual.

El impacto fue inmediato. En 1995 se estimaba que `Doom` estaba instalado en más
computadoras que el recién estrenado `Windows 95`. Su código fuente fue liberado
en 1997, permitiendo que una comunidad de aficionados creara modificaciones y
nuevos niveles. Esta práctica de liberar el código se volvió una tradición en
`id Software` y contribuyó a que los motores de Carmack se estudiaran en
universidades de todo el mundo.

## `Quake` y la tercera dimensión real

En 1996, `Quake` dio el salto definitivo. Por primera vez, el motor abandonaba
los [*sprites*](https://es.wikipedia.org/wiki/Sprite_(videojuegos))
bidimensionales y representaba cada elemento del mundo usando polígonos
tridimensionales. Los jugadores podían mirar hacia arriba y hacia abajo. Todo
era verdaderamente 3D.

Las contribuciones técnicas de `Quake` fueron profundas:

- [Mapas de luz](https://en.wikipedia.org/wiki/Lightmap) (*lightmaps*): Carmack
  introdujo el precálculo de iluminación. La luz se calculaba una sola vez y se
  almacenaba en texturas especiales que se aplicaban a las superficies del
  mundo. Esto permitía iluminación compleja (sombras suaves, iluminación
  indirecta) sin costo computacional durante la ejecución del juego.
- Caché de superficies (*surface caching*): en lugar de recalcular cada
  superficie en cada cuadro, el motor almacenaba las superficies ya procesadas.
  Solo si una superficie cambiaba (por ejemplo, al recibir iluminación dinámica)
  se reconstruía. [Michael
  Abrash](https://es.wikipedia.org/wiki/Michael_Abrash), coautor del motor,
  documentó este sistema en detalle.
- Iluminación dinámica: añadida en una sola hora de programación por Carmack,
  permitía que explosiones y disparos iluminaran temporalmente el entorno.

El motor de `Quake` también introdujo el concepto de [*cliente-servidor* en el
multijugador](https://es.wikipedia.org/wiki/Cliente-servidor) con predicción de
movimiento, sentando las bases técnicas del juego competitivo en red.

## El reverso de Carmack

Una de las anécdotas más famosas sobre Carmack involucra una técnica de
renderizado de sombras. Durante la investigación posterior a `Quake II`, Carmack
trabajaba con [*stencil shadow
volumes*](https://en.wikipedia.org/wiki/Shadow_volume) (volúmenes de sombra
usando búferes de esténcil). El problema era que cuando la cámara entraba dentro
de un volumen de sombra, esta desaparecía en gran parte de la pantalla. Carmack
descubrió de forma independiente que se podía invertir la prueba de profundidad
--usando *z-fail* en lugar de *z-pass*-- para resolver el problema. Esta técnica
sería conocida como *Carmack's Reverse* y se convertiría en pieza central del
motor de `Doom 3` (2004).

Irónicamente, la empresa `Creative Labs` patentó este algoritmo en 2002. `id
Software` negoció un acuerdo para poder usarlo sin pagar regalías, pero el
episodio ejemplifica las tensiones entre la innovación abierta y el sistema de
[patentes de *software*](https://es.wikipedia.org/wiki/Patente_de_software) que
el propio Carmack ha criticado en múltiples ocasiones.

## Del espacio virtual al espacio real

En paralelo a su trabajo en videojuegos, Carmack fundó `Armadillo Aerospace` en
el año 2000, una empresa dedicada a desarrollar cohetes reutilizables. El equipo
compitió en los torneos de la [Fundación X
Prize](https://es.wikipedia.org/wiki/Fundación_X-Prize) y la
[NASA](https://es.wikipedia.org/wiki/NASA), aplicando la misma mentalidad de
iteración rápida que caracterizaba su trabajo en `id Software`.

En 2013 dejó la compañía que había cofundado para unirse a `Oculus VR` como
director de tecnología. Su trabajo fue fundamental para el desarrollo del casco
`Oculus Rift` y sentó las bases de la realidad virtual moderna. Cuando
`Facebook` adquirió `Oculus` en 2014, Carmack continuó impulsando la plataforma
hasta 2022, cuando dejó la empresa (ya renombrada `Meta`) para dedicarse a la
[inteligencia artificial
general](https://es.wikipedia.org/wiki/Inteligencia_artificial_general) (AGI)
con su nueva compañía `Keen Technologies`.

## El programador como artesano

¿Qué distingue a John Carmack de otros programadores? En primer lugar, su
enfoque en los fundamentos. Carmack no usaba motores de terceros: escribía cada
línea de código desde cero, estudiando los principios matemáticos y físicos que
subyacen al cómputo gráfico. En segundo lugar, su disciplina de trabajo: es
conocido por programar sesiones de ochenta horas semanales con una concentración
absoluta. En tercer lugar, su convicción por el [código
abierto](https://es.wikipedia.org/wiki/C%C3%B3digo_abierto): liberar el código
de sus motores no fue un gesto altruista, sino una decisión estratégica que creó
comunidades, mercados y oportunidades alrededor de su trabajo.

Hoy, a sus 55 años, Carmack sigue explorando nuevos horizontes. Su legado no
solo está en los juegos que millones de personas han disfrutado, sino en las
técnicas, estructuras de datos y algoritmos que todo motor gráfico moderno debe
conocer. John Carmack demostró que la programación no es únicamente una
ingeniería: es también un oficio artesanal donde la excelencia técnica es su
propia recompensa.

## Referencias

- Kushner, D. (2003). *Masters of Doom: How Two Guys Created an Empire and
  Transformed Pop Culture*. Random House.
- Abrash, M. (1997). *Michael Abrash's Graphics Programming Black Book*.
  Coriolis Group. [Versión en
  HTML](https://www.jagregory.com/abrash-black-book/).
- Sanglard, F. (2018). *Game Engine Black Book: DOOM*. Independiente.
- Sanglard, F. (2022). *Game Engine Black Book: Wolfenstein 3D*. Independiente.
- [id Tech en Wikipedia](https://es.wikipedia.org/wiki/Id_Tech)
- [Doom engine en Wikipedia](https://es.wikipedia.org/wiki/Doom_engine)
