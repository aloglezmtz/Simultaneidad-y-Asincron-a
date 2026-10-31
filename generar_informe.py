"""Genera informe/Practica5_Asincronia_Informe.pdf con el estilo de la Práctica 4.

Antes de ejecutar:  python experimento.py   (crea resultados/ y figs/)
Uso (desde la raíz del repo):  python informe/generar_informe.py
Requiere: reportlab, pandas, pillow y (opcional, para colorear el código) pygments.
"""
import os

import pandas as pd
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, Image, KeepTogether, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle)

# ------------------------------- DATOS DE PORTADA ------------------------------ #
NOMBRE = "GONZALEZ MARTINEZ ALONDRA GORETTI"
NOMBRE_CORTO = "Gonzalez Martinez Alondra Goretti"
CODIGO = "218534681"
PROFESOR = "Mtro. Zeus Cobián"
MATERIA = "Programación paralela y concurrente"
FECHA = "6 de noviembre del 2026"
# ------------------------------------------------------------------------------- #

_aqui = os.path.dirname(os.path.abspath(__file__))
# Funciona con las carpetas (informe/, resultados/, figs/) y también con todos los archivos sueltos en la raíz.
RAIZ = os.path.dirname(_aqui) if os.path.basename(_aqui) == "informe" else _aqui


def R(*p):
    anidado = os.path.join(RAIZ, *p)
    plano = os.path.join(RAIZ, p[-1])
    if os.path.exists(anidado):
        return anidado
    return plano if os.path.exists(plano) else anidado


_NOMBRE_PDF = "Practica5_Asincronia_Informe.pdf"
SALIDA = (os.path.join(RAIZ, "informe", _NOMBRE_PDF) if os.path.isdir(os.path.join(RAIZ, "informe"))
          else os.path.join(RAIZ, _NOMBRE_PDF))

NAVY, BLUE = colors.HexColor("#1f3a5f"), colors.HexColor("#2f6fed")
ROW, ORANGE, PEACH = colors.HexColor("#e8edfb"), colors.HexColor("#e8a33d"), colors.HexColor("#fde8c8")
GREY = colors.HexColor("#667085")

# ---------------------------------- fuentes ------------------------------------ #
def _reg(nombre, rutas):
    for r in rutas:
        if os.path.exists(r):
            pdfmetrics.registerFont(TTFont(nombre, r)); return True
    return False

L = "/usr/share/fonts/truetype/liberation/"
D = "/usr/share/fonts/truetype/dejavu/"
if all([_reg("Serif", [L + "LiberationSerif-Regular.ttf"]), _reg("Serif-B", [L + "LiberationSerif-Bold.ttf"]),
        _reg("Serif-I", [L + "LiberationSerif-Italic.ttf"]), _reg("Sans", [L + "LiberationSans-Regular.ttf"]),
        _reg("Sans-B", [L + "LiberationSans-Bold.ttf"]), _reg("Sans-I", [L + "LiberationSans-Italic.ttf"])]):
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
    registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
    SERIF, SERIF_B, SERIF_I, SANS, SANS_B, SANS_I = "Serif", "Serif-B", "Serif-I", "Sans", "Sans-B", "Sans-I"
else:  # respaldo: fuentes estándar de PDF
    SERIF, SERIF_B, SERIF_I, SANS, SANS_B, SANS_I = "Times-Roman", "Times-Bold", "Times-Italic", "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"
if _reg("Mono", [D + "DejaVuSansMono.ttf"]):
    MONO = "Mono"; _reg("Mono-B", [D + "DejaVuSansMono-Bold.ttf"])
    registerFontFamily = pdfmetrics.registerFontFamily
    registerFontFamily("Mono", normal="Mono", bold="Mono-B", italic="Mono", boldItalic="Mono-B")
else:
    MONO = "Courier"

