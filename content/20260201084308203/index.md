+++
title = "eBPF: una máquina virtual en el kernel"
slug = "20260201084308203"
date = "2026-02-01T08:43:11.516876+01:00"
[taxonomies]
autor = ["Víctor Manuel Jáquez Leal"]
tema = ["articulos"]
+++

Imagina que pudieras añadir pequeños fragmentos de código directamente al kernel
de Linux mientras está ejecutándose, sin necesidad de reiniciar, recompilar o
tocar el código fuente del sistema operativo. Pues esto es posible con **eBPF**
(Extended Berkeley Packet Filter).

<!-- pyml disable-next-line line-length -->
{{ figure(src="EBPF_logo.png" alt="eBPF logo" caption="Logo del proyecto eBPF [*](https://commons.wikimedia.org/wiki/File:EBPF_logo.png)") }}

### De filtrar paquetes de red a programar el kernel

Todo comenzó en 1992 con el BPF original (Berkeley Packet Filter), creado por
Steven McCanne y Van Jacobson para filtrar eficientemente paquetes de red en
herramientas como `tcpdump`. Era una máquina virtual simple dentro del kernel
que permitía ejecutar programas pequeños para decidir qué paquetes capturar,
evitando copiar todo el tráfico al espacio de usuario. El cambio radical llegó
alrededor de 2014, cuando ingenieros como Alexei Starovoitov de Facebook
comenzaron a extender BPF (de ahí *eBPF*) de manera ambiciosa: ampliaron el
conjunto de instrucciones, añadieron más registros, permitieron mapeos de datos
para comunicarse con el espacio de usuario y, crucialmente, crearon un
verificador de seguridad robusto. Esta evolución, integrada oficialmente en
Linux 3.18, transformó eBPF de un simple filtro de paquetes en una plataforma de
programación genérica y segura para el kernel. Hoy, impulsado por proyectos como
[Cilium](https://cilium.io/) y [BCC](https://github.com/iovisor/bcc), y adoptado
masivamente en la nube, eBPF es un pilar de la infraestructura moderna.

En esencia, eBPF es una máquina virtual dentro del kernel de Linux. Permite
ejecutar programas de forma segura y controlada en respuesta a eventos
específicos del sistema, como una llamada al sistema, un evento de red o una
llamada de función. Piensa en ello como un sistema de *ganchos* (hooks)
programables a nivel del sistema operativo.

<!-- more -->

### ¿Cómo funciona?

1. **Escribes un programa** en un subconjunto restringido de C (o usando
   lenguajes de más alto nivel). Este programa define la lógica que quieres
   ejecutar.
2. **El compilador** (como `clang`) lo traduce a bytecode eBPF.
3. **El verificador del kernel** realiza una rigurosa auditoría de seguridad y
   corrección en tiempo de carga: asegura que el programa no tenga bucles
   infinitos, que no acceda a memoria fuera de sus límites y que finalice
   siempre. Es el guardián de la estabilidad del sistema.
4. **Si pasa la verificación**, el bytecode se **compila Just-In-Time (JIT)** a
   código de máquina nativo para máximo rendimiento y se adjunta al "gancho" o
   evento elegido.

El kernel ejecuta tu código automáticamente cada vez que ocurre ese evento. El
overhead es mínimo (nanosegundos), lo que lo hace viable para producción.

### Un "Hola Mundo"

Vamos a un ejemplo práctico y ejecutable. Instalaremos `bpftrace`, una
herramienta de alto nivel que abstrae gran parte de la complejidad de eBPF,
ideal para prototipado y exploración.

¡Recuerda! No hagas este ejercicio directamente sobre tu sistema, hazlo dentro
una máquina virtual con QEMU.

Dependencia básica (en Ubuntu/Debian):

```bash
sudo apt update && sudo apt install -y bpftrace
```

El programa `contador-llamadas.bt`:

```cpp
#!/usr/bin/env bpftrace

// Este es un programa eBPF que cuenta todas las llamadas al sistema
// y muestra un resumen cada 2 segundos.

tracepoint:syscalls:sys_enter_*
{
    @llamadas[probe] = count(); // Incrementa un contador para este syscall específico
}

interval:s:2
{
    printf("\n--- Conteo de llamadas al sistema (últimos 2 segundos) ---\n");
    print(@llamadas);
    clear(@llamadas);
}
```

Para ejecutarlo (necesitarás permisos de root para interactuar con el kernel):

```bash
sudo bpftrace contador-llamadas.bt
```

Verás una salida dinámica que se actualiza cada 2 segundos, mostrando un
histograma de todas las llamadas al sistema que tu máquina está realizando (como
`open`, `read`, `write`).

¡Felicidades! Acabas de ejecutar tu primer programa eBPF.

Este pequeño script es una potente herramienta de observabilidad, dándote
visibilidad instantánea sobre la actividad del kernel.

{{ asciinema(file="ebpf.cast", id="clone") }}

### Usos comunes del eBPF

Sus casos de uso principales son:

1. Observabilidad y Monitoreo de Rendimiento (Monitoring):
   * Herramientas como `bpftrace` (que ya usamos), `BCC` (Binary Collection
     Compiler) y `sysdig`/`falco` permiten crear perfiles de rendimiento a bajo
     nivel en tiempo real.
   * Se puede rastrear la latencia de E/S de disco, el uso de la CPU por
     función, las contenciones de bloqueo (`lock contention`) o el rendimiento
     de la red, todo sin recompilar o reiniciar aplicaciones. Proyectos como
     [Pixie](https://docs.px.dev/about-pixie/pixie-ebpf/) o
     [Parca](https://www.parca.dev/) usan eBPF para crear mapas de dependencias
     de servicios y perfiles continuos.

2. Redes y Rendimiento (Networking):
   * Cilium es el caso de éxito más conocido. Utiliza eBPF para reemplazar
     completamente el stack de networking tradicional de Kubernetes (iptables,
     kube-proxy), ofreciendo enrutamiento de red, balanceo de carga, políticas
     de seguridad y visibilidad con un overhead muchísimo menor y una lógica más
     inteligente.
   * Se puede implementar cortafuegos (firewalls) de capa 7 (HTTP,
     [gRPC](https://grpc.io/)) con lógica compleja, directamente en el kernel, a
     velocidades de línea.

3. Seguridad y Aplicación de Políticas (Security):
   * [Falco](https://falco.org/) actúa como un *detector de intrusiones* para tu
     sistema. Usa eBPF para supervisar la actividad del kernel (llamadas al
     sistema, actividad de red, actividad de archivos) en busca de
     comportamientos sospechosos (por ejemplo, un contenedor que intenta
     ejecutar un shell, o un proceso que modifica un archivo binario crítico) y
     genera alertas.
   * Se pueden crear políticas de seguridad basadas en el comportamiento, no
     solo en usuarios o puertos.

### Problemas y riesgos potenciales

Ninguna tecnología es una bala de plata, y eBPF tiene sus desafíos:

1. **Complejidad y Barrera de Entrada:** Programar directamente en eBPF a bajo
   nivel es complejo. Requiere un profundo conocimiento del kernel Linux y sus
   estructuras de datos internas. Afortunadamente, herramientas como `bpftrace`
   y bibliotecas de más alto nivel (`libbpf`) están reduciendo esta barrera.
2. **Verificador Estricto:** El verificador, aunque crucial para la seguridad,
   puede ser difícil de satisfacer. Programas lógicamente válidos pueden ser
   rechazados si el verificador no puede probar matemáticamente que son seguros,
   lo que puede frustrar a los desarrolladores.
3. **Fragmentación y Compatibilidad:** Los programas eBPF dependen de estructuras
   de datos internas del kernel (`kernel headers`). Un cambio en una nueva
   versión del kernel puede romperlos. La comunidad ha creado prácticas como el
   **Compile Once - Run Everywhere (CO-RE)** para mitigar esto, pero sigue
   siendo un punto de atención.
4. **Seguridad y Mal Uso Potencial:** Aunque el verificador es excelente, no es
   perfecto. En el pasado, se han encontrado vulnerabilidades que permitían
   "escapar" del entorno seguro de eBPF y comprometer el kernel. Además, en
   manos equivocadas, eBPF es una herramienta de observabilidad tan poderosa que
   puede convertirse fácilmente en un **rootkit de nivel kernel** prácticamente
   indetectable para herramientas tradicionales, haciendo que su propia
   fortaleza sea también un riesgo de seguridad si un atacante obtiene
   privilegios suficientes para cargar código.
5. **Overhead y Estabilidad:** Aunque el overhead por evento es minúsculo,
   **instrumentar todo** (cada paquete de red, cada llamada al sistema) en un
   sistema muy cargado puede sumar y consumir recursos de CPU. Hay que usarlo
   con criterio.

### Conclusión

eBPF ha pasado de ser un simple filtro de paquetes a convertirse en un *sistema
operativo programable dentro del sistema operativo*. Amplía el acceso a las
capacidades del kernel, permitiendo a ingenieros de plataforma y desarrolladores
crear herramientas de observabilidad, redes y seguridad altamente eficientes y
personalizadas sin necesidad de modificar el núcleo.

Es una tecnología fundamental que está detrás de la infraestructura de *la
nube*. Como cualquier herramienta compleja, requiere comprensión de sus
mecanismos y límites. Empezar con herramientas de alto nivel como `bpftrace` es
la mejor manera de experimentar su magia sin ahogarse en la complejidad.

### Referencias

* **Documentación Oficial y Comunidad:**
  * [eBPF.io](https://ebpf.io/) - El portal principal con documentación,
    proyectos y noticias.
  * [BPF and XDP Reference Guide
    Cilium](https://docs.cilium.io/en/stable/bpf/) - Una guía técnica excelente
    y profunda.
* **Herramientas y Ejemplos:**
  * [BPF Compiler Collection (BCC)](https://github.com/iovisor/bcc) - Conjunto
     de herramientas y ejemplos listos para usar.
  * [bpftrace (Repositorio)](https://github.com/iovisor/bpftrace) - Lenguaje de
    alto nivel para eBPF. Su [Guía de
     referencia](https://github.com/iovisor/bpftrace/blob/master/docs/reference_guide.md)
    es oro molido.
* **Aprendizaje Práctico:**
  * [Brendan Gregg's Blog](https://www.brendangregg.com/ebpf.html) - La fuente
    principal de ejemplos y casos de uso de rendimiento. Imprescindible.
* **Historia y Contexto:**
  * [The BSD Packet Filter: A New Architecture for User-level Packet Capture (1992)](https://www.tcpdump.org/papers/bpf-usenix93.pdf)
    \- El artículo original de McCanne y Jacobson.
  * [A thorough introduction to eBPF (LWN.net)](https://lwn.net/Articles/740157/)
    \- Un excelente artículo técnico que cubre la historia y evolución.
