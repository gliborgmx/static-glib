+++
title = "x86CSS: un CPU x86 funcional hecho únicamente con CSS"
slug = "20260510080116947"
date = "2026-05-10T08:01:16.851635+02:00"
[taxonomies]
autor = ["Víctor Manuel Jáquez Leal"]
tema = ["articulos"]
[extra]
og_image = "x86CSS.png"
+++

Imagina que estás viendo un videojuego. Mueves a tu personaje, saltas
obstáculos, recoges monedas. Todo eso que ves en pantalla es el resultado de
miles de cálculos por segundo que realiza el procesador de tu computadora. Ahora
imagina que esos mismos cálculos, en vez de ejecutarse en un chip de silicio, se
ejecutan dentro de una hoja de estilos [Cascading Style
Sheets](https://es.wikipedia.org/wiki/CSS). Suena a broma, pero es exactamente
lo que logró Lyra Rebane en febrero de 2026 con
[x86CSS](https://lyra.horse/x86css/): un
[CPU](https://es.wikipedia.org/wiki/Unidad_central_de_procesamiento) compatible
con la arquitectura [x86](https://es.wikipedia.org/wiki/X86) de 16 bits que
funciona íntegramente con CSS, sin una sola línea de JavaScript.

## De estilos a instrucciones de máquina

CSS nació a finales de los años noventa como un lenguaje para dar estilo visual
a documentos [HTML](https://es.wikipedia.org/wiki/HTML): colores, fuentes,
márgenes, animaciones sencillas. Nadie en su sano juicio pensaba en usarlo para
cómputo de propósito general. Pero con el paso de las décadas, el estándar fue
acumulando funcionalidades que, combinadas de forma creativa, permiten
representar y manipular estado.

El proyecto de Rebane toma un programa escrito en
[C](https://es.wikipedia.org/wiki/C_(lenguaje_de_programaci%C3%B3n)), lo compila
con [GCC](https://es.wikipedia.org/wiki/GNU_Compiler_Collection) a código de
máquina nativo para el [Intel 8086](https://es.wikipedia.org/wiki/Intel_8086),
el procesador que IBM eligió para su primera PC en 1981, y luego traduce cada
byte de ese binario a reglas CSS. El resultado es una página web que, al abrirse
en un navegador basado en Chromium, ejecuta el programa sin intervención humana.

La página de demostración incluye tres programas: la [sucesión de
Fibonacci](https://es.wikipedia.org/wiki/Sucesi%C3%B3n_de_Fibonacci), el
[triángulo de Pascal](https://es.wikipedia.org/wiki/Tri%C3%A1ngulo_de_Pascal) y
un juego de palabras llamado *Horsle*, una parodia de Wordle donde la palabra
siempre es «horse».

<!-- pyml disable-next-line line-length-->
{{ figure(src="x86CSS.png" alt="Una hoja de estilo CSS transformándose en transistores de un chip x86" caption="CSS convertido en CPU") }}

## ¿Cómo funciona sin JavaScript?

El núcleo de la emulación descansa en tres características modernas de CSS:

- **Animaciones como reloj:** una animación `@keyframes` que se repite
  indefinidamente actúa como la señal de reloj del CPU. En cada ciclo, el
  navegador revalúa las reglas y avanza un paso de ejecución.
- **Consultas de estilo como lógica condicional:** las *style container queries*
  (`@container style()`) permiten que una regla CSS examine el valor de una
  propiedad personalizada y decida qué hacer en función de ese valor. Es el
  equivalente a una instrucción `if`.
- **Propiedades personalizadas como registros y memoria:** cada registro del
  8086 (`AX`, `BX`, `CX`, etc.) y cada celda de memoria se almacenan en
  variables CSS (`--AX`, `--BX`, `--m0`, `--m1`…). La unidad aritmético-lógica
  se implementa con expresiones `calc()` y las nuevas funciones `if()`.

El proyecto usa además las funciones personalizadas `@function`, otra novedad de
CSS que permite definir bloques reutilizables de lógica.

## Sin JavaScript, en serio

La página incluye una etiqueta `<script>` mínima que proporciona un reloj basado
en JavaScript para mejorar la estabilidad y velocidad de la emulación. Pero si
deshabilitas JavaScript en tu navegador, el emulador sigue funcionando: el CSS
contiene su propia implementación del reloj usando únicamente animaciones.

Este detalle es importante porque existe un debate técnico sobre si los sistemas
que requieren interacción humana (como mover el ratón) cuentan realmente como
[Turing completos](https://es.wikipedia.org/wiki/Turing_completo). Rebane quiso
que su CPU funcionara sin ninguna intervención del usuario, cerrando así esa
discusión.

## Genealogía de las computadoras en CSS

x86CSS no surgió de la nada. En 2023, Jane Ori publicó el *CPU Hack*: una
técnica que usa animaciones CSS y el selector `:hover` para crear un ciclo
continuo de cómputo. Rebane toma esa idea y la lleva al extremo: en lugar de
implementar una máquina sencilla, emula directamente la arquitectura x86, con su
mapa de opcodes, sus modos de direccionamiento y su lógica de segmentación de
memoria.

El proyecto implementa la mayoría de las instrucciones del 8086. No todas,
algunas banderas como el *carry flag* no están modeladas, pero las suficientes
para que programas reales compilados con GCC funcionen correctamente. La
estrategia de desarrollo fue pragmática: escribir programas en C, compilarlos
con distintas optimizaciones, e implementar solo las instrucciones que el
compilador generaba.

## No es práctico, y eso está bien

La propia autora lo admite: si quieres rendimiento, es mejor escribir
directamente en CSS sin emular un CPU completo. Un emulador de este tipo ejecuta
unas pocas instrucciones por segundo, mientras que un CPU real ejecuta miles de
millones.

Pero la utilidad no era el objetivo. x86CSS es una demostración de que los
límites entre presentación y cómputo son más difusos de lo que parecen. Es una
obra de arte técnico y una invitación a repensar lo que significa «programar».

## ¿Puedo ejecutar mis propios programas?

Sí. El repositorio incluye un script en Python (`build_css.py`) que toma un
archivo binario con código 8086 y genera el HTML con las reglas CSS
correspondientes. Si quieres escribir en C, puedes usar `gcc-ia16`, un
compilador cruzado que genera binarios para el 8086. Por defecto hay 1.5kB de
memoria, ampliables modificando el script.

## Para cerrar

Cuando Alan Turing definió su máquina teórica en 1936, probablemente no imaginó
que ochenta años después alguien demostraría que un lenguaje para dar color y
forma a páginas web también puede ejecutar cualquier cálculo concebible.
`x86CSS` es el recordatorio más extremo de que la computación no le pertenece a
ningún lenguaje ni plataforma: emerge donde haya reglas, estado y un reloj que
marque el paso del tiempo.

Si quieres verlo en acción, visita
[lyra.horse/x86css](https://lyra.horse/x86css/) en un navegador basado en
Chromium. El código fuente está disponible en
[GitHub](https://github.com/rebane2001/x86CSS) bajo la licencia GPLv3.

## Referencias

- [Expert CSS: The CPU Hack](https://dev.to/janeori/expert-css-the-cpu-hack-4ddj),
  de Jane Ori (2023).
- [CSS is Turing Complete](https://mooninaut.github.io/css-is-turing-complete/),
  de Clement Cherlin (2022-2025).
- [You no longer need JavaScript](https://lyra.horse/blog/2025/08/you-dont-need-js/),
  publicación en el blog de Lyra Rebane (2025).