# ---------------------------------- estilos ------------------------------------ #
P = ParagraphStyle("P", fontName=SERIF, fontSize=10.5, leading=14.6, alignment=TA_JUSTIFY, spaceAfter=6)
SUBH = ParagraphStyle("SUBH", fontName=SANS_B, fontSize=11.5, leading=15, textColor=BLUE, spaceBefore=8, spaceAfter=5)
BUL = ParagraphStyle("BUL", parent=P, leftIndent=18, bulletIndent=6, spaceAfter=3)
CAP = ParagraphStyle("CAP", fontName=SANS, fontSize=8.3, leading=11, alignment=TA_CENTER, textColor=GREY, spaceBefore=3, spaceAfter=10)
TBLCAP = ParagraphStyle("TBLCAP", fontName=SANS, fontSize=8.8, leading=11, spaceBefore=4, spaceAfter=4)
BAN = ParagraphStyle("BAN", fontName=SANS_B, fontSize=14.5, leading=18, textColor=colors.white)
REF = ParagraphStyle("REF", parent=P, leftIndent=22, firstLineIndent=-22, alignment=0, spaceAfter=5)
CELL = ParagraphStyle("CELL", fontName=SERIF, fontSize=10, leading=12.5)
CELLS = ParagraphStyle("CELLS", fontName=SERIF, fontSize=7.4, leading=9.6)

MARGEN = 0.72 * inch
ANCHO = letter[0] - 2 * MARGEN


def code(t):  # texto monoespaciado en línea
    return f"<font name='{MONO}' size='9'>{t}</font>"


def banner(texto):
    t = Table([[Paragraph(texto, BAN)]], colWidths=[ANCHO])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY), ("LEFTPADDING", (0, 0), (-1, -1), 11),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 9)]))
    return KeepTogether([Spacer(1, 4), t, Spacer(1, 8)])


def tabla(filas, anchos, negrita_ultima=True):
    t = Table(filas, colWidths=anchos, repeatRows=1)
    est = [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
           ("FONTNAME", (0, 0), (-1, 0), SANS_B), ("FONTNAME", (0, 1), (-1, -1), SANS), ("FONTSIZE", (0, 0), (-1, -1), 8.8),
           ("LINEBELOW", (0, 0), (-1, 0), 2, ORANGE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW]),
           ("LINEBELOW", (0, 1), (-1, -1), .4, colors.HexColor("#d5dae6")),
           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("LEFTPADDING", (0, 0), (-1, -1), 8)]
    if negrita_ultima:
        est.append(("FONTNAME", (-1, 1), (-1, -1), SANS_B))
    t.setStyle(TableStyle(est))
    return t


def figura(ruta, ancho, num, texto):
    w, h = PILImage.open(ruta).size
    return KeepTogether([Image(ruta, width=ancho, height=ancho * h / w),
                         Paragraph(f"<font color='#2f6fed'><b>Figura {num}.</b></font> {texto} <i>Fuente: elaboración propia.</i>", CAP)])


# ---------------------- ventana de código / terminal --------------------------- #
C_BG, C_BAR, C_NUM, C_TXT = colors.HexColor("#171a26"), colors.HexColor("#2b2f40"), colors.HexColor("#5b6280"), colors.HexColor("#c0caf5")
PAL = {"Keyword": "#bb9af7", "Name.Builtin": "#7dcfff", "Name.Function": "#7aa2f7", "Name.Class": "#7aa2f7",
       "Literal.String": "#9ece6a", "Literal.Number": "#ff9e64", "Comment": "#6b7394", "Operator.Word": "#bb9af7",
       "Name.Decorator": "#e0af68"}


def _color(tipo):
    t = str(tipo).replace("Token.", "")
    while t:
        if t in PAL:
            return colors.HexColor(PAL[t])
        t = t.rpartition(".")[0]
    return C_TXT


def tokenizar_python(fuente):
    """Devuelve una lista de líneas; cada línea es una lista de (texto, color)."""
    try:
        from pygments import lex
        from pygments.lexers import PythonLexer
        lineas, actual = [], []
        for tipo, val in lex(fuente, PythonLexer()):
            partes = val.split("\n")
            for i, p in enumerate(partes):
                if i > 0:
                    lineas.append(actual); actual = []
                if p:
                    actual.append((p, _color(tipo)))
        if actual:
            lineas.append(actual)
        return lineas
    except ImportError:
        return [[(l, C_TXT)] for l in fuente.splitlines()]


