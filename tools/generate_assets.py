"""Genera los SVG estáticos del README (hero, títulos, tarjetas, íconos).

Uso: python tools/generate_assets.py
Todo el arte vive en SVG autocontenidos con fondo propio, así que se ve igual
en tema claro y oscuro de GitHub.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
ICONS = OUT / "icons"
OUT.mkdir(exist_ok=True)

BG = "#0d1f20"
PANEL = "#12292a"
PANEL2 = "#173536"
RED = "#d64545"
RED_L = "#e05a5a"
RED_D = "#8f2b2b"
CREAM = "#f4ece6"
MUTED = "#9db7b4"
FONT = "'Trebuchet MS','Segoe UI',Verdana,sans-serif"


def write(name, svg):
    (OUT / name).write_text(svg, encoding="utf-8")


def swirl(x, y, s=1.0):
    """Pequeño remolino rojo (guiño al icono de la referencia)."""
    return (
        f'<g transform="translate({x},{y}) scale({s})">'
        f'<path d="M0 22 C0 6 14 -2 28 4 C20 6 16 12 20 18 C24 24 34 22 36 14 '
        f'C40 28 24 40 10 36 C4 34 0 28 0 22 Z" fill="{RED}"/>'
        f'<circle cx="23" cy="14" r="3.2" fill="{BG}"/></g>'
    )


def tentacle(d, w, delay=0, dur=7, amp=3):
    return (
        f'<path d="{d}" fill="none" stroke="{RED}" stroke-width="{w}" stroke-linecap="round">'
        f'<animateTransform attributeName="transform" type="rotate" values="0 0 0;{amp} 0 0;0 0 0;-{amp} 0 0;0 0 0" '
        f'dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></path>'
    )


def hero():
    bubbles = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{CREAM}" opacity="0.85">'
        f'<animate attributeName="cy" values="{y};{y-30};{y}" dur="{d}s" repeatCount="indefinite"/></circle>'
        for x, y, r, d in [(700, 90, 9, 4), (730, 55, 6, 5), (760, 30, 4, 6), (640, 60, 5, 7)]
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 440" width="1000" height="440" role="img" aria-label="Portfolio de Andrés Felipe Joya Buitrago">
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0a1819"/><stop offset="1" stop-color="#11302f"/>
  </linearGradient>
  <linearGradient id="r" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{RED_D}"/><stop offset="1" stop-color="{RED_L}"/>
  </linearGradient>
</defs>
<rect width="1000" height="440" rx="18" fill="url(#g)"/>
<!-- tablones de fondo -->
<path d="M430 440 L520 250 L760 250 L720 440 Z" fill="#164d4d" opacity=".55"/>
<path d="M470 440 L545 280 L735 280 L705 440 Z" fill="#1a6060" opacity=".45"/>
<!-- tentáculos -->
<g transform="translate(-30,440)">{tentacle("M0 20 C60 -25 110 10 160 -12 C190 -26 215 -10 240 -22", 26, 0, 8)}</g>
<g transform="translate(1040,150)">{tentacle("M0 0 C-80 40 -90 120 -40 170 C-10 205 -70 250 -120 230", 34, 1, 9)}</g>
<g transform="translate(980,380)">{tentacle("M0 0 C-60 -30 -110 10 -150 -20", 22, 2, 6, 4)}</g>
<g transform="translate(14,10)" opacity=".9">{tentacle("M0 0 C30 18 24 44 -6 56", 18, 0.5, 7)}</g>
<!-- criatura / silueta decorativa -->
<g transform="translate(700,150)">
  <path d="M0 140 C-20 60 40 0 120 20 C190 38 230 110 190 200 C150 280 40 280 0 140 Z" fill="url(#r)"/>
  <path d="M60 30 C70 -10 120 -20 140 10 C120 8 90 14 80 40 Z" fill="{RED_D}"/>
  <circle cx="132" cy="68" r="7" fill="{CREAM}"/><circle cx="132" cy="68" r="3" fill="{BG}"/>
  <path d="M30 230 C10 270 60 290 90 262" fill="none" stroke="{RED_D}" stroke-width="14" stroke-linecap="round"/>
</g>
{bubbles}
<!-- jarra -->
<g transform="translate(560,170)">
  <rect x="0" y="0" width="64" height="74" rx="8" fill="{RED_D}"/>
  <rect x="0" y="14" width="64" height="8" fill="{CREAM}"/><rect x="0" y="52" width="64" height="8" fill="{CREAM}"/>
  <path d="M64 18 C92 18 92 56 64 56" fill="none" stroke="{CREAM}" stroke-width="8"/>
  <animateTransform attributeName="transform" type="translate" values="560,170;560,162;560,170" dur="4s" repeatCount="indefinite"/>
</g>
<!-- título -->
<text x="56" y="190" font-family="{FONT}" font-size="104" font-weight="800" font-style="italic" fill="{CREAM}" letter-spacing="-2">Portfolio</text>
<rect x="60" y="212" width="0" height="6" rx="3" fill="{RED}"><animate attributeName="width" values="0;330;330" keyTimes="0;.5;1" dur="2.2s" fill="freeze"/></rect>
<text x="58" y="268" font-family="{FONT}" font-size="34" font-weight="700" fill="{RED_L}">Andrés Felipe Joya Buitrago</text>
<text x="58" y="308" font-family="{FONT}" font-size="20" fill="{MUTED}">Ingeniero en Sistemas · Desarrollador Fullstack · Bucaramanga, Colombia</text>
<g font-family="{FONT}" font-size="15" font-weight="700">
  <rect x="58" y="340" width="112" height="34" rx="17" fill="{RED}"/><text x="114" y="362" text-anchor="middle" fill="{BG}">Laravel</text>
  <rect x="182" y="340" width="112" height="34" rx="17" fill="none" stroke="{RED}" stroke-width="2"/><text x="238" y="362" text-anchor="middle" fill="{CREAM}">React</text>
  <rect x="306" y="340" width="112" height="34" rx="17" fill="none" stroke="{RED}" stroke-width="2"/><text x="362" y="362" text-anchor="middle" fill="{CREAM}">Python</text>
  <rect x="430" y="340" width="112" height="34" rx="17" fill="none" stroke="{RED}" stroke-width="2"/><text x="486" y="362" text-anchor="middle" fill="{CREAM}">Docker</text>
</g>
<text x="58" y="414" font-family="{FONT}" font-size="18" font-style="italic" fill="{CREAM}">“Iré hasta los límites de lo que mi mente permita, y mi alma desee”</text>
</svg>'''
    write("hero.svg", svg)


def heading(slug, text, width=900):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 84" width="{width}" height="84" role="img" aria-label="{text}">
<rect width="{width}" height="84" rx="14" fill="{PANEL}"/>
<rect x="0" y="0" width="8" height="84" rx="4" fill="{RED}"/>
{swirl(30, 20, 1.1)}
<text x="86" y="56" font-family="{FONT}" font-size="40" font-weight="800" fill="{CREAM}">{text}</text>
<rect x="{width-210}" y="40" width="190" height="4" rx="2" fill="{RED_D}"/>
<rect x="{width-210}" y="40" width="60" height="4" rx="2" fill="{RED_L}">
  <animate attributeName="x" values="{width-210};{width-80};{width-210}" dur="3.5s" repeatCount="indefinite"/></rect>
</svg>'''
    write(f"h-{slug}.svg", svg)


def icon_path(slug):
    m = re.search(r' d="([^"]+)"', (ICONS / f"{slug}.svg").read_text(encoding="utf-8"))
    return m.group(1)


def pill(slug, text, glyph):
    """Fila de contacto: círculo rojo con ícono + texto."""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 54" width="400" height="54" role="img" aria-label="{text}">
<rect width="400" height="54" rx="12" fill="{PANEL}"/>
<rect x="0" y="0" width="5" height="54" rx="2.5" fill="{RED}"/>
<circle cx="34" cy="27" r="15" fill="{RED}"/>
{glyph}
<text x="62" y="33" font-family="{FONT}" font-size="16" fill="{CREAM}">{text}</text>
</svg>'''
    write(f"c-{slug}.svg", svg)


def glyph_icon(slug, color=BG):
    return f'<g transform="translate(24,17) scale(0.83)"><path d="{icon_path(slug)}" fill="{color}"/></g>'


def contacts():
    pill("mail", "joya.andres23@gmail.com", glyph_icon("gmail"))
    pill("github", "github.com/Sandrez12", glyph_icon("github"))
    pill(
        "linkedin",
        "linkedin.com/in/andres-joya-69a552357",
        f'<text x="34" y="33" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="800" fill="{BG}">in</text>',
    )
    pill("web", "Portafolio web (Render)", f'<circle cx="34" cy="27" r="8" fill="none" stroke="{BG}" stroke-width="2"/><path d="M26 27 H42 M34 19 C30 24 30 30 34 35 M34 19 C38 24 38 30 34 35" fill="none" stroke="{BG}" stroke-width="1.6"/>')


def timeline():
    rows = [
        ("2019 - actualidad", "Ingeniería en Sistemas", "Universidad Autónoma de Bucaramanga (UNAB)"),
        ("2025", "Cognia · proyecto en equipo", "App web para niños con autismo: login, dashboard y juegos"),
        ("2025", "LSC · IA + móvil + cloud", "Traductor de lengua de señas: LSTM, MediaPipe, AWS y Expo"),
        ("2026", "GestorEscolarBUAP", "Sistema académico en Laravel desplegado con Docker"),
        ("2026", "StockWise", "Backend de gestión de inventarios con FastAPI y PostgreSQL"),
    ]
    h = 28 + 62 * len(rows)
    body = ""
    for i, (when, title, sub) in enumerate(rows):
        y = 34 + i * 62
        body += (
            f'<rect x="24" y="{y-8}" width="10" height="10" rx="2" fill="{RED}"/>'
            f'<text x="50" y="{y+2}" font-family="{FONT}" font-size="14" fill="{RED_L}" font-weight="700">{when}</text>'
            f'<text x="176" y="{y+2}" font-family="{FONT}" font-size="17" fill="{CREAM}" font-weight="700">{title}</text>'
            f'<text x="176" y="{y+24}" font-family="{FONT}" font-size="13" fill="{MUTED}">{sub}</text>'
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 {h}" width="560" height="{h}" role="img" aria-label="Educación y trayectoria">
<rect width="560" height="{h}" rx="18" fill="{PANEL}"/>
<line x1="29" y1="34" x2="29" y2="{h-38}" stroke="{RED_D}" stroke-width="2"/>
{body}
</svg>'''
    write("timeline.svg", svg)


def strengths():
    items = [
        ("Pensamiento lógico", "resolución de problemas", 0.9),
        ("Trabajo en equipo", "colaboración en proyectos reales", 0.85),
        ("Comunicación efectiva", "claridad al explicar y documentar", 0.8),
        ("Adaptabilidad", "aprendizaje continuo de nuevas tecnologías", 0.9),
    ]
    h = 24 + 66 * len(items)
    body = ""
    for i, (t, s, v) in enumerate(items):
        y = 38 + i * 66
        bars = "".join(
            f'<rect x="{24 + k*37}" y="{y+10}" width="30" height="8" rx="2" fill="{RED if k < round(v*8) else CREAM}" opacity="{1 if k < round(v*8) else .85}"/>'
            for k in range(8)
        )
        body += (
            f'<text x="24" y="{y}" font-family="{FONT}" font-size="16" fill="{CREAM}" font-weight="700">{t}</text>{bars}'
            f'<text x="24" y="{y+38}" font-family="{FONT}" font-size="12.5" fill="{MUTED}">{s}</text>'
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 330 {h}" width="330" height="{h}" role="img" aria-label="Fortalezas">
<rect width="330" height="{h}" rx="14" fill="{PANEL}"/>
{body}
</svg>'''
    write("strengths.svg", svg)


def about_card():
    lines = [
        "Soy estudiante de Ingeniería en Sistemas y desarrollador",
        "de software. Me apasionan las tecnologías y su impacto en",
        "la vida diaria: construyo herramientas útiles, resuelvo",
        "problemas con análisis y colaboro en proyectos de impacto.",
        "Mi meta: crecer como desarrollador fullstack.",
    ]
    t = ""
    for i, l in enumerate(lines):
        weight = 'font-weight="700"' if i == 4 else ""
        fill = CREAM if i < 4 else RED_L
        t += f'<text x="26" y="{80 + i*28}" font-family="{FONT}" font-size="16.5" fill="{fill}" {weight}>{l}</text>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 236" width="520" height="236" role="img" aria-label="Quién soy">
<rect width="520" height="236" rx="16" fill="{PANEL}"/>
<text x="26" y="42" font-family="{FONT}" font-size="14" fill="{MUTED}" letter-spacing="2">SOY UN INGENIERO EN FORMACIÓN</text>
{t}
<rect x="26" y="206" width="90" height="5" rx="2.5" fill="{RED}"/>
</svg>'''
    write("about.svg", svg)


def languages():
    rows = [
        ("es", "Español", 6, "Lengua nativa", "Nativo"),
        ("en", "Inglés", 5, "Comprendo y me expreso con fluidez", "C1"),
        ("pt", "Portugués", 1, "Aprendiendo desde hace 2 meses", "Iniciando"),
    ]
    h = 28 + 82 * len(rows)
    body = ""
    for i, (code, name, lvl, desc, tag) in enumerate(rows):
        y = 40 + i * 82
        bars = "".join(
            f'<rect x="{24 + k*44}" y="{y+10}" width="38" height="9" rx="2" fill="{RED if k < lvl else CREAM}" opacity="{1 if k < lvl else .85}"/>'
            for k in range(6)
        )
        body += (
            f'<text x="24" y="{y}" font-family="{FONT}" font-size="17" font-weight="800" fill="{CREAM}">{name}</text>'
            f'<text x="376" y="{y}" text-anchor="end" font-family="{FONT}" font-size="14" font-weight="800" fill="{RED_L}">{tag}</text>'
            f'{bars}'
            f'<text x="24" y="{y+40}" font-family="{FONT}" font-size="12.5" fill="{MUTED}">{desc}</text>'
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 {h}" width="400" height="{h}" role="img" aria-label="Idiomas">
<rect width="400" height="{h}" rx="14" fill="{PANEL}"/>
<rect x="0" y="0" width="5" height="{h}" rx="2.5" fill="{RED}"/>
{body}
</svg>'''
    write("languages.svg", svg)


SKILLS = [
    ("html5", "HTML5"), ("css", "CSS3"), ("javascript", "JavaScript"), ("typescript", "TypeScript"),
    ("react", "React"), ("tailwindcss", "Tailwind"), ("php", "PHP"), ("laravel", "Laravel"),
    ("python", "Python"), ("fastapi", "FastAPI"), ("pytorch", "PyTorch"), ("openjdk", "Java"),
    ("kotlin", "Kotlin"), ("android", "Android"), ("sharp", "C#"), ("unity", "Unity"),
    ("mysql", "MySQL"), ("postgresql", "PostgreSQL"), ("supabase", "Supabase"), ("docker", "Docker"),
    ("git", "Git"), ("github", "GitHub"), ("nodedotjs", "Node.js"), ("androidstudio", "Android Studio"),
]


def skills_band(cols=8):
    cw, rh = 112, 96
    rows = (len(SKILLS) + cols - 1) // cols
    W, H = cw * cols, rh * rows + 24
    body = ""
    for i, (slug, name) in enumerate(SKILLS):
        c, r = i % cols, i // cols
        cx, cy = c * cw + cw // 2, 24 + r * rh
        body += (
            f'<g transform="translate({cx-25},{cy+4}) scale(2.1)"><path d="{icon_path(slug)}" fill="{RED_L}">'
            f'<animate attributeName="opacity" values="1;.65;1" dur="{3 + (i % 4)}s" repeatCount="indefinite"/></path></g>'
            f'<text x="{cx}" y="{cy+82}" text-anchor="middle" font-family="{FONT}" font-size="13.5" fill="{CREAM}">{name}</text>'
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Habilidades">
<rect width="{W}" height="{H}" rx="16" fill="{PANEL}"/>
{body}
</svg>'''
    write("skills.svg", svg)


def footer():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 110" width="900" height="110" role="img" aria-label="Gracias por visitar">
<rect width="900" height="110" rx="16" fill="{BG}"/>
<path d="M0 90 C150 40 300 120 450 80 C600 40 750 120 900 70 L900 110 L0 110 Z" fill="{RED_D}" opacity=".6">
<animate attributeName="d" dur="8s" repeatCount="indefinite"
 values="M0 90 C150 40 300 120 450 80 C600 40 750 120 900 70 L900 110 L0 110 Z;M0 70 C150 110 300 50 450 90 C600 120 750 50 900 90 L900 110 L0 110 Z;M0 90 C150 40 300 120 450 80 C600 40 750 120 900 70 L900 110 L0 110 Z"/></path>
<path d="M0 100 C200 70 350 110 520 90 C700 70 800 100 900 90 L900 110 L0 110 Z" fill="{RED}" opacity=".8"/>
<text x="450" y="46" text-anchor="middle" font-family="{FONT}" font-size="24" font-weight="800" fill="{CREAM}">Gracias por pasar por mi perfil</text>
<text x="450" y="70" text-anchor="middle" font-family="{FONT}" font-size="14" fill="{MUTED}">Hecho con cariño, café y bastante código</text>
</svg>'''
    write("footer.svg", svg)


if __name__ == "__main__":
    hero()
    for slug, text in [
        ("quien", "¿quién soy?"),
        ("contacto", "contacto"),
        ("trayectoria", "educación / trayectoria"),
        ("skills", "habilidades"),
        ("proyectos", "proyectos destacados"),
        ("stats", "estadísticas"),
        ("snake", "contribuciones"),
    ]:
        heading(slug, text)
    contacts()
    timeline()
    strengths()
    languages()
    about_card()
    skills_band()
    footer()
    print("ok")
