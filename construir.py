"""
Construye el portfolio: una página por idioma (index.html, eu/, en/), sitemap.xml y robots.txt.

Solo biblioteca estándar. Los textos están aquí; los vídeos en videos/<proyecto>-<idioma>.mp4 y sus
portadas en portadas/ (scripts/portada.swift). Cada vez que cambie algo, se vuelve a ejecutar:

    python3 construir.py
"""
import hashlib
import html
import re
import struct
from pathlib import Path

RAIZ = Path(__file__).parent
URL = 'https://ngalparsoro.github.io/'
GITHUB = 'https://github.com/ngalparsoro'
IDIOMAS = ['es', 'eu', 'en']           # el primero va en la raíz
LOCALE = {'es': 'es_ES', 'eu': 'eu_ES', 'en': 'en_GB'}
NOMBRE_IDIOMA = {'es': 'Español', 'eu': 'Euskara', 'en': 'English'}
# Cloudflare Web Analytics (sin cookies). Vacío: sin estadísticas.
ANALITICA_TOKEN = '63fe7f08a7044c90adf6e517d1da597f'

CORREO = 'n.galparsoro@gmail.com'

SITIO = {
    'es': {
        'titulo': 'Nora Galparsoro · Portfolio',
        'descripcion': 'Nora Galparsoro, ingeniera: producción, procesos y datos aplicados a planta. Seis '
                       'proyectos contados en vídeo, trayectoria y contacto.',
        'ceja': 'Producción · Procesos · Datos aplicados a planta',
        'entradilla': 'Ingeniera con más de 10 años dirigiendo producción, procesos y equipos en industria. '
                      'Las dos veces que me he encontrado con información que solo existía de palabra, he '
                      'construido el sistema que la puso por escrito. Aquí, seis proyectos, cada uno contado '
                      'en un vídeo de unos tres minutos.',
        'escribeme': 'Escríbeme',
        'saltar': 'Ir a los proyectos',
        'idiomas': 'Idioma',
        'indice': 'Proyectos',
        'video': 'Vídeo',
        'sin_sonido': 'Vídeo sin sonido',
        'codigo': 'Código en GitHub',
        'mas': 'Más en GitHub',
        'todos': 'Todos los repositorios',
        'trayectoria': 'Trayectoria',
        'experiencia': 'Experiencia',
        'formacion': 'Formación',
        'lenguas': 'Idiomas',
        'contacto': '¿Hablamos?',
        'contacto_texto': 'Busco un puesto de producción u operaciones en el que la digitalización de planta '
                          'forme parte del encargo, no un proyecto aparte que nadie tiene tiempo de llevar.',
        'pie': 'Hecha a mano en HTML y CSS, sin frameworks · alojada en GitHub Pages',
    },
    'eu': {
        'titulo': 'Nora Galparsoro · Portfolioa',
        'descripcion': 'Nora Galparsoro, ingeniaria: ekoizpena, prozesuak eta lantegian aplikatutako datuak. '
                       'Sei proiektu bideoan kontatuak, ibilbidea eta harremana.',
        'ceja': 'Ekoizpena · Prozesuak · Lantegian aplikatutako datuak',
        'entradilla': 'Ingeniaria naiz, eta 10 urte baino gehiago daramatzat industrian ekoizpena, prozesuak '
                      'eta taldeak zuzentzen. Ahoz bakarrik zegoen informazioarekin topo egin dudan bi '
                      'aldietan, hura idatziz jarri duen sistema eraiki dut. Hemen, sei proiektu, bakoitza '
                      'hiru minutu inguruko bideo batean kontatua.',
        'escribeme': 'Idatzidazu',
        'saltar': 'Proiektuetara joan',
        'idiomas': 'Hizkuntza',
        'indice': 'Proiektuak',
        'video': 'Bideoa',
        'sin_sonido': 'Bideoa, soinurik gabe',
        'codigo': 'Kodea GitHub-en',
        'mas': 'Gehiago GitHub-en',
        'todos': 'Biltegi guztiak',
        'trayectoria': 'Ibilbidea',
        'experiencia': 'Esperientzia',
        'formacion': 'Prestakuntza',
        'lenguas': 'Hizkuntzak',
        'contacto': 'Hitz egingo dugu?',
        'contacto_texto': 'Ekoizpen edo operazio arloko lanpostu bat bilatzen dut, lantegiaren digitalizazioa '
                          'enkarguaren parte izango dena, eta ez inork eramateko astirik ez duen aparteko '
                          'proiektu bat.',
        'pie': 'Eskuz egina, HTML eta CSSz, frameworkik gabe · GitHub Pages-en ostatatua',
    },
    'en': {
        'titulo': 'Nora Galparsoro · Portfolio',
        'descripcion': 'Nora Galparsoro, engineer: production, processes and data on the shop floor. Six '
                       'projects told on video, career and contact.',
        'ceja': 'Production · Processes · Data on the shop floor',
        'entradilla': 'Engineer with 10+ years leading production, processes and teams in industry. Both '
                      'times I came across information that only existed by word of mouth, I built the system '
                      'that put it in writing. Here are six projects, each one told in a video of about three '
                      'minutes.',
        'escribeme': 'Get in touch',
        'saltar': 'Skip to projects',
        'idiomas': 'Language',
        'indice': 'Projects',
        'video': 'Video',
        'sin_sonido': 'Silent video',
        'codigo': 'Code on GitHub',
        'mas': 'More on GitHub',
        'todos': 'All repositories',
        'trayectoria': 'Career',
        'experiencia': 'Experience',
        'formacion': 'Education',
        'lenguas': 'Languages',
        'contacto': 'Shall we talk?',
        'contacto_texto': 'I am looking for a production or operations role where shop-floor digitalisation '
                          'is part of the brief, not a side project nobody has time to run.',
        'pie': 'Handmade in HTML and CSS, no frameworks · hosted on GitHub Pages',
    },
}

