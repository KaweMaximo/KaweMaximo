# Generates the animated SVGs of the profile README (assets/banner.svg and
# assets/terminal.svg) from profile.toml.
#
# Usage: python3 scripts/gen_svgs.py [--config profile.toml] [--out assets]
#
# Needs Python 3.11+ (tomllib) and nothing else. SMIL only (no CSS animations,
# no web fonts): GitHub serves the SVGs as <img>, where SMIL keeps working and
# external resources are blocked. After rebuilding, bump the ?v= query on each
# <img> in README.md, or GitHub keeps serving the cached copy; the "build
# profile" workflow does both on every change to profile.toml.
import argparse
import os
import random
import sys
from xml.sax.saxutils import escape

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    sys.exit("gen_svgs.py needs Python 3.11 or newer (for tomllib).")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,'Liberation Mono',monospace"
GREEN, CYAN, PURPLE, RED = "#00ff88", "#00e5ff", "#b16cff", "#ff2e63"
COLORS = {
    "green": GREEN, "cyan": CYAN, "purple": PURPLE, "red": RED,
    "yellow": "#f2cc60", "white": "#e6edf3", "gray": "#8b949e", "dim": "#6e7681",
}
CW = 0.6  # monospace advance as a fraction of the font size


def fail(msg):
    sys.exit(f"profile.toml: {msg}")


def color(name):
    if isinstance(name, str) and name.startswith("#") and len(name) in (4, 7):
        return name
    if name not in COLORS:
        fail(f"unknown color {name!r}; use one of {', '.join(COLORS)} or #rrggbb")
    return COLORS[name]


def typing_values(n, width_per_char):
    return ";".join(f"{i * width_per_char:.1f}" for i in range(n + 1))


