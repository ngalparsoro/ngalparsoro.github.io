"""
La imagen que sale al compartir el enlace (og-<idioma>.jpg, 1200 × 630): titular de la portada y las
portadas de los seis vídeos, en el orden de la página. Toma los textos de construir.py.

Necesita Pillow, fontTools y brotli (para leer las .woff2):

    python3 scripts/og.py
"""
import io
import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFilter, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from construir import IDIOMAS, PROYECTOS, SITIO  # noqa: E402

W, H = 1200, 630
MARGEN = 64
NARANJA = '#f2a03a'
LINEAS = {
    'es': ('Seis proyectos, cada uno', 'contado en un vídeo'),
    'eu': ('Sei proiektu, bakoitza', 'bideo batean kontatua'),
    'en': ('Six projects, each one', 'told in a video'),
}


def ttf(nombre):
    """La .woff2 de fuentes/ como TrueType en memoria, para Pillow."""
    f = TTFont(RAIZ / 'fuentes' / f'{nombre}.woff2')
    f.flavor = None
    datos = io.BytesIO()
    f.save(datos)
    return datos.getvalue()


FUENTES = {n: ttf(n) for n in ('montserrat', 'inter', 'ibm-plex-mono')}


def letra(nombre, tam, peso=None):
    f = ImageFont.truetype(io.BytesIO(FUENTES[nombre]), tam)
    if peso:
        f.set_variation_by_axes([peso])
    return f


def ceja_que_cabe(texto, ancho):
    """La ceja en mayúsculas, del cuerpo más grande (17 → 13) que quepa en el ancho."""
    for tam in range(17, 12, -1):
        f = letra('ibm-plex-mono', tam)
        if f.getlength(texto) <= ancho:
            return f
    return f


def imagen(lang):
    im = Image.new('RGB', (W, H), '#16171b')
    brillo = Image.new('L', (W, H), 0)
    ImageDraw.Draw(brillo).ellipse((-200, -260, 520, 360), fill=90)
    im = Image.composite(Image.new('RGB', (W, H), '#7a4a1c'), im, brillo.filter(ImageFilter.GaussianBlur(120)))
    d = ImageDraw.Draw(im)

    w, h, hueco = 256, 144, 12
    x0, y0 = W - MARGEN - 2 * w - hueco, (H - 3 * h - 2 * hueco) // 2

    ceja = SITIO[lang]['ceja'].upper()
    d.text((MARGEN, 150), ceja, font=ceja_que_cabe(ceja, x0 - MARGEN - 24), fill=NARANJA)
    d.text((MARGEN, 186), 'Nora', font=letra('montserrat', 76, 800), fill='#ffffff')
    d.text((MARGEN, 272), 'Galparsoro', font=letra('montserrat', 76, 800), fill=NARANJA)
    for i, linea in enumerate(LINEAS[lang]):
        d.text((MARGEN, 384 + 36 * i), linea, font=letra('inter', 28, 400), fill='#d6d8de')
    d.text((MARGEN, 520), 'ngalparsoro.github.io', font=letra('ibm-plex-mono', 17), fill='#8b8f99')

    for i, p in enumerate(PROYECTOS):
        portada = Image.open(RAIZ / 'portadas' / f'{p["id"]}-{lang}.jpg').resize((w, h), Image.LANCZOS)
        mascara = Image.new('L', (w, h), 0)
        ImageDraw.Draw(mascara).rounded_rectangle((0, 0, w - 1, h - 1), 10, fill=255)
        x, y = x0 + (i % 2) * (w + hueco), y0 + (i // 2) * (h + hueco)
        d.rounded_rectangle((x - 1, y - 1, x + w, y + h), 11, outline='#33363d')
        im.paste(portada, (x, y), mascara)
    return im


if __name__ == '__main__':
    for lang in IDIOMAS:
        destino = RAIZ / f'og-{lang}.jpg'
        imagen(lang).save(destino, quality=86, optimize=True)
        print(destino.name)