# En el orden de la página. «titulo» admite <em> (la palabra en color, como en la portada del vídeo);
# el resto es texto. Los textos de ceja, título, subtítulo y meta son los de cada vídeo.
PROYECTOS = [
    {
        'id': 'panel-of',
        'stack': ['Python', 'SQL · Oracle', 'HTML · CSS · JS', 'BI Publisher'],
        'enlaces': [('demo', None, URL + 'panel-de-of/mockup_panel_ofs_v2.html'),
                    ('codigo', None, GITHUB + '/panel-de-of')],
        'es': {
            'corto': 'Panel de OF',
            'ceja': 'Digitalización industrial · Caso real',
            'titulo': 'Panel de <em>OF</em>',
            'sub': 'Órdenes de fabricación en línea, sin tocar el ERP.',
            'meta': 'Planta de mecanizado y montaje · empresa y datos ficticios',
            'demo': 'Abrir el panel',
        },
        'eu': {
            'corto': 'Panel de OF',
            'ceja': 'Industria-digitalizazioa · Benetako kasua',
            'titulo': 'Panel de <em>OF</em>',
            'sub': 'Fabrikazio-aginduak lerroan, ERPa ukitu gabe.',
            'meta': 'Mekanizatu eta muntaia-lantegia · enpresa eta datu fiktizioak',
            'demo': 'Panela ireki',
        },
        'en': {
            'corto': 'Panel de OF',
            'ceja': 'Industrial digitalisation · Real case',
            'titulo': 'Panel de <em>OF</em>',
            'sub': 'Production orders on the line, without touching the ERP.',
            'meta': 'Machining and assembly plant · fictitious company and data',
            'demo': 'Open the panel',
        },
    },
    {
        'id': 'mantenimiento',
        'stack': ['scikit-learn', 'LightGBM', 'Isolation Forest', 'pandas', 'Streamlit'],
        'enlaces': [('codigo', None, GITHUB + '/Milling-Machine-Failure-Prediction')],
        'es': {
            'corto': 'Parada de máquina',
            'ceja': 'Mantenimiento predictivo · Machine learning',
            'titulo': 'Predicción de parada de <em>máquina</em>',
            'sub': 'Un sistema de tres capas que detecta la avería antes de que ocurra, con las señales que '
                   'la máquina ya genera.',
            'meta': 'Proyecto final · Bootcamp de Data Science · junio 2026',
        },
        'eu': {
            'corto': 'Makina-geldialdiak',
            'ceja': 'Mantentze prediktiboa · Machine learning',
            'titulo': 'Makina-geldialdien <em>iragarpena</em>',
            'sub': 'Hiru geruzako sistema bat, matxura gertatu aurretik detektatzen duena makinak berak '
                   'sortzen dituen seinaleekin.',
            'meta': 'Amaierako proiektua · Data Science bootcampa · 2026ko ekaina',
        },
        'en': {
            'corto': 'Machine failure',
            'ceja': 'Predictive maintenance · Machine learning',
            'titulo': 'Machine <em>failure</em> prediction',
            'sub': 'A three-layer system that detects a breakdown before it happens, using the signals the '
                   'machine already produces.',
            'meta': 'Capstone project · Data Science bootcamp · June 2026',
        },
    },
    {
        'id': 'behatokiak',
        'stack': ['Python', 'pandas', 'MapLibre GL', 'JavaScript', 'GitHub Actions', 'Playwright'],
        'enlaces': [('web', 'hautesbehatokia.eus', 'https://hautesbehatokia.eus'),
                    ('web', 'nazioenbehatokia.eus', 'https://nazioenbehatokia.eus')],
        'es': {
            'corto': 'Observatorios electorales',
            'ceja': 'Visualización de datos · Mapas web',
            'titulo': 'Observatorios <em>electorales</em>',
            'sub': 'Dos webs hermanas que convierten los resultados oficiales en mapas interactivos, de '
                   'cada elección y territorio hasta la sección censal.',
            'nota': 'Hauteskunde Behatokia es un proyecto individual: datos, diseño y desarrollo. En el '
                    'Observatorio Electoral de las Naciones, desarrollo y diseño, con la dirección de Ion '
                    'Ansa Mendizabal.',
            'meta': 'Webs públicas · 2026',
        },
        'eu': {
            'corto': 'Hauteskunde-behatokiak',
            'ceja': 'Datu-bistaratzea · Web-mapak',
            'titulo': 'Hauteskunde-<em>behatokiak</em>',
            'sub': 'Emaitza ofizialak mapa interaktibo bihurtzen dituzten bi webgune ahizpa, hauteskunde '
                   'eta lurralde bakoitzeko, sekzio zentsaleraino.',
            'nota': 'Hauteskunde Behatokia banakako proiektua da: datuak, diseinua eta garapena. Nazioen '
                    'Hautes Behatokian, garapena eta diseinua, Ion Ansa Mendizabalen zuzendaritzapean.',
            'meta': 'Webgune publikoak · 2026',
        },
        'en': {
            'corto': 'Election observatories',
            'ceja': 'Data visualisation · Web maps',
            'titulo': 'Election <em>observatories</em>',
            'sub': 'Two sister websites that turn official results into interactive maps, for every '
                   'election and territory, down to the census section.',
            'nota': 'Hauteskunde Behatokia is a solo project: data, design and development. On the Nations '
                    'Electoral Observatory, development and design, directed by Ion Ansa Mendizabal.',
            'meta': 'Public websites · 2026',
        },
    },
    {
        'id': 'mitumi',
        'stack': ['Python', 'Flask', 'FastAPI', 'PostgreSQL', 'Docker', 'Render', 'Groq'],
        'enlaces': [('codigo', None, GITHUB + '/Agentes_Mitumi')],
        'es': {
            'corto': 'MITÜMI',
            'ceja': 'Proyecto de equipo · Cliente real',
            'titulo': 'Agentes de IA para <em>MITÜMI</em>',
            'sub': 'Una plataforma de gestión de eventos con seis agentes de IA: la IA propone y una '
                   'persona valida.',
            'nota': 'Mi parte: integración de los agentes, API y despliegue.',
            'meta': 'Desafío de Tripulaciones · The Bridge · julio 2026',
        },
        'eu': {
            'corto': 'MITÜMI',
            'ceja': 'Talde-proiektua · Benetako bezeroa',
            'titulo': 'AA agenteak <em>MITÜMI</em>rentzat',
            'sub': 'Ekitaldiak kudeatzeko plataforma bat, sei AA agenterekin: AAk proposatu eta pertsona '
                   'batek baliozkotzen du.',
            'nota': 'Nire zatia: agenteen integrazioa, APIa eta hedapena.',
            'meta': 'Desafío de Tripulaciones · The Bridge · 2026ko uztaila',
        },
        'en': {
            'corto': 'MITÜMI',
            'ceja': 'Team project · Real client',
            'titulo': 'AI agents for <em>MITÜMI</em>',
            'sub': 'An event-management platform with six AI agents: the AI proposes, a person approves.',
            'nota': 'My part: agent integration, API and deployment.',
            'meta': 'Desafío de Tripulaciones (crew challenge) · The Bridge · July 2026',
        },
    },
    {
        'id': 'jobscout',
        'stack': ['Python', 'ReAct', 'Groq', 'FastAPI', 'React', 'SQLite'],
        'enlaces': [('codigo', None, GITHUB + '/Agente_JobScout')],
        'es': {
            'corto': 'JobScout',
            'ceja': 'Proyecto final · IA generativa',
            'titulo': 'Job<em>Scout</em>',
            'sub': 'Un agente de IA para buscar empleo.',
            'meta': 'Bootcamp de Data Science e IA · The Bridge · 2026',
        },
        'eu': {
            'corto': 'JobScout',
            'ceja': 'Azken proiektua · AA sortzailea',
            'titulo': 'Job<em>Scout</em>',
            'sub': 'Lana bilatzeko AA agente bat.',
            'meta': 'Data Science eta AA bootcampa · The Bridge · 2026',
        },
        'en': {
            'corto': 'JobScout',
            'ceja': 'Final project · Generative AI',
            'titulo': 'Job<em>Scout</em>',
            'sub': 'An AI agent for job hunting.',
            'meta': 'Data Science & AI Bootcamp · The Bridge · 2026',
        },
    },
    {
        'id': 'clima',
        'stack': ['Python', 'pandas', 'Matplotlib', 'Seaborn', 'SciPy', 'ERA5'],
        'enlaces': [('codigo', None, GITHUB + '/EDA-Weather-Change-in-Basque-Country')],
        'es': {
            'corto': 'Clima de Euskal Herria',
            'ceja': 'Proyecto individual · Análisis exploratorio de datos',
            'titulo': 'El clima de <em>Euskal Herria</em>',
            'sub': '85 años de datos diarios en siete ciudades: ¿cuánto ha cambiado el clima?',
            'meta': '1940–2025 · Bootcamp de Data Science e IA · The Bridge · mayo 2026',
        },
        'eu': {
            'corto': 'Euskal Herriko klima',
            'ceja': 'Banakako proiektua · Datuen analisi esploratzailea',
            'titulo': 'Euskal Herriko <em>klima</em>',
            'sub': '85 urteko eguneroko datuak zazpi hiritan: zenbat aldatu da klima?',
            'meta': '1940–2025 · Data Science eta AA bootcampa · The Bridge · 2026ko maiatza',
        },
        'en': {
            'corto': 'Climate of Euskal Herria',
            'ceja': 'Solo project · Exploratory data analysis',
            'titulo': 'The climate of <em>Euskal Herria</em>',
            'sub': '85 years of daily data in seven cities: how much has the climate changed?',
            'meta': '1940–2025 · Data Science & AI bootcamp · The Bridge · May 2026',
        },
    },
]

