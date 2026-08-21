# -*- coding: utf-8 -*-
"""Genere assets/contributions.svg — heatmap rose des contributions GitHub.

Les donnees viennent de l'endpoint public https://github.com/users/<user>/contributions :
pas de token, pas de dependance externe, donc rien qui puisse expirer ou etre
rate-limite. Le SVG est statique (aucune animation) : GitHub bloque les animations
dans les images distantes, un graphe anime s'afficherait fige.
"""
import io, os, re, sys, urllib.request

USER = os.environ.get("GH_USER", "PINKKAGUY")
OUT  = os.path.join("assets", "contributions.svg")

PINK, DIM = "#FF1F8F", "#8A7E86"
FONT   = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
LEVELS = ["#1d1018", "#5c1338", "#a01f63", "#d92a80", "#FF4DA0"]
MONTHS = ["janv", u"févr", "mars", "avr", "mai", "juin",
          "juil", u"août", "sept", "oct", "nov", u"déc"]
CELL, GAP = 12, 3
STEP = CELL + GAP
LEFT, TOP = 22, 46


def fetch(user):
    req = urllib.request.Request(
        "https://github.com/users/%s/contributions" % user,
        headers={"User-Agent": "profile-readme-heatmap"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8")


def parse(html):
    """-> (jours tries [(date, level)], total)"""
    days = [(m.group(1), int(m.group(2))) for m in
            re.finditer(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*data-level="(\d)"', html)]
    if not days:
        sys.exit("aucune donnee de contribution trouvee pour %s" % USER)
    total = sum(int(n) for n in re.findall(r'>\s*(\d+)\s+contributions?\s+on\s', html))
    return sorted(set(days)), total


def build(days, total):
    first = days[0][0]
    y, m, d = (int(x) for x in first.split("-"))
    import datetime
    start_weekday = (datetime.date(y, m, d).weekday() + 1) % 7   # 0 = dimanche

    cells = []
    for i, (date, level) in enumerate(days):
        idx = start_weekday + i
        cells.append((idx // 7, idx % 7, date, level))
    n_weeks = max(c[0] for c in cells) + 1

    W = LEFT + n_weeks * STEP + 16
    H = TOP + 7 * STEP + 40
    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" fill="none">'
         % (W, H, W, H)]
    o.append('<rect x="0" y="0" width="%d" height="%d" rx="14" fill="#0f0810" stroke="%s" stroke-opacity="0.4"/>'
             % (W, H, PINK))
    o.append('<text x="%d" y="26" fill="%s" font-family="%s" font-size="13" font-weight="700">%d contributions cette année</text>'
             % (LEFT, PINK, FONT, total))

    seen = None
    for wk, wd, date, _ in cells:
        month = int(date[5:7])
        if wd == 0 and month != seen and int(date[8:10]) <= 7:
            o.append('<text x="%d" y="%d" fill="%s" font-family="%s" font-size="9.5">%s</text>'
                     % (LEFT + wk * STEP, TOP - 8, DIM, FONT, MONTHS[month - 1]))
            seen = month

    for wk, wd, _, level in cells:
        o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s"/>'
                 % (LEFT + wk * STEP, TOP + wd * STEP, CELL, CELL, LEVELS[level]))

    ly = TOP + 7 * STEP + 18
    lx = W - 16 - (5 * STEP + 74)
    o.append('<text x="%d" y="%d" fill="%s" font-family="%s" font-size="9.5" dominant-baseline="middle">moins</text>'
             % (lx, ly, DIM, FONT))
    for i, c in enumerate(LEVELS):
        o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s"/>'
                 % (lx + 38 + i * STEP, ly - CELL // 2, CELL, CELL, c))
    o.append('<text x="%d" y="%d" fill="%s" font-family="%s" font-size="9.5" dominant-baseline="middle">plus</text>'
             % (lx + 38 + 5 * STEP + 6, ly, DIM, FONT))
    o.append('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    days, total = parse(fetch(USER))
    svg = build(days, total)
    if not os.path.isdir("assets"):
        os.makedirs("assets")
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(svg)
    print("%s ecrit : %d jours, %d contributions" % (OUT, len(days), total))
