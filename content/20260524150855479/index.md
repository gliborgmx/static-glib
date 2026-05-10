+++
title = "Comparativa de agentes de codificación en la terminal"
slug = "20260524150855479"
date = "2026-05-24T15:08:08.512430+02:00"
[taxonomies]
autor = ["Víctor Manuel Jáquez Leal"]
tema = ["articulos"]
[extra]
og_image = "coding-agents.png"
+++

Desde hace unos meses, en GitHub, y otros repositorios públicos, hay una
explosión de *pull requests*, con etiquetas en el mensaje de *commit*,
expresando que en dicha modificación intervino un agente de programación. Pero
¿qué son estos agentes?

## ¿Qué es un coding agent?

<!-- pyml disable-next-line line-length-->
{{ figure(src="coding-agents.png" alt="Coding Agents" caption="Agentes de programación. Hecho con <https://chat.qwen.ai/>")}}

Un *coding agent* o agente de programación es un programa que utiliza un [modelo
de lenguaje](https://es.wikipedia.org/wiki/Modelo_de_lenguaje_grande) (LLM) para
trabajar en una base de código de forma autónoma. A diferencia de un
autocompletado como Copilot o un chat como ChatGPT, un agente:

- Lee el código fuente del proyecto para entender su estructura.
- Ejecuta herramientas reales: abre archivos, los edita, corre comandos en la
  [terminal](https://es.wikipedia.org/wiki/Terminal_(inform%C3%A1tica)), usa
  `git` para confirmar cambios.
- Planea múltiples pasos y se adapta si algo falla.
- Puede delegar tareas en subagentes que trabajan en paralelo.
- Respeta un sistema de permisos: pide confirmación antes de modificar archivos
  o ejecutar comandos de riesgo.

Estos agentes habitan la terminal o el editor de código. La persona define el
objetivo y revisa el resultado, mientras el agente ejecuta el ciclo de
desarrollo.

En este artículo revisamos siete agentes de programación que se ejecutan desde
la terminal, cada uno con un enfoque distinto.

## Claude Code

Desarrollado por [Anthropic](https://es.wikipedia.org/wiki/Anthropic), Claude
Code fue el primero en popularizar el formato de agente de terminal. Es un
programa privativo, escrito en TypeScript y Python, que utiliza exclusivamente
los modelos Claude (Sonnet 4.6, Opus 4.6, Haiku 4.5).

Su integración con el ecosistema de Anthropic es profunda: ofrece aplicaciones
de escritorio, extensión para VS Code y JetBrains, sesiones en la nube que
siguen ejecutándose sin la computadora encendida, y un SDK para flujos
personalizados. Soporta el protocolo
[MCP](https://es.wikipedia.org/wiki/Model_Context_Protocol) para conectar
herramientas externas.

El costo parte de 20 USD al mes con el plan Pro, con límites que pueden ser
restrictivos para bases de código grandes. Es la opción más pulida, pero el
bloqueo a un solo proveedor de modelos es su principal limitación.

## Codex

Codex es el agente de programación de OpenAI. Escrito en Rust, es software libre
bajo licencia Apache 2.0 y tiene más de 80 mil estrellas en GitHub.

Funciona en terminal, en una aplicación de escritorio, como extensión de VS
Code, y en la nube desde chatgpt.com. Utiliza los modelos GPT (5.4, 5.3-Codex,
5.5) y está incluido en los planes de ChatGPT Plus, Pro, Business y Enterprise.

Ofrece subagentes, revisión automática de código antes de confirmar cambios,
búsqueda web integrada y un modo de ejecución desatendida para automatización.
Su fortaleza es la integración con el ecosistema de OpenAI y la velocidad de sus
modelos en tareas de código.

## Gemini CLI

Gemini CLI es el agente de [Google](https://es.wikipedia.org/wiki/Google), de
código abierto bajo licencia Apache 2.0. Escrito principalmente en
[TypeScript](https://es.wikipedia.org/wiki/TypeScript), ofrece acceso gratuito
con una cuenta personal de Google: 60 peticiones por minuto y mil por día con
Gemini 2.5 Pro y su ventana de contexto de un millón de *tokens*.

Incluye búsqueda web con Google Search, operaciones con archivos, comandos de
terminal y soporte MCP. Se integra con Gemini Code Assist para usarse también
desde VS Code. Su ventaja más notable es la generosidad del plan gratuito,
aunque la calidad en tareas complejas de código puede ser inferior a la de
Claude o GPT.

## OpenCode

OpenCode es el más popular en GitHub: más de 157 mil estrellas y 460
colaboradores. Es software libre bajo licencia MIT, escrito en TypeScript, y
surgió como alternativa abierta a Claude Code.

Su principal ventaja es que no está atado a ningún proveedor. Soporta 75 o más
proveedores de modelos, incluidos Anthropic, OpenAI, Google, DeepSeek y modelos
locales con Ollama. Incluye integración con GitHub Copilot: si ya se paga la
suscripción de Copilot, se puede usar OpenCode sin costo adicional.

Tiene soporte para 40 o más lenguajes mediante LSP, subagentes, sesiones en
paralelo y una aplicación de escritorio en fase beta. Su arquitectura permite
que un agente se ejecute en una computadora y se controle remotamente desde un
dispositivo móvil.

## Pi

Pi es un agente de programación minimalista para la terminal, creado por Mario
Zechner y mantenido por Earendil Inc. Escrito en TypeScript bajo licencia MIT,
acumula más de 53 mil estrellas en GitHub.

Su filosofía es opuesta a la mayoría: en lugar de incluir cada funcionalidad
como parte del núcleo, Pi delega casi todo a extensiones, *skills*, plantillas
de comandos y temas. El agente base solo ofrece cuatro herramientas: `read`,
`write`, `edit` y `bash`. Lo demás —subagentes, modo de planeación, MCP,
permisos— se construye con extensiones en TypeScript o se instala como paquete
desde npm o git.

Soporta más de 15 proveedores (Anthropic, OpenAI, Google, Azure, Bedrock,
Mistral, Groq, Cerebras, xAI, Hugging Face, Ollama y otros) y permite cambiar de
modelo en mitad de una sesión con `/model` o `Ctrl+L`.

Sus sesiones se almacenan como árboles navegables: se puede volver a cualquier
punto anterior con `/tree` y continuar desde ahí. Las sesiones se exportan a
HTML o se comparten mediante un *gist* de GitHub. Además, permite enviar
mensajes mientras el agente trabaja para corregir el rumbo sin interrumpir la
ejecución.

Pi funciona en cuatro modos: interactivo (TUI), impresión o JSON para
secuencias de comandos, RPC para integraciones con otros procesos, y SDK para
incrustarlo en aplicaciones propias. Su mayor fortaleza es la capacidad de
modificarse a sí mismo durante una sesión: se le puede pedir que construya una
extensión y, tras recargar con `/reload`, queda disponible.

Hace tiempo, hablamos de [moltbot](@/20260221084055135.md), un agente de ámbito
general, no solo de programación, e internamente utiliza Pi.

## Aider

Aider es el más veterano del grupo: nació en mayo de 2023, fue creado por Paul
Gauthier y está escrito en Python bajo licencia Apache 2.0. [Ya habíamos hablado
de él](@/20260124141943218.md) hace un tiempo.

En lugar de copiar el formato de agente de terminal como los demás, Aider se
enfoca en editar código dentro de un repositorio `git`. Cada cambio que realiza
se confirma automáticamente con un mensaje descriptivo, lo que permite deshacer
con `git revert` en cualquier momento. Genera un mapa del repositorio usando
*Tree-sitter* que permite al modelo entender la estructura del proyecto sin leer
cada archivo.

Soporta cientos de modelos mediante LiteLLM y tiene modos especializados como el
modo arquitecto, donde un modelo planea y otro ejecuta los cambios. Incluye
revisión automática con linters, tests automáticos y entrada por voz.

## Maki

Maki es el más reciente y ligero del grupo. Escrito en Rust por Tony Solomonik
bajo licencia MIT, tiene alrededor de 140 estrellas en GitHub, pero propone
ideas novedosas, y es mi preferido actualmente. Hasta he colaborado con un par
de commits.

Su enfoque es la eficiencia de *tokens*: busca reducir el costo y el uso de
contexto sin perder capacidad. Para lograrlo introduce dos herramientas
originales:

`index` usa *Tree-sitter* para generar un esqueleto compacto de cada archivo
(importaciones, tipos, funciones con sus líneas), lo que permite al modelo
entender la estructura sin leer el archivo completo. Según el autor, esto ahorra
165 *tokens* por turno.

`code_execution` es un intérprete dentro de un espacio aislado donde las
herramientas del agente están disponibles como funciones asíncronas. El modelo
escribe un script, lo ejecuta, filtra resultados, y solo esta salida llega al
contexto. Esto puede reducir 40 mil *tokens* a apenas 30 en ciertas tareas.

Además, analiza los comandos de terminal con *Tree-sitter* para entender
exactamente qué se va a ejecutar, y ofrece subagentes con tres niveles de
modelo, memoria persistente entre sesiones, y 26 temas de color en su interfaz
de 60 cuadros por segundo.

Soporta Anthropic, OpenAI, Google, Copilot, Ollama, Mistral, Z.AI, DeepSeek y
Synthetic. Su salida en modo desatendido es compatible con Claude Code.

## Comparación

| Agente | Licencia | Lenguaje | Proveedores | Precio base |
|--------|----------|----------|-------------|-------------|
| Claude Code | Privativa | TypeScript | Solo Anthropic | 20 USD/mes (Pro) |
| Codex | Apache 2.0 | Rust | Solo OpenAI | Incluido en ChatGPT Plus |
| Gemini CLI | Apache 2.0 | TypeScript | Solo Google | Gratis (plan personal) |
| OpenCode | MIT | TypeScript | 75+ proveedores | Gratis (API key o Copilot) |
| Pi | MIT | TypeScript | 15+ proveedores | Gratis (API key) |
| Aider | Apache 2.0 | Python | Cientos (LiteLLM) | Gratis (API key) |
| Maki | MIT | Rust | 9 proveedores | Gratis (API key) |

Cada agente tiene su razón de ser. Claude Code es la opción más madura, pero
encierra en un solo proveedor. Codex aprovecha la velocidad de los modelos más
recientes de OpenAI. Gemini CLI ofrece la capa gratuita más generosa. OpenCode
gana en libertad de elección y comunidad. Aider encaja como un colaborador
disciplinado en flujos `git`. Pi lleva la extensibilidad al extremo: casi nada
está predefinido porque casi todo se puede construir. Maki apuesta por la
eficiencia de *tokens*, una preocupación real cuando los costos se acumulan.

La decisión depende de qué modelos se prefieran, cuánto se quiera gastar y qué
tanto se valore la libertad frente a la integración. Lo que comparten todos es
que están cambiando la forma de programar: el código se describe, el agente lo
ejecuta y la persona revisa, decide y aprende.

## Referencias

[1] Anthropic (2026). *Claude Code overview*.
<https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview>

[2] OpenAI (2026). *Codex CLI*.
<https://developers.openai.com/codex/cli>

[3] Google (2026). *Gemini CLI: your open-source AI agent*.
<https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-cli-open-source-ai-agent/>

[4] OpenCode (2026). *OpenCode documentation*.
<https://opencode.ai/docs/>

[5] Pi (2026). *Pi Coding Agent*.
<https://pi.dev/>

[6] Aider (2026). *AI pair programming in your terminal*.
<https://aider.chat/>

[7] Maki (2026). *Maki: the efficient coder*.
<https://maki.sh/>

[8] Repositorio de Claude Code.
<https://github.com/anthropics/claude-code>

[9] Repositorio de Codex.
<https://github.com/openai/codex>

[10] Repositorio de Gemini CLI.
<https://github.com/google-gemini/gemini-cli>

[11] Repositorio de OpenCode.
<https://github.com/anomalyco/opencode>

[12] Repositorio de Pi.
<https://github.com/earendil-works/pi>

[13] Repositorio de Aider.
<https://github.com/Aider-AI/aider>

[14] Repositorio de Maki.
<https://github.com/tontinton/maki>