# Sin vídeo: al final, en «Más en GitHub».
OTROS = [
    {
        'nombre': 'Sudoku Solver',
        'url': GITHUB + '/Sudoku_Solver_DL',
        'stack': ['YOLOv8', 'OpenCV', 'PyTorch', 'Keras', 'Streamlit'],
        'es': 'De una foto de un sudoku a su solución: detecta el tablero con YOLOv8, lee los dígitos con '
              'una CNN y compara tres motores de resolución, uno clásico y dos aprendidos.',
        'eu': 'Sudoku baten argazkitik bere ebazpenera: taula YOLOv8rekin detektatzen du, digituak CNN '
              'batekin irakurtzen ditu eta hiru ebazpen-motor alderatzen ditu, bat klasikoa eta bi ikasiak.',
        'en': 'From a photo of a sudoku to its solution: it finds the board with YOLOv8, reads the digits '
              'with a CNN and compares three solving engines, one classic and two learned.',
    },
]

# Trayectoria, del CV de 2026 (versión corta). Por idioma: (puesto, dónde, detalle).
# El último fabricante va sin nombre, para no ligar la empresa al Panel de OF.
EXPERIENCIA = [
    {
        'cuando': '2024 – 2025',
        'es': ('Responsable de línea', 'Fabricante industrial, Gipuzkoa',
               'Línea de mecanizado y montaje: 16 personas, hasta 23 en punta, a tres turnos. Más de un 10 % de '
               'mejora en la producción de montaje, sostenida mientras el equipo se recomponía.'),
        'eu': ('Lerroko arduraduna', 'Industria-fabrikatzailea, Gipuzkoa',
               'Mekanizatu eta muntaia-lerroa: 16 pertsona, puntetan 23 arte, hiru txandatan. Muntaiako ekoizpena '
               '% 10 baino gehiago hobetu zen, eta hobekuntzari eutsi zitzaion taldea berrosatzen zen bitartean.'),
        'en': ('Line Manager', 'Industrial manufacturer, Gipuzkoa',
               'Machining and assembly line: 16 people, up to 23 at peak, over three shifts. Assembly output up '
               'by more than 10%, sustained while the team kept changing.'),
    },
    {
        'cuando': '2020 – 2024',
        'es': ('Encargada de taller', 'Ebakilan',
               'Corte, plegado y preprocesado de metal: 50 personas a tres turnos y más de 75 toneladas al día.'),
        'eu': ('Tailerreko arduraduna', 'Ebakilan',
               'Metala ebaki, tolestu eta aurreprozesatzea: 50 pertsona hiru txandatan eta egunean 75 tona baino '
               'gehiago.'),
        'en': ('Workshop Manager', 'Ebakilan',
               'Metal cutting, bending and pre-processing: 50 people over three shifts and more than 75 tonnes a '
               'day.'),
    },
    {
        'cuando': '2018 – 2020',
        'es': ('Oficina técnica', 'Ebakilan',
               'Impulsé la digitalización de la oficina técnica durante la pandemia: del expediente en papel a la '
               'orden en PDF. Sigue en uso seis años después.'),
        'eu': ('Bulego teknikoa', 'Ebakilan',
               'Bulego teknikoaren digitalizazioa bultzatu nuen pandemian: paperezko espedientetik PDFko '
               'agindura. Sei urte geroago oraindik erabiltzen da.'),
        'en': ('Technical Office Engineer', 'Ebakilan',
               'Drove the digitalisation of the technical office during the pandemic: from paper files to PDF '
               'orders. Still in use six years later.'),
    },
    {
        'cuando': '2016 – 2017',
        'es': ('Técnica de calidad y costes', 'Zegama Okindegia',
               'Un sistema de seguimiento de costes por proceso (KPIs) y un nuevo sistema de calidad.'),
        'eu': ('Kalitate eta kostuetako teknikaria', 'Zegama Okindegia',
               'Prozesuko kostuen jarraipen-sistema bat (KPIak) eta kalitate-sistema berri bat.'),
        'en': ('Quality & Cost Technician', 'Zegama Okindegia',
               'A process-based cost-monitoring system (KPIs) and a new quality system.'),
    },
    {
        'cuando': '2011 – 2015',
        'es': ('Concejala de Infraestructuras y Servicios Urbanos', 'Ayuntamiento de Donostia',
               'Segunda teniente de alcalde: unos 70 M€ al año y cerca de 100 personas. La recogida selectiva de '
               'residuos pasó del 37 % al 49 %.'),
        'eu': ('Azpiegitura eta Hiri Zerbitzuetako zinegotzia', 'Donostiako Udala',
               'Bigarren alkateordea: urtean 70 M€ inguru eta ia 100 pertsona. Hondakinen gaikako bilketa % 37tik '
               '% 49ra igo zen.'),
        'en': ('City Councillor for Infrastructure & Urban Services', 'Donostia City Council',
               'Second Deputy Mayor: around €70M a year and nearly 100 staff. Separate waste collection rose from '
               '37% to 49%.'),
    },
]

