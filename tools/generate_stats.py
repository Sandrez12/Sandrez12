"""Genera assets/stats.svg y assets/langs.svg con datos reales de GitHub.

Requiere la variable de entorno GITHUB_TOKEN (la del workflow sirve) y usa la
API GraphQL/REST. Uso: GITHUB_TOKEN=... python tools/generate_stats.py [usuario]
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

USER = sys.argv[1] if len(sys.argv) > 1 else "Sandrez12"
OUT = Path(__file__).resolve().parent.parent / "assets"
TOKEN = os.environ["GITHUB_TOKEN"]

BG, PANEL = "#0d1f20", "#12292a"
RED, RED_L, RED_D = "#d64545", "#e05a5a", "#8f2b2b"
CREAM, MUTED = "#f4ece6", "#9db7b4"
FONT = "'Trebuchet MS','Segoe UI',Verdana,sans-serif"


def api(url, data=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode() if data else None,
        headers={"Authorization": f"Bearer {TOKEN}", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def stats_svg(u):
    c = u["contributionsCollection"]
    repos = u["repositories"]["nodes"]
    items = [
        ("Contribuciones (último año)", c["contributionCalendar"]["totalContributions"]),
        ("Commits", c["totalCommitContributions"]),
        ("Pull requests", c["totalPullRequestContributions"]),
        ("Repositorios propios", u["repositories"]["totalCount"]),
        ("Lenguajes distintos", len({e["node"]["name"] for r in repos for e in r["languages"]["edges"]})),
    ]
    rows = ""
    for i, (k, v) in enumerate(items):
        y = 112 + i * 44
        rows += (
            f'<rect x="28" y="{y-18}" width="9" height="9" rx="2" fill="{RED}"/>'
            f'<text x="50" y="{y-9}" font-family="{FONT}" font-size="16" fill="{CREAM}">{k}</text>'
            f'<text x="412" y="{y-9}" text-anchor="end" font-family="{FONT}" font-size="22" font-weight="800" fill="{RED_L}">{v}</text>'
            f'<line x1="28" y1="{y+5}" x2="412" y2="{y+5}" stroke="{RED_D}" stroke-opacity=".5"/>'
        )
    since = u["createdAt"][:4]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 330" width="440" height="330" role="img" aria-label="Estadísticas de GitHub">
<rect width="440" height="330" rx="18" fill="{PANEL}"/>
<rect width="8" height="330" rx="4" fill="{RED}"/>
<text x="28" y="46" font-family="{FONT}" font-size="24" font-weight="800" fill="{CREAM}">{USER} en números</text>
<text x="28" y="68" font-family="{FONT}" font-size="12.5" fill="{MUTED}">En GitHub desde {since} · actualizado {datetime.now(timezone.utc):%d/%m/%Y}</text>
{rows}
</svg>'''
    (OUT / "stats.svg").write_text(svg, encoding="utf-8")


def langs_svg(u):
    tot = {}
    for r in u["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            tot[e["node"]["name"]] = tot.get(e["node"]["name"], 0) + e["size"]
    ignore = {"Blade", "Jupyter Notebook", "ShaderLab", "HLSL", "Shell", "Dockerfile"}
    items = sorted(((k, v) for k, v in tot.items() if k not in ignore), key=lambda kv: -kv[1])[:6]
    total = sum(v for _, v in items) or 1
    shades = [RED_L, "#c94a4a", "#b03d3d", "#8f2b2b", "#6e2323", "#4d1c1c"]
    rows = ""
    bar_x, bar_w = 150, 250
    for i, (name, v) in enumerate(items):
        y = 96 + i * 38
        pct = v * 100 / total
        w = max(6, bar_w * pct / 100)
        rows += (
            f'<text x="28" y="{y}" font-family="{FONT}" font-size="15" fill="{CREAM}">{name}</text>'
            f'<rect x="{bar_x}" y="{y-12}" width="{bar_w}" height="12" rx="6" fill="{BG}"/>'
            f'<rect x="{bar_x}" y="{y-12}" width="{w:.0f}" height="12" rx="6" fill="{shades[i]}">'
            f'<animate attributeName="width" from="0" to="{w:.0f}" dur="1.2s" fill="freeze"/></rect>'
            f'<text x="412" y="{y}" text-anchor="end" font-family="{FONT}" font-size="13" fill="{MUTED}">{pct:.1f}%</text>'
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 330" width="440" height="330" role="img" aria-label="Lenguajes principales">
<rect width="440" height="330" rx="18" fill="{PANEL}"/>
<rect width="8" height="330" rx="4" fill="{RED}"/>
<text x="28" y="46" font-family="{FONT}" font-size="24" font-weight="800" fill="{CREAM}">Lenguajes principales</text>
<text x="28" y="68" font-family="{FONT}" font-size="12.5" fill="{MUTED}">Por volumen de código en mis repositorios</text>
{rows}
</svg>'''
    (OUT / "langs.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    data = api(
        "https://api.github.com/graphql",
        {
            "query": """query($login:String!){ user(login:$login){
              createdAt
              contributionsCollection { totalCommitContributions totalPullRequestContributions
                contributionCalendar { totalContributions } }
              repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
                totalCount nodes { name stargazerCount
                  languages(first: 10, orderBy:{field:SIZE,direction:DESC}) { edges { size node { name } } } } }
            } }""",
            "variables": {"login": USER},
        },
    )["data"]["user"]
    stats_svg(data)
    langs_svg(data)
    print("stats.svg y langs.svg generados")