# ------------------------------------------------------------------ banner
def banner(cfg):
    W, H = 1200, 340
    name = cfg.get("name", "")
    sub = cfg.get("subtitle", "")
    if not name:
        fail("[banner] needs a name")
    random.seed(cfg.get("seed", 230))

    rain = []
    for i in range(26):
        x = 20 + i * 45 + random.randint(-8, 8)
        chars = "".join(random.choice("0123456789ABCDEF<>/{}$#") for _ in range(16))
        spans = "".join(f'<tspan x="{x}" dy="17">{escape(c)}</tspan>' for c in chars)
        dur = random.uniform(5, 11)
        begin = random.uniform(0, 8)
        op = random.choice([0.10, 0.14, 0.18, 0.24])
        rain.append(
            f'<g opacity="{op}" transform="translate(0 -300)"><text font-family="{MONO}" font-size="14" fill="{GREEN}">{spans}</text>'
            f'<animateTransform attributeName="transform" type="translate" values="0 -300;0 {H + 20}" '
            f'dur="{dur:.2f}s" begin="{begin:.2f}s" repeatCount="indefinite"/></g>'
        )

    # Long names and subtitles shrink to fit the 1200px banner.
    nfs = min(88, int(1080 / (len(name) * (CW + 10 / 88))))
    ls = f"{10 * nfs / 88:g}"
    fs = min(22, int(1100 / (max(len(sub), 1) * CW)))
    sub_w = len(sub) * fs * CW
    sub_x = (W - sub_w) / 2
    type_dur = 2.8
    vals = typing_values(len(sub), fs * CW)
    cursor_x = ";".join(f"{sub_x + float(v):.1f}" for v in vals.split(";"))
    label = cfg.get("description") or f"{name}: {sub.lstrip('> ').strip()}"

    # glitch: discrete jitter on two coloured copies, clipped to a moving band
    jit = "0;0;0;0;0;0;5;-4;0;0;0;0;0;0;0;-6;3;0;0;0"
    band = "0;0;0;0;0;0;120;150;0;0;0;0;0;0;0;95;135;0;0;0"
    name_attrs = f'x="600" y="160" text-anchor="middle" font-family="{MONO}" font-size="{nfs}" font-weight="800" letter-spacing="{ls}"'
    name_txt = escape(name)

    hud = []
    if cfg.get("top_left", ""):
        hud.append(f'<circle cx="74" cy="38" r="4" fill="{GREEN}"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></circle>')
        hud.append(f'<text x="86" y="42">{escape(cfg["top_left"])}</text>')
    if cfg.get("top_right", ""):
        hud.append(f'<text x="{W - 74}" y="42" text-anchor="end">{escape(cfg["top_right"])}</text>')
    if cfg.get("bottom_left", ""):
        hud.append(f'<text x="74" y="{H - 34}">{escape(cfg["bottom_left"])}</text>')
    if cfg.get("bottom_right", ""):
        hud.append(f'<text x="{W - 74}" y="{H - 34}" text-anchor="end">{escape(cfg["bottom_right"])}</text>')
    hud = "\n  ".join(hud)

    motto = ""
    if cfg.get("motto", ""):
        motto = f'''<text x="600" y="276" text-anchor="middle" font-family="{MONO}" font-size="15" letter-spacing="7" fill="{GREEN}" opacity="0">{escape(cfg["motto"])}
  <animate attributeName="opacity" values="0;1" dur="0.8s" begin="3.8s" fill="freeze"/></text>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(label, {'"': "&quot;"})}">
<defs>
  <radialGradient id="bg" cx="50%" cy="45%" r="80%">
    <stop offset="0" stop-color="#0b1d16"/><stop offset=".55" stop-color="#070b10"/><stop offset="1" stop-color="#020305"/>
  </radialGradient>
  <linearGradient id="name" x1="0" y1="0" x2="1" y2="0" spreadMethod="reflect">
    <stop offset="0" stop-color="{GREEN}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="0 0;2 0" dur="9s" repeatCount="indefinite"/>
  </linearGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="{GREEN}" stroke-opacity=".07"/>
  </pattern>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#000" fill-opacity=".35"/>
  </pattern>
  <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".35" stop-color="#fff" stop-opacity="1"/>
    <stop offset=".75" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="fadeMask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
  <clipPath id="band"><rect x="0" y="0" width="{W}" height="14">
    <animate attributeName="y" values="{band}" dur="3.2s" calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>
  <clipPath id="typed"><rect x="{sub_x:.1f}" y="200" height="34" width="0">
    <animate attributeName="width" values="{vals}" dur="{type_dur}s" begin="0.8s" calcMode="discrete" fill="freeze"/></rect></clipPath>
</defs>

<rect width="{W}" height="{H}" rx="16" fill="url(#bg)"/>
<g mask="url(#fadeMask)">
  <g><rect y="-40" width="{W}" height="{H + 80}" fill="url(#grid)"/>
    <animateTransform attributeName="transform" type="translate" values="0 0;0 40" dur="2.5s" repeatCount="indefinite"/></g>
</g>
<g>{"".join(rain)}</g>

<!-- name -->
<text {name_attrs} fill="{GREEN}" opacity=".45" filter="url(#glow)">{name_txt}</text>
<g clip-path="url(#band)">
  <text {name_attrs} fill="{RED}" opacity=".85">{name_txt}
    <animate attributeName="x" values="{";".join(str(600 + int(v)) for v in jit.split(";"))}" dur="3.2s" calcMode="discrete" repeatCount="indefinite"/></text>
  <text {name_attrs} fill="{CYAN}" opacity=".85">{name_txt}
    <animate attributeName="x" values="{";".join(str(600 - int(v)) for v in jit.split(";"))}" dur="3.2s" calcMode="discrete" repeatCount="indefinite"/></text>
</g>
<text {name_attrs} fill="url(#name)">{name_txt}</text>

<!-- typed subtitle + cursor -->
<text x="{sub_x:.1f}" y="225" font-family="{MONO}" font-size="{fs}" fill="#9fb3c8" textLength="{sub_w:.1f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#typed)">{escape(sub)}</text>
<rect x="{sub_x:.1f}" y="206" width="12" height="24" fill="{GREEN}">
  <animate attributeName="x" values="{cursor_x}" dur="{type_dur}s" begin="0.8s" calcMode="discrete" fill="freeze"/>
  <animate attributeName="opacity" values="1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/>
</rect>

<!-- motto -->
{motto}

<!-- HUD -->
<g fill="none" stroke="{GREEN}" stroke-opacity=".55" stroke-width="2">
  <path d="M24 54V24H54"/><path d="M{W - 54} 24H{W - 24}V54"/><path d="M24 {H - 54}V{H - 24}H54"/><path d="M{W - 54} {H - 24}H{W - 24}V{H - 54}"/>
</g>
<g font-family="{MONO}" font-size="12" fill="#5f8a74" letter-spacing="1.5">
  {hud}
</g>

<!-- CRT -->
<rect width="{W}" height="{H}" rx="16" fill="url(#scan)" pointer-events="none"/>
<rect x="0" y="-20" width="{W}" height="60" fill="{GREEN}" opacity=".05">
  <animate attributeName="y" values="-60;{H}" dur="5s" repeatCount="indefinite"/></rect>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="none" stroke="{GREEN}" stroke-opacity=".18"/>
</svg>
'''


# ---------------------------------------------------------------- terminal
def schedule(lines):
    """Start time of each line: a command is typed out, then its output
    follows line by line, then a pause before the next command."""
    times, t, prev = [], 0.4, None
    for line in lines:
        if "cmd" in line:
            if prev is not None:
                t += 0.6
            times.append(round(t, 2))
            t += 0.15 + max(0.4, len(line["cmd"]) * 0.06)
        else:
            t += 0.25 if prev == "cmd" else 0.2
            times.append(round(t, 2))
        prev = "cmd" if "cmd" in line else "out"
    return times, round(t + 0.4, 2)