# Por idioma: (título, dónde).
FORMACION = [
    {
        'cuando': '2026',
        'es': ('Bootcamp de Data Science e Inteligencia Artificial', 'The Bridge'),
        'eu': ('Data Science eta Adimen Artifizialeko bootcampa', 'The Bridge'),
        'en': ('Data Science & Artificial Intelligence Bootcamp', 'The Bridge'),
    },
    {
        'cuando': '2015 – 2016',
        'es': ('Máster en Innovación Empresarial y Dirección de Proyectos', 'Mondragon Unibertsitatea'),
        'eu': ('Enpresa Berrikuntza eta Proiektuen Zuzendaritzako Masterra', 'Mondragon Unibertsitatea'),
        'en': ("Master's in Business Innovation & Project Management", 'Mondragon University'),
    },
    {
        'cuando': '2016',
        'es': ('CAPM · Certified Associate in Project Management', 'PMI'),
        'eu': ('CAPM · Certified Associate in Project Management', 'PMI'),
        'en': ('CAPM · Certified Associate in Project Management', 'PMI'),
    },
    {
        'cuando': '2004 – 2008',
        'es': ('Ingeniería Técnica en Diseño Industrial y de Producto', 'Mondragon Unibertsitatea'),
        'eu': ('Industria eta Produktu Diseinuko Ingeniaritza Teknikoa', 'Mondragon Unibertsitatea'),
        'en': ('Technical Engineering in Industrial & Product Design', 'Mondragon University'),
    },
]