class Ventana(Flowable):
    """Ventana oscura estilo editor: barra con 3 puntos, números de línea y texto coloreado."""
    FS, LH, PAD, BAR = 7.2, 9.4, 9, 17

    def __init__(self, lineas, titulo=None, inicio=1, numerar=True):
        super().__init__()
        self.lineas, self.titulo, self.inicio, self.numerar = lineas, titulo, inicio, numerar

    def wrap(self, aw, ah):
        self.w = aw
        self.h = (self.BAR if self.titulo else 0) + 2 * self.PAD + len(self.lineas) * self.LH
        return aw, self.h

    def draw(self):
        c = self.canv
        c.setFillColor(C_BG); c.roundRect(0, 0, self.w, self.h, 5, stroke=0, fill=1)
        y = self.h
        if self.titulo:
            c.setFillColor(C_BAR); c.roundRect(0, self.h - self.BAR, self.w, self.BAR, 5, stroke=0, fill=1)
            c.rect(0, self.h - self.BAR, self.w, 6, stroke=0, fill=1)
            for i, col in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
                c.setFillColor(colors.HexColor(col)); c.circle(10 + i * 11, self.h - self.BAR / 2, 2.6, stroke=0, fill=1)
            c.setFillColor(colors.HexColor("#a0a7c0")); c.setFont(SANS, 7.4)
            c.drawString(46, self.h - self.BAR / 2 - 2.5, self.titulo)
            y -= self.BAR
        y -= self.PAD + self.FS
        xnum = 24 if self.numerar else 0
        for i, linea in enumerate(self.lineas):
            if self.numerar:
                c.setFillColor(C_NUM); c.setFont(MONO, self.FS)
                c.drawRightString(self.PAD + xnum - 8, y, str(self.inicio + i))
            x = self.PAD + xnum
            for texto, col in linea:
                c.setFillColor(col); c.setFont(MONO, self.FS)
                c.drawString(x, y, texto)
                x += pdfmetrics.stringWidth(texto, MONO, self.FS)
            y -= self.LH


def ventanas_codigo(ruta, titulo, primero=20, trozo=38):
    fuente = open(ruta, encoding="utf-8").read()
    lineas = tokenizar_python(fuente)
    out, i, n = [], 0, primero
    while i < len(lineas):
        out += [Ventana(lineas[i:i + n], titulo if i == 0 else None, inicio=i + 1), Spacer(1, 2)]
        i += n; n = trozo
    return out


def ventana_terminal(ruta_salida, comando, titulo):
    lineas = [[("$ ", colors.HexColor("#9ece6a")), (comando, C_TXT)]]
    for l in open(ruta_salida, encoding="utf-8").read().splitlines():
        col = colors.HexColor("#7aa2f7") if l.startswith("===") else (colors.HexColor("#9ece6a") if l.startswith("-->") else C_TXT)
        lineas.append([(l, col)])
    return Ventana(lineas, titulo, numerar=False)


# ---------------------------- plantillas de página ----------------------------- #
def barra_degradada(c):
    n, h = 120, letter[1]
    for i in range(n):
        t = i / (n - 1)
        r, g, b = (0.76 + (0.07 - 0.76) * t, 0.15 + (0.72 - 0.15) * t, 0.85 + (0.65 - 0.85) * t)
        c.setFillColorRGB(r, g, b); c.rect(0, h - (i + 1) * h / n, .37 * inch, h / n + 1, stroke=0, fill=1)


def pagina_portada(c, d):
    c.saveState(); barra_degradada(c); c.restoreState()


