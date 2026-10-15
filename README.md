# Portfolio · Nora Galparsoro

Web: <https://ngalparsoro.github.io> (castellano) · [/eu/](https://ngalparsoro.github.io/eu/) · [/en/](https://ngalparsoro.github.io/en/)

Seis proyectos de ciencia de datos, IA y desarrollo web, cada uno contado en un vídeo de unos tres minutos.
HTML y CSS a mano, sin frameworks ni paso de compilación en GitHub: lo que hay en el repositorio es lo que se publica.

## Estructura

```
construir.py        textos en tres idiomas → index.html, eu/index.html, en/index.html, sitemap.xml, robots.txt
estilo.css          estilos (paleta y letras de las portadas de los vídeos; modo oscuro)
portfolio.js        al reproducir un vídeo se paran los demás
videos/             <proyecto>-<idioma>.mp4 (H.264, 1080p, sin sonido, con el índice al principio)
portadas/           el fotograma del segundo 3 de cada vídeo (scripts/portada.swift)
og-<idioma>.jpg     la imagen que sale al compartir el enlace (scripts/og.py)
fuentes/            Montserrat, Inter e IBM Plex Mono alojadas aquí (licencia OFL: fuentes/LICENCIAS.txt)
```

## Cambiar algo

Los textos están en `construir.py` (`SITIO`, `PROYECTOS`, `OTROS`; la trayectoria en `EXPERIENCIA`, `FORMACION` y
`LENGUAS`). Después:

```bash
python3 construir.py
python3 -m http.server 8799     # → http://localhost:8799
```

Un vídeo nuevo o cambiado: se copia como `videos/<proyecto>-<idioma>.mp4`, se saca su portada y se vuelve a construir
(la duración se lee del propio vídeo):

```bash
swiftc -O -o /tmp/portada scripts/portada.swift
/tmp/portada videos/clima-es.mp4 portadas/clima-es.jpg 3 1280
```

Cada versión de un vídeo se queda en el historial de git; mejor cambiarlos pocas veces y de una vez.

Si cambia el titular de la portada o el orden de los proyectos, también la imagen que sale al compartir el enlace
(necesita Pillow, fontTools y brotli):

```bash
python3 scripts/og.py
```

## Estadísticas

Cloudflare Web Analytics, sin cookies: visitas por página, procedencia, país y dispositivo. La clave del sitio está en
`ANALITICA_TOKEN` (`construir.py`); vacía, las páginas salen sin el script y con la CSP cerrada.