LENGUAS = {
    'es': 'Euskera (EGA) y castellano, nativos · inglés avanzado (First Certificate; dos años en Edimburgo)',
    'eu': 'Euskara (EGA) eta gaztelania, ama-hizkuntzak · ingelesa, maila aurreratua (First Certificate; bi '
          'urte Edinburgon)',
    'en': 'Basque (EGA) and Spanish, native · advanced English (First Certificate; two years in Edinburgh)',
}


def duracion(video):
    """Segundos del vídeo, leídos del átomo mvhd (los vídeos llevan el índice al principio)."""
    datos = video.read_bytes()[:1 << 20]
    i = datos.find(b'mvhd')
    if i < 0:
        raise SystemExit(f'{video}: sin mvhd en el primer MB')
    if datos[i + 4] == 1:
        escala, dur = struct.unpack('>IQ', datos[i + 24:i + 36])
    else:
        escala, dur = struct.unpack('>II', datos[i + 16:i + 24])
    return dur / escala


def mmss(segundos):
    s = round(segundos)
    return f'{s // 60}:{s % 60:02d}'


def huella(ruta):
    return hashlib.sha256((RAIZ / ruta).read_bytes()).hexdigest()[:10]


def sin_etiquetas(texto):
    return re.sub(r'<[^>]+>', '', texto)


