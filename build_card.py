#!/usr/bin/env python3
"""
Builds assets/profile-card.svg  (the dashboard card for your GitHub README).

Usage:
    pip install pillow
    python build_card.py                    # uses the built-in devil portrait
    python build_card.py --photo me.jpg     # turns YOUR photo into the ASCII portrait

Edit the CONFIG block below, run again, commit assets/profile-card.svg.
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFilter, ImageOps

# ─────────────────────────── EDIT THIS ───────────────────────────
CONFIG = dict(
    username="DarkDevil-5439",
    name="DARK DEVIL",
    role="Developer & Tech Enthusiast",
    quote=["Debugging is like being the detective in a crime movie",
           "where you are also the murderer."],
    chips=["Python", "JavaScript", "C++", "Linux", "Git"],
    # (label, number)  -> replace with your real numbers
    stats=[("Stars", "128"), ("Commits", "1,240"), ("Repos", "24"), ("Followers", "86")],
    # (language, percent)
    skills=[("Python", 85), ("JavaScript", 72), ("C++", 60), ("HTML/CSS", 78)],
    # (repo name, description, language, language colour, stars)
    repos=[
        ("project-one",   "Short description of your best project", "Python",     "#3572A5", "42"),
        ("project-two",   "Short description of your second one",  "JavaScript", "#f1e05a", "27"),
        ("project-three", "Short description of your third one",   "C++",        "#f34b7d", "15"),
    ],
)
# ─────────────────────────────────────────────────────────────────

FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
RED, RED2 = "#ff2e3d", "#ff6a3d"
COLS, ROWS, CW, CH = 74, 44, 3.5, 6.2          # ascii grid + cell size (svg units)
PX, PY, PW, PH = 40, 84, 290, 300              # portrait panel
RAMP = " .:-=+*#%@"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ───────────────────────── portrait ─────────────────────────
W, H = 518, 546
EYES = [(221, 299), (297, 299)]


def devil_portrait():
    img = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(img)
    for r in range(270, 0, -3):                                   # aura
        d.ellipse((259 - r, 300 - r, 259 + r, 300 + r), fill=int(75 * (1 - r / 270) ** 1.6))
    horn = [(150, 215), (112, 150), (98, 85), (116, 28), (152, 92), (186, 150), (204, 192)]
    d.polygon(horn, fill=215)
    d.polygon([(W - x, y) for x, y in horn], fill=215)
    d.polygon([(20, H), (80, 440), (259, 405), (438, 440), (498, H)], fill=95)   # shoulders
    d.ellipse((134, 150, 384, 450), fill=105, outline=235, width=7)                # hood
    d.ellipse((181, 205, 337, 415), fill=6)                                        # face void
    for sx in (1, -1):                                                             # hoodie strings
        x0 = 259 + sx * 28
        d.line((x0, 410, x0 + sx * 6, 500), fill=190, width=4)
        d.ellipse((x0 + sx * 6 - 6, 496, x0 + sx * 6 + 6, 512), fill=220)
    eye = [(196, 282), (246, 304), (240, 318), (198, 302)]
    d.polygon(eye, fill=255)
    d.polygon([(W - x, y) for x, y in eye], fill=255)
    d.arc((205, 325, 313, 405), 15, 165, fill=235, width=5)                        # grin
    for tx in range(222, 300, 15):
        d.line((tx, 372, tx + 2, 384), fill=220, width=3)
    return img.filter(ImageFilter.GaussianBlur(2.2))


def photo_portrait(path):
    img = Image.open(path).convert("L")
    img = ImageOps.fit(img, (W, H), centering=(0.5, 0.38))
    img = ImageOps.autocontrast(img, cutoff=2)
    return ImageOps.equalize(img)


def ascii_lines(img):
    small = img.resize((COLS, ROWS), Image.BOX)
    px = small.load()
    out = []
    for y in range(ROWS):
        row = ""
        for x in range(COLS):
            v = (px[x, y] / 255) ** 0.85
            row += RAMP[min(len(RAMP) - 1, int(v * len(RAMP)))]
        out.append(row)
    return out


def portrait_svg(img, show_eyes):
    ox = PX + (PW - COLS * CW) / 2
    oy = PY + (PH - ROWS * CH) / 2 + CH
    parts = []
    for i, row in enumerate(ascii_lines(img)):
        cells = [(k, ch) for k, ch in enumerate(row) if ch != " "]
        if not cells:
            continue
        xs = " ".join(f"{ox + k * CW:.1f}" for k, _ in cells)      # exact x for every glyph
        txt = esc("".join(ch for _, ch in cells))
        parts.append(f'<text x="{xs}" y="{oy + i * CH:.1f}">{txt}</text>')
    glow = ""
    if show_eyes:
        for ex, ey in EYES:
            cx = ox + ex / W * COLS * CW
            cy = oy - CH + ey / H * ROWS * CH
            glow += (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="#fff" filter="url(#glow)">'
                     f'<animate attributeName="opacity" values="1;.35;1" dur="2.6s" repeatCount="indefinite"/></circle>')
    return (f'<g font-family="{FONT}" font-size="5.8" fill="url(#ascii)">' + "".join(parts) + "</g>" + glow)


# ───────────────────────── svg parts ─────────────────────────
GH_PATH = ("M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49"
           "-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82"
           ".72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15"
           "-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82"
           ".44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2"
           " 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z")


def titlebar(c):
    return f'''
<circle cx="46" cy="42" r="5.5" fill="#ff5f57"/><circle cx="66" cy="42" r="5.5" fill="#febc2e"/><circle cx="86" cy="42" r="5.5" fill="#28c840"/>
<g transform="translate(110,34)" fill="#e6edf3"><path d="{GH_PATH}"/></g>
<circle cx="146" cy="42" r="9" fill="url(#redg)"/>
<rect x="164" y="31" width="440" height="22" rx="11" fill="#151922" stroke="#242a36"/>
<text x="180" y="46" font-family="{FONT}" font-size="11.5" fill="#9aa4b2">{esc(c["username"])} / <tspan fill="#e6edf3">README.md</tspan></text>
<text x="916" y="46" text-anchor="end" font-family="{FONT}" font-size="11.5" fill="#7d8590">Preview</text>
<line x1="21" y1="64" x2="939" y2="64" stroke="#1d222c"/>'''


def header(c):
    chips, x = "", 350
    for ch in c["chips"]:
        w = 14 + len(ch) * 7
        chips += (f'<rect x="{x}" y="176" width="{w}" height="22" rx="11" fill="#1a0c10" stroke="#5a1a22"/>'
                  f'<text x="{x + w / 2}" y="191" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#ffb4ba">{esc(ch)}</text>')
        x += w + 8
    q1, q2 = c["quote"]
    return f'''
<text x="350" y="136" font-family="{FONT}" font-size="46" font-weight="800" fill="url(#redg)" filter="url(#glow)" letter-spacing="2">{esc(c["name"])}</text>
<text x="352" y="162" font-family="{FONT}" font-size="14" fill="#9aa4b2"><tspan fill="{RED}">&gt;</tspan> {esc(c["role"])}</text>
{chips}
<rect x="350" y="212" width="570" height="64" rx="10" fill="#0a0c11" stroke="#22262f"/>
<rect x="350" y="212" width="4" height="64" rx="2" fill="{RED}"/>
<text x="372" y="238" font-family="{FONT}" font-size="12.5" font-style="italic" fill="#c9d1d9">“{esc(q1)}</text>
<text x="372" y="258" font-family="{FONT}" font-size="12.5" font-style="italic" fill="#c9d1d9">{esc(q2)}”<tspan fill="{RED}">▌<animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></tspan></text>'''


def stats(c):
    shapes = [[.35, .55, .45, .8, 1], [.5, .7, .4, .9, .65], [.4, .4, .7, .55, .9], [.3, .5, .6, .8, 1]]
    out = ""
    for i, (label, val) in enumerate(c["stats"]):
        x, y = 350 + i * 146, 292
        out += (f'<rect x="{x}" y="{y}" width="132" height="84" rx="10" fill="#0a0c11" stroke="#22262f"/>'
                f'<text x="{x + 14}" y="{y + 40}" font-family="{FONT}" font-size="22" font-weight="800" fill="#fff">{esc(val)}</text>'
                f'<text x="{x + 14}" y="{y + 62}" font-family="{FONT}" font-size="11" fill="#8b94a3">{esc(label)}</text>')
        for j, h in enumerate(shapes[i % 4]):
            bh, bx, base = 40 * h, x + 92 + j * 7, y + 66
            out += (f'<rect x="{bx}" y="{base - bh:.1f}" width="4" height="{bh:.1f}" rx="1.5" fill="{RED}" opacity="{.45 + .11 * j:.2f}">'
                    f'<animate attributeName="height" from="0" to="{bh:.1f}" dur=".9s" begin="{j * .08:.2f}s" fill="freeze"/>'
                    f'<animate attributeName="y" from="{base}" to="{base - bh:.1f}" dur=".9s" begin="{j * .08:.2f}s" fill="freeze"/></rect>')
    return out


def skills(c):
    out = (f'<rect x="40" y="396" width="290" height="164" rx="12" fill="#0a0c11" stroke="#22262f"/>'
           f'<text x="58" y="422" font-family="{FONT}" font-size="12.5" font-weight="700" fill="#fff">Tech Stack</text>'
           f'<circle cx="312" cy="418" r="3.5" fill="{RED}"><animate attributeName="opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/></circle>')
    for i, (lang, pct) in enumerate(c["skills"]):
        y = 448 + i * 27
        out += (f'<text x="58" y="{y + 8}" font-family="{FONT}" font-size="11" fill="#c9d1d9">{esc(lang)}</text>'
                f'<rect x="136" y="{y}" width="130" height="8" rx="4" fill="#1a1e27"/>'
                f'<rect x="136" y="{y}" width="{130 * pct / 100:.1f}" height="8" rx="4" fill="url(#redh)">'
                f'<animate attributeName="width" from="0" to="{130 * pct / 100:.1f}" dur="1.2s" fill="freeze"/></rect>'
                f'<text x="312" y="{y + 8}" text-anchor="end" font-family="{FONT}" font-size="11" fill="#8b94a3">{pct}%</text>')
    return out


def repos(c):
    out = (f'<rect x="350" y="392" width="570" height="168" rx="12" fill="#0a0c11" stroke="#22262f"/>'
           f'<text x="368" y="418" font-family="{FONT}" font-size="12.5" font-weight="700" fill="#fff">Featured Repositories</text>')
    for i, (name, desc, lang, col, stars) in enumerate(c["repos"][:3]):
        y = 430 + i * 42
        out += (f'<rect x="364" y="{y}" width="542" height="36" rx="8" fill="#0d1016" stroke="#1d222c"/>'
                f'<rect x="378" y="{y + 11}" width="12" height="14" rx="2" fill="none" stroke="{RED}" stroke-width="1.5"/>'
                f'<text x="400" y="{y + 15}" font-family="{FONT}" font-size="12" font-weight="700" fill="#e6edf3">{esc(name)}</text>'
                f'<text x="400" y="{y + 29}" font-family="{FONT}" font-size="10" fill="#7d8590">{esc(desc)}</text>'
                f'<circle cx="716" cy="{y + 18}" r="4.5" fill="{col}"/>'
                f'<text x="726" y="{y + 22}" font-family="{FONT}" font-size="11" fill="#9aa4b2">{esc(lang)}</text>'
                f'<text x="860" y="{y + 22}" font-family="{FONT}" font-size="12" fill="#f5b82e">★</text>'
                f'<text x="876" y="{y + 22}" font-family="{FONT}" font-size="11" fill="#c9d1d9">{esc(stars)}</text>')
    return out


def build(photo=None):
    c = CONFIG
    img = photo_portrait(photo) if photo else devil_portrait()
    panel = (f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="12" fill="#07080c" stroke="#3a1419"/>'
             f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="12" fill="url(#vig)"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="600" viewBox="0 0 960 600" role="img" aria-label="{esc(c["name"])} GitHub profile card">
<defs>
  <linearGradient id="redg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{RED2}"/><stop offset="1" stop-color="{RED}"/></linearGradient>
  <linearGradient id="redh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#b3121f"/><stop offset="1" stop-color="{RED}"/></linearGradient>
  <linearGradient id="ascii" gradientUnits="userSpaceOnUse" x1="0" y1="{PY}" x2="0" y2="{PY + PH}"><stop offset="0" stop-color="#ff8a6a"/><stop offset=".55" stop-color="{RED}"/><stop offset="1" stop-color="#8f1020"/></linearGradient>
  <radialGradient id="vig" cx=".5" cy=".42" r=".7"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".75"/></radialGradient>
  <radialGradient id="bg" cx=".15" cy="0" r="1.1"><stop offset="0" stop-color="#2a0a10"/><stop offset=".5" stop-color="#0b0d12"/><stop offset="1" stop-color="#06070a"/></radialGradient>
  <filter id="glow" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="960" height="600" rx="22" fill="url(#bg)"/>
<rect x="20.5" y="20.5" width="919" height="559" rx="14" fill="#0d1016" fill-opacity=".92" stroke="#262b36"/>
{titlebar(c)}
{panel}
{portrait_svg(img, photo is None)}
{header(c)}
{stats(c)}
{skills(c)}
{repos(c)}
</svg>'''


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--photo", help="path to your photo (optional)")
    ap.add_argument("--out", default="assets/profile-card.svg")
    a = ap.parse_args()
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(build(a.photo))
    print("written ->", a.out)