def pagina_normal(c, d):
    c.saveState()
    y = letter[1] - .5 * inch
    c.setFont(SANS, 8); c.setFillColor(GREY)
    c.drawString(MARGEN, y, "Práctica 5 · Simultaneidad y asincronía")
    c.drawRightString(letter[0] - MARGEN, y, MATERIA.capitalize())
    c.setStrokeColor(NAVY); c.setLineWidth(.8); c.line(MARGEN, y - 5, letter[0] - MARGEN, y - 5)
    yf = .5 * inch
    c.setStrokeColor(colors.HexColor("#cbd2dc")); c.setLineWidth(.5); c.line(MARGEN, yf + 12, letter[0] - MARGEN, yf + 12)
    c.setFillColor(GREY); c.drawString(MARGEN, yf, f"{NOMBRE_CORTO} · {CODIGO}")
    c.setFillColor(NAVY); c.roundRect(letter[0] - MARGEN - 30, yf - 5, 30, 15, 5, stroke=0, fill=1)
    c.setFillColor(colors.white); c.setFont(SANS_B, 8.5); c.drawCentredString(letter[0] - MARGEN - 15, yf, str(d.page))
    c.restoreState()


class Doc(BaseDocTemplate):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        fr = Frame(MARGEN, .8 * inch, ANCHO, letter[1] - 1.55 * inch, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        fp = Frame(MARGEN, .6 * inch, ANCHO, letter[1] - 1.1 * inch, id="p", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate("portada", frames=[fp], onPage=pagina_portada),
                               PageTemplate("normal", frames=[fr], onPage=pagina_normal)])


# --------------------------------- contenido ----------------------------------- #
def portada():
    S = [Spacer(1, 4),
         Paragraph("UNIVERSIDAD DE GUADALAJARA", ParagraphStyle("u", fontName=SERIF_B, fontSize=29, leading=34, alignment=TA_CENTER)),
         Table([[""]], colWidths=[ANCHO], rowHeights=[4], style=[("BACKGROUND", (0, 0), (-1, -1), colors.black)]),
         Spacer(1, 6),
         Paragraph("CENTRO UNIVERSITARIO DE CIENCIAS EXACTAS E INGENIERÍAS", ParagraphStyle("c1", fontName=SERIF_B, fontSize=10.5, alignment=TA_CENTER, leading=14)),
         Paragraph("Departamento de Innovación Basada en la Información y el Conocimiento", ParagraphStyle("c2", fontName=SERIF, fontSize=12, alignment=TA_CENTER, leading=16)),
         Spacer(1, 18)]
    logo = R("informe", "assets", "logo_udg.png")
    if os.path.exists(logo):
        w, h = PILImage.open(logo).size
        im = Image(logo, width=1.75 * inch, height=1.75 * inch * h / w); im.hAlign = "CENTER"; S.append(im)
    S += [Spacer(1, 8), Paragraph("Ingeniería En Computación", ParagraphStyle("c3", fontName=SERIF, fontSize=13, alignment=TA_CENTER, leading=17)),
          Spacer(1, 8)]
    cab = Table([[Paragraph("PRÁCTICA 5", ParagraphStyle("k", fontName=SANS_B, fontSize=10, alignment=TA_CENTER, textColor=colors.white))],
                 [Paragraph("Descargas: Secuencial vs. Asincronía", ParagraphStyle("t", fontName=SANS_B, fontSize=22, leading=27, alignment=TA_CENTER, textColor=colors.white))],
                 [Paragraph("Comparación de rendimiento entre time.sleep() y asyncio.gather()", ParagraphStyle("s", fontName=SANS, fontSize=9.5, alignment=TA_CENTER, textColor=colors.HexColor("#c9d4ea")))]],
                colWidths=[ANCHO])
    cab.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY), ("TOPPADDING", (0, 0), (-1, 0), 14), ("BOTTOMPADDING", (0, 1), (-1, 1), 6),
                             ("BOTTOMPADDING", (0, 2), (-1, 2), 14), ("LINEBELOW", (0, -1), (-1, -1), 1.5, ORANGE)]))
    lab = lambda a, b: Paragraph(f"<b>{a}</b>: {b}", CELL)
    info = Table([[lab("Nombre", NOMBRE), lab("Código", CODIGO)], [lab("Materia", MATERIA), lab("Grupo", "____________")],
                  [lab("Nombre del profesor", PROFESOR), lab("Actividad", "Práctica 5 (100 puntos)")],
                  [lab("Fecha de entrega", FECHA), lab("Lenguaje", "Python 3.12 · asyncio")]],
                 colWidths=[ANCHO * .62, ANCHO * .38])
    info.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ROW), ("GRID", (0, 0), (-1, -1), 1, colors.black),
                              ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
    bib = Table([[Paragraph("<b>Bibliografía:</b><br/>"
                            "Python Software Foundation. (s. f.). <i>asyncio — Asynchronous I/O</i>. Python 3 Documentation.<br/>"
                            "Python Software Foundation. (s. f.). <i>Coroutines and tasks</i>. Python 3 Documentation.<br/>"
                            "Selivanov, Y. (2015). <i>PEP 492 – Coroutines with async and await syntax</i>.<br/>"
                            "Recursos didácticos de la asignatura (Simultaneidad y asincronía).", CELLS)]], colWidths=[ANCHO])
    bib.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PEACH), ("BOX", (0, 0), (-1, -1), 1, colors.black),
                             ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
    S += [cab, info, bib, NextPageTemplate("normal"), PageBreak()]
    return S