def url_idioma(lang):
    return URL if lang == IDIOMAS[0] else f'{URL}{lang}/'


def pagina(lang):
    t = SITIO[lang]
    e = html.escape
    pre = '' if lang == IDIOMAS[0] else '../'
    v_css, v_js = huella('estilo.css'), huella('portfolio.js')
    if ANALITICA_TOKEN:
        csp_cf = (" https://static.cloudflareinsights.com", "; connect-src 'self' https://cloudflareinsights.com")
        analitica = (f'\n<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
                     f'data-cf-beacon=\'{{"token": "{ANALITICA_TOKEN}"}}\'></script>')
    else:
        csp_cf, analitica = ('', ''), ''

    alternos = '\n'.join(f'<link rel="alternate" hreflang="{l}" href="{url_idioma(l)}">' for l in IDIOMAS)
    idiomas = '\n'.join(
        f'<li><a href="{pre}{"" if l == IDIOMAS[0] else l + "/"}" lang="{l}" hreflang="{l}" '
        f'title="{NOMBRE_IDIOMA[l]}"{" aria-current=\"page\"" if l == lang else ""}>{l.upper()}</a></li>'
        for l in IDIOMAS)
    indice = '\n'.join(f'<li><a class="p-{p["id"]}" href="#{p["id"]}">{e(p[lang]["corto"])}</a></li>'
                       for p in PROYECTOS)

    articulos = []
    for p in PROYECTOS:
        x = p[lang]
        video = f'videos/{p["id"]}-{lang}.mp4'
        dur = mmss(duracion(RAIZ / video))
        enlaces = []
        for tipo, etiqueta, href in p['enlaces']:
            texto = etiqueta or (x['demo'] if tipo == 'demo' else t['codigo'])
            enlaces.append(f'<a class="boton boton-{tipo}" href="{href}">{e(texto)}<span aria-hidden="true">↗</span></a>')
        nota = f'\n<p class="nota">{e(x["nota"])}</p>' if 'nota' in x else ''
        stack = ''.join(f'<li>{e(s)}</li>' for s in p['stack'])
        articulos.append(f'''<article class="proyecto p-{p["id"]}" id="{p["id"]}" aria-labelledby="t-{p["id"]}">
<figure class="video">
<video controls muted playsinline preload="none" width="1280" height="720" poster="{pre}portadas/{p["id"]}-{lang}.jpg" aria-label="{t["video"]}: {e(sin_etiquetas(x["titulo"]))}">
<source src="{pre}{video}" type="video/mp4">
</video>
<figcaption>{t["sin_sonido"]} · {dur}</figcaption>
</figure>
<div class="texto">
<p class="ceja">{e(x["ceja"])}</p>
<h2 id="t-{p["id"]}">{x["titulo"]}</h2>
<p class="sub">{e(x["sub"])}</p>{nota}
<p class="meta">{e(x["meta"])}</p>
<ul class="stack">{stack}</ul>
<p class="enlaces">{"".join(enlaces)}</p>
</div>
</article>''')

    otros = '\n'.join(f'''<li>
<h3><a href="{o["url"]}">{e(o["nombre"])}<span aria-hidden="true">↗</span></a></h3>
<p>{e(o[lang])}</p>
<ul class="stack">{"".join(f"<li>{e(s)}</li>" for s in o["stack"])}</ul>
</li>''' for o in OTROS)

    experiencia = '\n'.join(
        f'<li><p class="cuando">{x["cuando"]}</p><p class="puesto">{e(x[lang][0])} '
        f'<span class="donde">· {e(x[lang][1])}</span></p><p class="detalle">{e(x[lang][2])}</p></li>'
        for x in EXPERIENCIA)
    formacion = '\n'.join(
        f'<li><p class="cuando">{x["cuando"]}</p><p class="puesto">{e(x[lang][0])} '
        f'<span class="donde">· {e(x[lang][1])}</span></p></li>'
        for x in FORMACION)

    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self'; media-src 'self'; style-src 'self'; font-src 'self'; script-src 'self'{csp_cf[0]}{csp_cf[1]}; base-uri 'none'; form-action 'none'">