def terminal(cfg):
    W = 1000
    fs, lh, x0, y0 = 16, 27, 28, 84
    cw = fs * CW
    user, host = cfg.get("user", "user"), cfg.get("host", "host")
    lines = cfg.get("lines", [])
    if not lines:
        fail("[terminal] needs at least one [[terminal.lines]] block")
    prompt = f"{user}@{host}:~$ "
    prompt_svg = (
        f'{escape(user)}@{escape(host)}<tspan fill="#8b949e">:</tspan>'
        f'<tspan fill="{CYAN}">~</tspan><tspan fill="#8b949e">$ </tspan>'
    )
    max_chars = int((W - 2 * x0) / cw)
    for n, line in enumerate(lines, 1):
        if ("cmd" in line) == ("out" in line):
            fail(f"line {n} needs exactly one of cmd or out")
        width = len(prompt) + len(line["cmd"]) if "cmd" in line else sum(len(p[0]) for p in line["out"])
        if width > max_chars:
            print(f"warning: terminal line {n} has {width} characters and the window fits {max_chars}", file=sys.stderr)

    times, end_at = schedule(lines)
    H = y0 + lh * (len(lines) + 1) + 10
    body, defs = [], []
    for i, (line, t) in enumerate(zip(lines, times)):
        y = y0 + i * lh
        show = f'<set attributeName="opacity" to="1" begin="{t:g}s" fill="freeze"/>'
        if "cmd" in line:
            data = line["cmd"]
            px = x0 + len(prompt) * cw
            dur = max(0.4, len(data) * 0.06)
            defs.append(
                f'<clipPath id="c{i}"><rect x="{px:.1f}" y="{y - fs}" height="{lh}" width="0">'
                f'<animate attributeName="width" values="{typing_values(len(data), cw)}" dur="{dur:.2f}s" '
                f'begin="{t + 0.15:.2f}s" calcMode="discrete" fill="freeze"/></rect></clipPath>'
            )
            body.append(
                f'<g opacity="0">{show}<text x="{x0}" y="{y}" fill="{GREEN}" xml:space="preserve" textLength="{len(prompt) * cw:.1f}" lengthAdjust="spacingAndGlyphs">{prompt_svg}</text>'
                f'<text x="{px:.1f}" y="{y}" fill="#e6edf3" textLength="{len(data) * cw:.1f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#c{i})">{escape(data)}</text></g>'
            )
        else:
            spans = "".join(f'<tspan fill="{color(c)}">{escape(s)}</tspan>' for s, c in line["out"])
            body.append(f'<g opacity="0">{show}<text x="{x0}" y="{y}" xml:space="preserve">{spans}</text></g>')

    # the idle prompt with a blinking cursor, once everything has played
    y = y0 + len(lines) * lh
    px = x0 + len(prompt) * cw
    body.append(
        f'<g opacity="0"><set attributeName="opacity" to="1" begin="{end_at:g}s" fill="freeze"/>'
        f'<text x="{x0}" y="{y}" fill="{GREEN}" xml:space="preserve" textLength="{len(prompt) * cw:.1f}" lengthAdjust="spacingAndGlyphs">{prompt_svg}</text>'
        f'<rect x="{px:.1f}" y="{y - fs + 2}" width="{cw:.1f}" height="{fs + 2}" fill="{GREEN}">'
        f'<animate attributeName="opacity" values="1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect></g>'
    )
    title = cfg.get("title") or f"{user}@{host}: ~ — zsh"
    label = cfg.get("description") or "Terminal: " + ", ".join(line["cmd"] for line in lines if "cmd" in line)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(label, {'"': "&quot;"})}">
<defs>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity=".5"/><stop offset="1" stop-color="{PURPLE}" stop-opacity=".5"/></linearGradient>
  {"".join(defs)}
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="#0d1117" stroke="url(#edge)" stroke-width="1.5"/>
<path d="M1 15A14 14 0 0 1 15 1H{W - 15}A14 14 0 0 1 {W - 1} 15V42H1Z" fill="#161b22"/>
<line x1="1" y1="42" x2="{W - 1}" y2="42" stroke="#30363d"/>
<circle cx="26" cy="22" r="6.5" fill="#ff5f56"/><circle cx="48" cy="22" r="6.5" fill="#ffbd2e"/><circle cx="70" cy="22" r="6.5" fill="#27c93f"/>
<text x="{W / 2:g}" y="27" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#8b949e">{escape(title)}</text>
<g font-family="{MONO}" font-size="{fs}">{"".join(body)}</g>
</svg>
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default=os.path.join(ROOT, "profile.toml"))
    ap.add_argument("--out", default=os.path.join(ROOT, "assets"))
    args = ap.parse_args()
    try:
        with open(args.config, "rb") as f:
            cfg = tomllib.load(f)
    except (OSError, tomllib.TOMLDecodeError) as e:
        sys.exit(f"cannot read {args.config}: {e}")
    os.makedirs(args.out, exist_ok=True)
    for name, svg in (("banner.svg", banner(cfg.get("banner", {}))), ("terminal.svg", terminal(cfg.get("terminal", {})))):
        with open(os.path.join(args.out, name), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {os.path.join(args.out, name)}")


if __name__ == "__main__":
    main()
