# Generates the animated SVGs of the profile README (assets/banner.svg and
# assets/terminal.svg).
#
# Usage: python3 scripts/gen_svgs.py assets
#
# SMIL only (no CSS animations, no web fonts): GitHub serves the SVGs as <img>,
# where SMIL keeps working and external resources are blocked. After changing an
# SVG, bump the ?v= query on its <img> in README.md, or GitHub keeps serving the
# cached copy.
import os, random, sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]
random.seed(230)
MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,'Liberation Mono',monospace"
GREEN, CYAN, PURPLE, RED = "#00ff88", "#00e5ff", "#b16cff", "#ff2e63"
CW = 0.6  # monospace advance as a fraction of the font size


def typing_values(n, width_per_char):
    return ";".join(f"{i * width_per_char:.1f}" for i in range(n + 1))


# ------------------------------------------------------------------ banner
def banner():
    W, H = 1200, 340
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

    sub = "> software engineer  //  solutions architect  //  offensive security"
    fs = 22
    sub_w = len(sub) * fs * CW
    sub_x = (W - sub_w) / 2
    type_dur = 2.8
    vals = typing_values(len(sub), fs * CW)
    cursor_x = ";".join(f"{sub_x + float(v):.1f}" for v in vals.split(";"))

    # glitch: discrete jitter on two coloured copies, clipped to a moving band
    jit = "0;0;0;0;0;0;5;-4;0;0;0;0;0;0;0;-6;3;0;0;0"
    band = "0;0;0;0;0;0;120;150;0;0;0;0;0;0;0;95;135;0;0;0"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Kawe Maximo: software engineer, solutions architect, offensive security">
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
<text x="600" y="160" text-anchor="middle" font-family="{MONO}" font-size="88" font-weight="800" letter-spacing="10" fill="{GREEN}" opacity=".45" filter="url(#glow)">KAWE MAXIMO</text>
<g clip-path="url(#band)">
  <text x="600" y="160" text-anchor="middle" font-family="{MONO}" font-size="88" font-weight="800" letter-spacing="10" fill="{RED}" opacity=".85">KAWE MAXIMO
    <animate attributeName="x" values="{";".join(str(600 + int(v)) for v in jit.split(";"))}" dur="3.2s" calcMode="discrete" repeatCount="indefinite"/></text>
  <text x="600" y="160" text-anchor="middle" font-family="{MONO}" font-size="88" font-weight="800" letter-spacing="10" fill="{CYAN}" opacity=".85">KAWE MAXIMO
    <animate attributeName="x" values="{";".join(str(600 - int(v)) for v in jit.split(";"))}" dur="3.2s" calcMode="discrete" repeatCount="indefinite"/></text>
</g>
<text x="600" y="160" text-anchor="middle" font-family="{MONO}" font-size="88" font-weight="800" letter-spacing="10" fill="url(#name)">KAWE MAXIMO</text>

<!-- typed subtitle + cursor -->
<text x="{sub_x:.1f}" y="225" font-family="{MONO}" font-size="{fs}" fill="#9fb3c8" textLength="{sub_w:.1f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#typed)">{escape(sub)}</text>
<rect x="{sub_x:.1f}" y="206" width="12" height="24" fill="{GREEN}">
  <animate attributeName="x" values="{cursor_x}" dur="{type_dur}s" begin="0.8s" calcMode="discrete" fill="freeze"/>
  <animate attributeName="opacity" values="1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/>
</rect>

<!-- motto -->
<text x="600" y="276" text-anchor="middle" font-family="{MONO}" font-size="15" letter-spacing="7" fill="{GREEN}" opacity="0">BUILD IT · BREAK IT · HARDEN IT
  <animate attributeName="opacity" values="0;1" dur="0.8s" begin="3.8s" fill="freeze"/></text>

<!-- HUD -->
<g fill="none" stroke="{GREEN}" stroke-opacity=".55" stroke-width="2">
  <path d="M24 54V24H54"/><path d="M{W - 54} 24H{W - 24}V54"/><path d="M24 {H - 54}V{H - 24}H54"/><path d="M{W - 54} {H - 24}H{W - 24}V{H - 54}"/>
</g>
<g font-family="{MONO}" font-size="12" fill="#5f8a74" letter-spacing="1.5">
  <circle cx="74" cy="38" r="4" fill="{GREEN}"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></circle>
  <text x="86" y="42">SYS::ONLINE</text>
  <text x="{W - 74}" y="42" text-anchor="end">LAT -23.52 · LON -46.18 · MOGI DAS CRUZES</text>
  <text x="74" y="{H - 34}">root@kawe:~#</text>
  <text x="{W - 74}" y="{H - 34}" text-anchor="end">PURPLE TEAM · BUILD ▸ BREAK ▸ HARDEN</text>
</g>

<!-- CRT -->
<rect width="{W}" height="{H}" rx="16" fill="url(#scan)" pointer-events="none"/>
<rect x="0" y="-20" width="{W}" height="60" fill="{GREEN}" opacity=".05">
  <animate attributeName="y" values="-60;{H}" dur="5s" repeatCount="indefinite"/></rect>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="none" stroke="{GREEN}" stroke-opacity=".18"/>