<title>{e(t["titulo"])}</title>
<meta name="description" content="{e(t["descripcion"])}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#16171b">
<link rel="canonical" href="{url_idioma(lang)}">
{alternos}
<link rel="alternate" hreflang="x-default" href="{URL}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(t["titulo"])}">
<meta property="og:description" content="{e(t["descripcion"])}">
<meta property="og:url" content="{url_idioma(lang)}">
<meta property="og:image" content="{URL}og-{lang}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{LOCALE[lang]}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="preload" href="{pre}fuentes/montserrat.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{pre}fuentes/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pre}estilo.css?v={v_css}">
<script src="{pre}portfolio.js?v={v_js}" defer></script>{analitica}
</head>
<body>
<a class="saltar" href="#proyectos">{t["saltar"]}</a>
<header class="portada">
<nav class="barra" aria-label="{t["idiomas"]}">
<a class="marca" href="{pre}{"" if lang == IDIOMAS[0] else lang + "/"}">Nora Galparsoro</a>
<ul class="idiomas">
{idiomas}
</ul>
</nav>
<div class="portada-texto">
<p class="ceja">{e(t["ceja"])}</p>
<h1>Nora <span>Galparsoro</span></h1>
<p class="entradilla">{e(t["entradilla"])}</p>
<p class="contacto">
<a class="boton boton-acento" href="mailto:{CORREO}">{t["escribeme"]}</a>
<a class="boton boton-claro" href="#trayectoria">{t["trayectoria"]}</a>
<a class="boton boton-claro" href="{GITHUB}">GitHub<span aria-hidden="true">↗</span></a>
</p>
</div>
<nav class="indice" aria-label="{t["indice"]}">
<ol>
{indice}
</ol>
</nav>
</header>
<main id="proyectos">
{chr(10).join(articulos)}
<section class="otros" aria-labelledby="t-otros">
<h2 id="t-otros">{t["mas"]}</h2>
<ul>
{otros}
</ul>
<p><a class="boton" href="{GITHUB}?tab=repositories">{t["todos"]}<span aria-hidden="true">↗</span></a></p>
</section>
<section class="trayectoria" id="trayectoria" aria-labelledby="t-trayectoria">
<h2 id="t-trayectoria">{t["trayectoria"]}</h2>
<div class="columnas">
<div>
<h3>{t["experiencia"]}</h3>
<ol class="hitos">
{experiencia}
</ol>
</div>
<div>
<h3>{t["formacion"]}</h3>
<ol class="hitos">
{formacion}
</ol>
<h3>{t["lenguas"]}</h3>
<p class="lenguas">{e(LENGUAS[lang])}</p>
</div>
</div>
</section>
</main>
<section class="cierre" id="contacto" aria-labelledby="t-contacto">
<div class="cierre-dentro">
<h2 id="t-contacto">{t["contacto"]}</h2>
<p>{e(t["contacto_texto"])}</p>
<p class="correo"><a href="mailto:{CORREO}">{CORREO}</a></p>
<p><a class="boton boton-claro" href="{GITHUB}">GitHub<span aria-hidden="true">↗</span></a></p>
</div>
</section>
<footer class="pie">
<p>© 2026 Nora Galparsoro · {t["pie"]}</p>
</footer>
</body>
</html>
'''


def main():
    for lang in IDIOMAS:
        for p in PROYECTOS:
            for f in (f'videos/{p["id"]}-{lang}.mp4', f'portadas/{p["id"]}-{lang}.jpg'):
                if not (RAIZ / f).exists():
                    raise SystemExit(f'falta {f}')
        destino = RAIZ / ('index.html' if lang == IDIOMAS[0] else f'{lang}/index.html')
        destino.parent.mkdir(exist_ok=True)
        destino.write_text(pagina(lang), encoding='utf-8')
        print(destino.relative_to(RAIZ))

    urls = '\n'.join(f'  <url><loc>{url_idioma(l)}</loc></url>' for l in IDIOMAS)
    (RAIZ / 'sitemap.xml').write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n', encoding='utf-8')
    (RAIZ / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {URL}sitemap.xml\n', encoding='utf-8')


if __name__ == '__main__':
    main()
