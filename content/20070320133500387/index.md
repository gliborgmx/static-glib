+++
title = "Linux clústers - Parte 1/3"
slug = "20070320133500387"
date = "2007-03-20T12:35:00-06:00"
[taxonomies]
tema = ["articulos"]
autor = ["Juan Caballero"]
+++

Para iniciar la ronda de artículos que Ceyusa nos solicitó, me he dado a la
tarea de narrarles en una serie de tres artículos sobre la experiencia de
construir y hacer funcionar un clúster usando Linux como sistema operativo y
utilizando como ejemplo un clúster de 21 máquinas que estoy montando. En esta
primera parte veremos lo referente a conceptos básicos, el diseño y
requerimientos físicos y el arranque bajo el LiveCD ParallelKnoppix

<!-- more -->

¿Qué es un clúster?

- Alto rendimiento (High Performance)
- Alta disponibilidad (High Availability)
- Equilibrio de carga (Load Balancing)
- Escalabilidad (Scalability)

¿Qué necesito?

- **Nodos**. Sirven cualquier tipo de máquinas que hasta pueden ser de desecho,
  y lo más básico que se imaginen, solo requerimos que posean procesador,
  memoria, tarjeta de red y si de preferencia disco duro. Claro que entre más
  nodos tengamos más capacidad de cómputo tendremos, pero cuidado con el tipo de
  máquina que se colocan, no es lo mismo colocar un Pentium I a 100MHz que un
  CoreDuo a 2GHz, de preferencia usen nodos clónicos o de similar capacidad para
  que el balanceo de carga sea adecuado.
- **Sistema de red**. Si bien podemos usar sistemas como fibra óptica o mirynet
  que son de alta velocidad, el precio se eleva demasiado, actualmente la
  mayoría de las computadoras soporta e incluye red Ethernet 10/100/1000 y con
  un switch de cuantos puertos necesitemos basta para la mayoría de las
  aplicaciones. Existe un desarrollo para activarlas por conexiones WiFi, pero
  como no las he probado y las velocidades no se comparan, solo trataremos redes
  físicas.
- **Sistema operativo**. Por supuesto que Linux pero en cuanto a la distribución
  a usar tenemos toda una batería para escoger, es más, se puede transformar su
  distribución favorita en un sistema para súper-computo instalando los paquetes
  adecuados, pero por comodidad prefieran las distribuciones que ya incluyen
  este soporte.
- **Aplicaciones de funcionamiento**. El manejador de balanceo, sistemas de
  colas, soporte a MPI/LAM, etc. En las distribuciones que vienen listas para
  clustering ya las traen preparas para usarse.
- **Aplicaciones finales**. Pues depende de que uso le van a dar: para
  renderizar imágenes, cálculos matemáticos, rippear un DVD, codificar a OGG su
  biblioteca musical, etc. Muchas aplicaciones ya traen soporte para sistemas de
  clustering o sino tiene toda la libertad de crear las suyas y probar su
  clúster.

Caso práctico: **BlackMamba**

- Procesador: 2 Intel Xeon @ 1.6GHz
- Memoria: 2 Gb
- Disco Duro: 150 Gb
- Tarjeta de Red: Ethernet 10/100/1000 y Wifi Atheros
- Tarjeta de vídeo: NVidia QuadroPro 128Mb

ParallelKnoppix

Autor: Juan Caballero (linxe (arroba) glib . org . mx)