</svg>
'''


# ---------------------------------------------------------------- terminal
def terminal():
    W = 1000
    fs, lh, x0, y0 = 16, 27, 28, 84
    cw = fs * CW
    prompt = "kawe@kali:~$ "
    script = [
        ("cmd", "whoami", 0.4),
        ("out", [("Kawe Maximo", "#e6edf3"), (" — software engineer · solutions architect · offensive security", "#8b949e")], 1.2),
        ("cmd", "cat ./focus", 1.8),
        ("out", [("[web/api pentest]  ", GREEN), ("[cloud & iot hardening]  ", CYAN), ("[distributed systems]  ", PURPLE), ("[secure sdlc]", "#f2cc60")], 2.6),
        ("cmd", "nmap -sV --top-ports 5 kawe", 3.2),
        ("out", [("PORT      STATE  SERVICE         DETAILS", "#6e7681")], 4.6),
        ("port", ("443/tcp ", "web-appsec    ", "owasp top 10 · authn/authz · api abuse"), 4.8),
        ("port", ("1883/tcp", "iot-security  ", "mqtt · edge devices · raspberry pi fleets"), 5.0),
        ("port", ("8080/tcp", "cloud-security", "gcp iam · least privilege · secrets"), 5.2),
        ("port", ("22/tcp  ", "linux         ", "hardening · privesc · automation"), 5.4),
        ("port", ("9418/tcp", "secure-coding ", "threat modeling · sast/dast · ci/cd"), 5.6),
        ("cmd", "echo $MOTTO", 6.3),
        ("out", [('"Build it. Break it. Harden it."', GREEN)], 7.1),
        ("end", None, 7.5),
    ]
    H = y0 + lh * len(script) + 10
    body, defs = [], []
    for i, (kind, data, t) in enumerate(script):
        y = y0 + i * lh
        show = f'<set attributeName="opacity" to="1" begin="{t}s" fill="freeze"/>'
        if kind == "cmd":
            px = x0 + len(prompt) * cw
            dur = max(0.4, len(data) * 0.06)
            defs.append(
                f'<clipPath id="c{i}"><rect x="{px:.1f}" y="{y - fs}" height="{lh}" width="0">'
                f'<animate attributeName="width" values="{typing_values(len(data), cw)}" dur="{dur:.2f}s" '
                f'begin="{t + 0.15:.2f}s" calcMode="discrete" fill="freeze"/></rect></clipPath>'
            )
            body.append(
                f'<g opacity="0">{show}<text x="{x0}" y="{y}" fill="{GREEN}" xml:space="preserve" textLength="{len(prompt) * cw:.1f}" lengthAdjust="spacingAndGlyphs">kawe@kali<tspan fill="#8b949e">:</tspan>'
                f'<tspan fill="{CYAN}">~</tspan><tspan fill="#8b949e">$ </tspan></text>'
                f'<text x="{px:.1f}" y="{y}" fill="#e6edf3" textLength="{len(data) * cw:.1f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#c{i})">{escape(data)}</text></g>'
            )
        elif kind == "out":
            spans = "".join(f'<tspan fill="{c}">{escape(s)}</tspan>' for s, c in data)
            body.append(f'<g opacity="0">{show}<text x="{x0}" y="{y}" xml:space="preserve">{spans}</text></g>')
        elif kind == "port":
            port, svc, det = data
            body.append(
                f'<g opacity="0">{show}<text x="{x0}" y="{y}" xml:space="preserve">'
                f'<tspan fill="#e6edf3">{escape(port)}  </tspan><tspan fill="{GREEN}">open   </tspan>'
                f'<tspan fill="{CYAN}">{escape(svc)}  </tspan><tspan fill="#8b949e">{escape(det)}</tspan></text></g>'
            )
        else:
            px = x0 + len(prompt) * cw
            body.append(
                f'<g opacity="0">{show}<text x="{x0}" y="{y}" fill="{GREEN}" xml:space="preserve" textLength="{len(prompt) * cw:.1f}" lengthAdjust="spacingAndGlyphs">kawe@kali<tspan fill="#8b949e">:</tspan>'
                f'<tspan fill="{CYAN}">~</tspan><tspan fill="#8b949e">$ </tspan></text>'
                f'<rect x="{px:.1f}" y="{y - fs + 2}" width="{cw:.1f}" height="{fs + 2}" fill="{GREEN}">'
                f'<animate attributeName="opacity" values="1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect></g>'
            )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Terminal: whoami, focus areas and an nmap scan of Kawe's skills">
<defs>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity=".5"/><stop offset="1" stop-color="{PURPLE}" stop-opacity=".5"/></linearGradient>
  {"".join(defs)}
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="#0d1117" stroke="url(#edge)" stroke-width="1.5"/>
<path d="M1 15A14 14 0 0 1 15 1H{W - 15}A14 14 0 0 1 {W - 1} 15V42H1Z" fill="#161b22"/>
<line x1="1" y1="42" x2="{W - 1}" y2="42" stroke="#30363d"/>
<circle cx="26" cy="22" r="6.5" fill="#ff5f56"/><circle cx="48" cy="22" r="6.5" fill="#ffbd2e"/><circle cx="70" cy="22" r="6.5" fill="#27c93f"/>
<text x="{W / 2}" y="27" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#8b949e">kawe@kali: ~ — zsh</text>
<g font-family="{MONO}" font-size="{fs}">{"".join(body)}</g>
</svg>
'''


for name, fn in (("banner.svg", banner), ("terminal.svg", terminal)):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(fn())
print("ok")
