+++
title = "Contenedores en Linux"
slug = "20260106070405392"
date = "2026-01-06T07:04:05.344807+01:00"
[taxonomies]
autor = ["Víctor Manuel Jáquez Leal"]
tema = ["articulos"]
[extra]
og_image = "containers.jpg"
+++

Hace unos meses, una amiga me preguntó qué tan importante es incluir
*contenedores* en un programa de formación superior en computación. Desde su
punto de vista, enseñar a configurar servicios sin contenerización era
suficiente. Mi postura es la contraria, y en este texto intentaré explicarla.
Aunque [ya se ha hablado de contenedores aquí](@/20211022210304340.md), creo que
vale la pena reiterar y profundizar un poco.

{{ figure(src="containers.jpg" alt="Contenedores" caption="Contenedores") }}

Normalmente es suficiente saber instalar y configurar Apache, un servidor SMTP,
una base de datos como PostgreSQL, etc. Se suele asumir que un servidor es una
computadora física: si la hackean, todo falla; si un servicio consume demasiada
RAM, CPU o disco, todo falla; si el ancho de banda es insuficiente, todo falla;
si una actualización rompe una dependencia, hay que buscar soluciones
complicadas que ponen en riesgo todo el sistema.

Esto puede funcionar en sistemas modestos, más cercanos a un pasatiempo que a un
entorno profesional. Sin embargo, una solución a estos y otros problemas es la
*contenerización*:

> La contenerización es el **empaquetado** de código de software con solo las
> bibliotecas del sistema operativo y las dependencias necesarias para ejecutar
> el código con el fin de crear un único ejecutable ligero, denominado
> contenedor, que se ejecuta de forma coherente en cualquier infraestructura.
> [🔗](https://www.ibm.com/es-es/think/topics/containerization)

La contenerización añade un nivel adicional de complejidad a los sistemas. Por
eso, considero que estos conceptos y prácticas deberían aprenderse lo antes
posible, incluso durante la formación superior.

<!-- more -->

Decimos que añade complejidad porque estamos acostumbrados a manejar software
con todos los recursos del hardware disponibles a través del sistema operativo.
En cambio, con los contenedores, el software se ejecuta dentro de un *runtime*
que permite controlar a alto nivel los recursos que cada contenedor utiliza.

Para entender por qué el software es como es, ayuda revisar su historia.

Podemos remontarnos a 1979, cuando Unix V7 introdujo `chroot`, o a 2000 con las
`jail` de FreeBSD, a 2005 con OpenVZ o a 2008 con LXC. Pero el uso de
contenedores explotó a partir de 2013 con Docker.
[🔗](https://www.aquasec.com/blog/a-brief-history-of-containers-from-1970s-chroot-to-docker-2016/)

Otra tecnología clave para su masificación fue **Kubernetes**, la plataforma de
orquestación de contenedores por excelencia, que automatiza el despliegue,
escalado y gestión de aplicaciones. Kubernetes permitió popularizar conceptos
como *cloud computing* y *software as a service*.

Pero los contenedores no solo se usan en la nube. En mi caso, como desarrollador
de un proyecto grande como **WebKit**, dada la complejidad de su entorno, para
garantizar que las pruebas se ejecuten de manera consistente usamos [un
contenedor](https://github.com/Igalia/webkit-container-sdk), con todas las
herramientas y dependencias necesarias, independientemente del sistema
operativo. Otro ejemplo es **Flatpak**, que sirve para distribuir, instalar y
usar aplicaciones de escritorio para Linux, empaquetadas como contenedores. Hoy,
muchos desarrolladores prefieren distribuir su software a través de Flatpak,
común a todas las distribuciones, en lugar de crear paquetes RPM o DEB.

Volviendo al tema: tras el éxito de Docker surgieron múltiples soluciones para
crear, gestionar y distribuir contenedores, a menudo incompatibles entre sí.
Incluso Microsoft añadió soporte para contenedores en Windows. Para evitar la
fragmentación, en 2015 se creó la [Open Container
Initiative](https://opencontainers.org/) (OCI) bajo el paraguas de la Linux
Foundation, con el fin de definir estándares que permitan la interoperabilidad
entre contenedores de distintos proveedores.

Las especificaciones suelen ofrecer una visión conceptual más clara que los
productos concretos. Las de la OCI son tres:

- Especificación del *runtime*
  [🔗](https://specs.opencontainers.org/runtime-spec)
  - Define la configuración, entorno de ejecución y ciclo de vida de un
    contenedor.
- Especificación de *image* [🔗](https://specs.opencontainers.org/image-spec/):
  - Describe los metadatos sobre el contenido y las dependencias de la imagen,
    incluyendo cambios en las capas del sistema de archivos.
- Especificación de *distribution*
  [🔗](https://specs.opencontainers.org/distribution-spec):
  - Define una API para un protocolo que facilita y estandariza la distribución
    de contenido, principalmente imágenes de contenedores.

La especificación del *runtime* también define lo que es un *contenedor
estándar*:

> El objetivo de un Contenedor Estándar es encapsular un componente de software
> y todas sus dependencias en un formato autodescriptivo y portable, de modo que
> cualquier *runtime* compatible pueda ejecutarlo sin dependencias adicionales,
> independientemente de la máquina subyacente y del contenido del contenedor.

A nivel de kernel, para implementar un *runtime* de contenedores eficiente, se
desarrollaron subsistemas clave:

- namespaces
  - Aíslan recursos del kernel, haciendo que cada conjunto de procesos en un
    *namespace* vea un conjunto único de recursos (procesos, red, sistema de
    archivos, etc.).
- cgroups
  - Limita, contabiliza y aísla el uso de recursos (CPU, memoria, E/S de disco,
    etc.) de un conjunto de procesos.
- union filesystems
  - Permiten superponer varios sistemas de archivos (*branches*) de forma
    transparente, creando un único sistema de archivos virtual donde los
    directorios coincidentes se combinan.

Finalmente, apliquemos estos conceptos a un ejemplo con Docker.

Supongamos que quiero *contenerizar* una aplicación web hecha con **Flask**.
Primero debo crear la *imagen* del contenedor, es decir, el paquete que
contendrá la aplicación y sus dependencias. Para crearla, escribimos un
*manifiesto* con las instrucciones de construcción:

```Dockerfile
FROM python:alpine

# Instalar dependencias
RUN pip install flask

# Copiar la aplicación
COPY hello.py /

# Configuración final
ENV FLASK_APP=hello
EXPOSE 8000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
```

Casi todas las imágenes parten de una distribución básica de Linux. En este
caso, [Alpine](https://www.alpinelinux.org/), una distribución mínima muy usada
en contenedores, con variantes para entornos específicos como Python.

Tras instalar la distribución base, se añaden las dependencias de la aplicación
(solo Flask en este ejemplo). Luego, se copia la aplicación al directorio
correspondiente. Finalmente, se indica cómo ejecutarla.

Para construir la imagen en Docker, usamos:

```sh
docker image build -t hello:0.1 .
```

Este comando hace que el demonio de Docker genere la imagen y la almacene en su
repositorio interno. Podemos listar las imágenes disponibles con:

```sh
docker image list
```

Para ejecutar la aplicación como contenedor:

```sh
docker container run -p 8000:8000 hello:0.1
```

Entre los parámetros, el mapeo de puertos indica que el puerto 8000 del
contenedor se expone en el mismo puerto del sistema.

Para listar los contenedores en ejecución:

```sh
docker container list
```

Cada contenedor tiene un identificador único (*container id*) que se usa para
gestionarlo.

Para detener un contenedor:

```sh
docker container stop <container id>
```

Un contenedor detenido sigue disponible para reiniciarse. Para eliminarlo:

```sh
docker container rm <container id>
```

Finalmente, para eliminar una imagen del repositorio:

```sh
docker image rm hello:0.1
```

Y eso es todo. Gracias por leer hasta aquí. Espero que te haya sido útil.
Recuerda que este es solo un ejemplo y Docker es una herramienta más. Lo
importante son los conceptos, que se aplican de forma similar en otros sistemas
como [podman](https://podman.io/) o [flatpak](https://flatpak.org/).
