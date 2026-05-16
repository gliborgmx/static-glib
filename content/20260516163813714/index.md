+++
title = "¿Quién es djb?"
slug = "20260516163813714"
date = "2026-05-16T16:38:16.667395+02:00"
[taxonomies]
autor = ["Víctor Manuel Jáquez Leal"]
tema = ["articulos"]
[extra]
og_image = "djb.jpg"
+++

Continuando el tema de grandes programadores que iniciamos con [Fabrice
Bellard])[@/202508102102.md], ahora hablemos sobre otro grande de la profesión
que personalmente me ha inspirado y su software contribuyó a generar mis
primeros ingresos como consultor: Daniel J. Bernstein.

Mi primer producto como consultor era instalar un servicio de correo
electrónico, basado en [QMail](https://cr.yp.to/qmail.html), con LDAP como base
de datos de usuarios. Con QMail, obviamente, llegue a Daniel J. Bernstein,
conocido en la comunidad de software simplemente como `djb`.

Daniel J. Bernstein nació el 29 de octubre de 1971 en East Patchogue, Nueva
York. Matemático, criptólogo y programador, es una de las figuras más
influyentes en la seguridad informática moderna y un firme defensor del software
de dominio público.

<!-- pyml disable-next-line line-length-->
{{ figure(src="djb.jpg" alt="Daniel J. Bernstein" caption="Daniel J. Bernstein ([origen](https://www.youtube.com/watch?v=1svxNxG6hHc))")}}

Bernstein mostró desde temprana edad un talento excepcional para las
matemáticas. Se graduó de la preparatoria Bellport en Long Island a los 15 años,
y ese mismo año quedó en quinto lugar en el Westinghouse Science Talent Search.
A los 16, obtuvo un lugar entre los diez mejores en la competencia matemática
William Lowell Putnam. Estudió la licenciatura en matemáticas en la Universidad
de Nueva York y obtuvo su doctorado en la Universidad de California, Berkeley en
1995, bajo la tutela de Hendrik Lenstra.

A mediados de los años 90, Bernstein comenzó a escribir una serie de programas
diseñados con la seguridad como prioridad absoluta. Entre ellos destacan:

- `qmail` (1995-1998): un servidor de correo electrónico creado como alternativa
  segura a Sendmail. Su arquitectura modular y su diseño minimalista le
  permitieron permanecer libre de vulnerabilidades explotables durante más de
  una década. Fue utilizado por empresas como Yahoo para recibir correo.
- `djbdns` (1999-2001): una implementación del sistema DNS escrita en respuesta
  a las constantes fallas de seguridad de BIND, el servidor DNS dominante en la
  época. Facebook utilizó su componente `tinydns` para publicar direcciones de
  servidores, y OpenDNS usó `dnscache` para atender solicitudes de millones de
  usuarios.
- `daemontools`, `ucspi-tcp`, `publicfile`, `ezmlm`: un ecosistema de
  herramientas complementarias para la gestión de servicios UNIX, conexiones
  TCP, publicación de archivos y listas de correo.

Una característica distintiva de Bernstein fue su postura sobre las licencias.
Inicialmente, distribuyó su software como *libre de licencia* (*license-free*),
lo cual impedía la distribución de versiones modificadas y generó fricciones con
algunas distribuciones de Linux. Sin embargo, en diciembre de 2007 liberó
`qmail` y `djbdns` al dominio público, eliminando toda restricción legal sobre
su uso, modificación y redistribución. Este gesto consolidó su compromiso con la
libertad del software en su forma más pura.

Fue pionero en ofrecer recompensas por el hallazgo de fallos de seguridad en su
software. Durante años ofreció 500 USD (posteriormente elevada a 1000 USD) a
quien encontrara una vulnerabilidad en `qmail` o `djbdns`. En marzo de 2009,
entregó 1000 USD a Matthew Dempsky por descubrir una falla en `djbdns`. Su
convicción, polémica para algunos, es que es posible escribir software
invulnerable si el programador es lo suficientemente disciplinado.

Más allá del software de infraestructura, Bernstein ha realizado contribuciones
fundamentales a la criptografía moderna, muchas de ellas ampliamente desplegadas
en software libre:

- [Salsa20](https://en.wikipedia.org/wiki/Salsa20) y
  [ChaCha20](https://en.wikipedia.org/wiki/Salsa20#ChaCha_variant): cifradores
  de flujo de alta velocidad. `ChaCha20`, combinado con el generador de hashes
  [Poly1305](https://en.wikipedia.org/wiki/Poly1305), fue estandarizado por el
  IETF y es utilizado por Chrome en sus conexiones HTTPS con Google, así como en
  OpenSSH y WireGuard.
- [Curve25519](https://es.wikipedia.org/wiki/Curve25519) y
  [Ed25519](https://es.wikipedia.org/wiki/EdDSA#Ed25519): sistemas de curvas
  elípticas para intercambio de claves y firmas digitales. `Curve25519` es usado
  por WhatsApp para cifrado de extremo a extremo, y tanto `Curve25519` como
  `Ed25519` son la base de las operaciones criptográficas de OpenSSH y del
  firmado de paquetes en OpenBSD.
- [SPHINCS+](https://en.wikipedia.org/wiki/SPHINCS%2B): un esquema de firmas
  basado en funciones hash, seleccionado en 2022 como uno de los ganadores del
  concurso de estandarización de criptografía poscuántica del NIST.

En los años 90, Bernstein protagonizó el caso *Bernstein v. United States*, en
el cual demandó al gobierno de Estados Unidos por las restricciones a la
exportación de software criptográfico, argumentando que el código fuente es una
forma de expresión protegida por la Primera Enmienda. La corte falló a su favor,
sentando un precedente fundamental: el software es discurso protegido y las
restricciones nacionales sobre cifrado fueron declaradas inconstitucionales.
Bernstein se representó a sí mismo en el litigio, sin formación jurídica formal.

## Referencias

- Página personal de D. J. Bernstein. <https://cr.yp.to/djb.html>
- Wikipedia. «Daniel J. Bernstein».
  <https://es.wikipedia.org/wiki/Daniel_J._Bernstein>
- Wikipedia. «qmail». <https://es.wikipedia.org/wiki/Qmail>
- LWN.net. «Daniel Bernstein: ten years of qmail security».
  <https://lwn.net/Articles/257004/>
- Simons Institute. «Daniel Bernstein».
  <https://simons.berkeley.edu/people/daniel-bernstein>
- Fixquotes. «Biography of Daniel J. Bernstein».
  <https://fixquotes.com/authors/daniel-j-bernstein/>