def main():
    one = pd.read_csv(R("resultados", "corrida_unica.csv"))
    rep = pd.read_csv(R("resultados", "repeticiones.csv"))
    res = pd.read_csv(R("resultados", "resumen.csv")).set_index("metrica")
    esc = pd.read_csv(R("resultados", "escalamiento.csv"))
    sec, asy = one[one.enfoque == "Secuencial"].reset_index(drop=True), one[one.enfoque == "Asincrónico"].reset_index(drop=True)
    suma, mayor, t_sec, t_asy = sec.duracion_s.sum(), sec.duracion_s.max(), sec.fin_s.max(), asy.fin_s.max()
    acel, red = t_sec / t_asy, (1 - t_asy / t_sec) * 100
    p_sec, p_asy = res.loc["promedio", "secuencial_s"], res.loc["promedio", "asincrono_s"]
    f2 = lambda x: f"{x:.2f}"

    S = portada()
    # 1 --------------------------------------------------------------------------
    S += [banner("1. Objetivo de la práctica"),
          Paragraph("Aplicar programación asincrónica en Python para simular la descarga de cuatro archivos con duración aleatoria y "
                    f"comparar el rendimiento entre la ejecución secuencial (bloqueante) y la asincrónica (no bloqueante) usando {code('async')}, "
                    f"{code('await')} y {code('asyncio.gather()')}, registrando el tiempo total de cada enfoque.", P)]
    # 2 --------------------------------------------------------------------------
    S += [banner("2. Fundamento breve"),
          Paragraph(f"En la ejecución <b>secuencial</b> cada descarga espera a que termine la anterior: {code('time.sleep(d)')} detiene todo el "
                    "programa durante <i>d</i> segundos y el procesador queda ocioso. En la ejecución <b>asincrónica</b>, una función definida con "
                    f"{code('async def')} es una corrutina: al llegar a un {code('await')} se suspende y devuelve el control al <i>bucle de eventos</i> "
                    f"de {code('asyncio')}, que aprovecha para avanzar las demás (Selivanov, 2015). {code('asyncio.gather()')} programa todas las "
                    "corrutinas a la vez y regresa cuando la última termina (Python Software Foundation, s. f.-b). Con descargas independientes, "
                    "el modelo ideal predice que el tiempo secuencial es la <b>suma</b> de las duraciones y el asincrónico es la <b>mayor</b> de ellas.", P),
          Paragraph("Metodología de medición", SUBH)]
    for b in (f"Se sortean 4 duraciones entre 1 y 4 s con {code('random.Random(semilla)')} y se usan <b>las mismas</b> en ambos enfoques.",
              f"Se mide solo la ejecución de cada bloque con {code('time.perf_counter()')}.",
              f"Corrida de referencia con semilla 2025 y, después, {len(rep)} corridas con duraciones distintas y un experimento con 1 a 32 archivos.",
              "Entorno de prueba: Python 3.12.3; los tiempos absolutos dependen del equipo, pero la relación suma/máximo se conserva."):
        S.append(Paragraph(b, BUL, bulletText="•"))
    # 3 --------------------------------------------------------------------------
    S += [banner("3. Código de la práctica"), Paragraph("3.1 Programa completo (descargas.py)", SUBH)]
    S += ventanas_codigo(R("descargas.py"), "descargas.py · Python 3")
    S.append(Paragraph(f"El script <i>experimento.py</i> (en el repositorio) repite las mediciones y genera las tablas y gráficas de la sección 4.", ParagraphStyle("n", parent=P, spaceBefore=6)))
    # 4 --------------------------------------------------------------------------
    S += [banner("4. Resultados"), Paragraph("4.1 Capturas de la ejecución", SUBH),
          Paragraph("Salida real del programa con la semilla 2025 (se muestran la tabla comparativa y el inicio/fin de cada descarga):", P),
          ventana_terminal(R("resultados", "salida_descargas.txt"), "python descargas.py --semilla 2025", "terminal — descargas.py"),
          Paragraph("<font color='#2f6fed'><b>Figura 1.</b></font> Ejecución del bloque secuencial y del asincrónico. <i>Fuente: elaboración propia.</i>", CAP),
          Paragraph("4.2 Comparación", SUBH),
          Paragraph("<b>Tabla 1.</b> Tiempo total de la corrida de referencia y aceleración de la versión asincrónica.", TBLCAP),
          tabla([["Enfoque", "Suma de duraciones (s)", "Tiempo total (s)", "Aceleración"],
                 ["Secuencial (bloqueante)", f2(suma), f2(t_sec), "1.00×"],
                 ["Asincrónico (gather)", f2(mayor) + " (mayor)", f2(t_asy), f"{acel:.2f}×"]],
                [ANCHO * .34, ANCHO * .26, ANCHO * .22, ANCHO * .18]),
          Spacer(1, 10),
          figura(R("figs", "linea_de_tiempo.png"), ANCHO * .98, 2,
                 "Línea de tiempo de la corrida de referencia (la línea punteada marca el tiempo total)."),
          ]
    cap2 = Paragraph("<b>Tabla 2.</b> Repeticiones con duraciones aleatorias distintas (s).", TBLCAP)
    f = [["Corrida", "Duraciones", "Suma", "Mayor", "Secuencial", "Asincrónico", "Aceleración"]]
    for _, r in rep.iterrows():
        f.append([int(r.corrida), r.duraciones, f2(r.suma_duraciones), f2(r.mayor_duracion), f2(r.t_secuencial), f2(r.t_asincrono), f"{r.aceleracion:.2f}×"])
    f.append(["Promedio", "", f2(rep.suma_duraciones.mean()), f2(rep.mayor_duracion.mean()), f2(p_sec), f2(p_asy), f"{(rep.t_secuencial / rep.t_asincrono).mean():.2f}×"])
    t2 = tabla(f, [ANCHO * w for w in (.11, .27, .09, .09, .14, .15, .15)])
    t2.setStyle(TableStyle([("FONTNAME", (0, -1), (-1, -1), SANS_B), ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#cfdcf7"))]))
    S += [KeepTogether([cap2, t2]), Spacer(1, 8),
          figura(R("figs", "repeticiones.png"), ANCHO * .5, 3, "Tiempo total en cada corrida; el asincrónico sigue a la mayor duración individual."),
          ]
    cap3 = Paragraph("<b>Tabla 3.</b> Tiempo total según el número de descargas (0.1–0.5 s cada una).", TBLCAP)
    f = [["Archivos", "Secuencial (s)", "Asincrónico (s)", "Aceleración"]]
    for _, r in esc.iterrows():
        f.append([int(r.n_archivos), f"{r.t_secuencial:.3f}", f"{r.t_asincrono:.3f}", f"{r.aceleracion:.2f}×"])
    S += [KeepTogether([cap3, tabla(f, [ANCHO * .22, ANCHO * .28, ANCHO * .28, ANCHO * .22])]), Spacer(1, 8),
          figura(R("figs", "escalamiento.png"), ANCHO * .4, 4, "Escalamiento: el tiempo secuencial crece con el número de archivos; el asincrónico casi no cambia."),
          Paragraph(f"<i>Nota:</i> la práctica <i>simula</i> las descargas con esperas; en una descarga real el ancho de banda compartido puede limitar la "
                    f"ganancia, y entonces conviene acotar la concurrencia con {code('asyncio.Semaphore')}. Los tiempos varían unos milisegundos entre "
                    "ejecuciones, pero la relación suma/máximo se mantiene siempre.", P)]
    # 5 --------------------------------------------------------------------------
    S += [banner("5. Reflexión final"),
          Paragraph("<b>¿Qué ventaja representa la asincronía frente a la ejecución secuencial?</b> Aprovecha el tiempo de espera: mientras una descarga "
                    "aguarda, el bucle de eventos avanza las demás, por lo que el tiempo total deja de ser la suma de todas las esperas y pasa a ser "
                    f"aproximadamente la más larga. En la corrida de referencia se pasó de {f2(t_sec)} s a {f2(t_asy)} s ({acel:.2f} veces más rápido, "
                    f"{red:.0f} % menos tiempo) sin crear hilos ni procesos adicionales y con un código que se sigue leyendo de forma lineal. La ventaja "
                    f"crece con el número de tareas (casi {esc.aceleracion.iloc[-1]:.0f} veces con 32 archivos); su límite es que solo ayuda cuando el programa "
                    "espera entrada/salida, no cuando hace cálculo intensivo de CPU.", P),
          Paragraph("<b>¿En qué tipo de programas reales sería útil esta técnica?</b> En programas dominados por esperas de red o de disco: servidores web y "
                    "APIs que atienden muchos clientes a la vez (FastAPI, aiohttp), rastreadores web que consultan cientos de páginas, descargadores de "
                    "archivos, bots de chat, aplicaciones que consultan varias APIs o bases de datos para armar una sola respuesta, y sistemas de tiempo real "
                    "como chats, notificaciones o lectura de sensores.", P)]
    # 6 --------------------------------------------------------------------------
    S += [banner("6. Conclusión"),
          Paragraph(f"La versión <b>asincrónica fue la más rápida</b>: {f2(t_asy)} s frente a {f2(t_sec)} s en la corrida de referencia y {f2(p_asy)} s frente a "
                    f"{f2(p_sec)} s en promedio en {len(rep)} corridas. Los resultados confirman el modelo teórico (suma contra máximo): el tiempo secuencial "
                    f"coincidió con la suma de las duraciones ({f2(suma)} s) y el asincrónico con la mayor ({f2(mayor)} s), con apenas unos milisegundos de "
                    "sobrecarga. Además, la mejora aumenta con el número de tareas independientes y desaparece con una sola tarea o con trabajo de CPU. "
                    f"{code('async')}, {code('await')} y {code('asyncio.gather()')} permiten obtener esa ganancia con un código corto y legible.", P),
          banner("Referencias")]
    refs = ["Python Software Foundation. (s. f.-a). <i>asyncio — Asynchronous I/O</i>. Python 3 Documentation. https://docs.python.org/3/library/asyncio.html",
            "Python Software Foundation. (s. f.-b). <i>Coroutines and tasks</i>. Python 3 Documentation. https://docs.python.org/3/library/asyncio-task.html",
            "Selivanov, Y. (2015). <i>PEP 492 – Coroutines with async and await syntax</i>. Python Enhancement Proposals. https://peps.python.org/pep-0492/"]
    S += [Paragraph(r, REF) for r in refs]

    Doc(SALIDA, pagesize=letter, title="Práctica 5 · Simultaneidad y Asincronía", author=NOMBRE_CORTO, subject=MATERIA).build(S)
    print("Informe generado:", SALIDA)


if __name__ == "__main__":
    main()
