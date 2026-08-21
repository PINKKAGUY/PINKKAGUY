# -*- coding: utf-8 -*-
"""Genere assets/contributions.svg : la heatmap des contributions GitHub.

Les donnees viennent de l'endpoint public https://github.com/users/<user>/contributions :
pas de token, pas de dependance externe, donc rien qui puisse expirer ou etre
rate-limite. Le SVG est statique (aucune animation) : GitHub bloque les animations
dans les images distantes, un graphe anime s'afficherait fige.
"""
import datetime, os, re, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import style as S
from style import PINK, DIM, PAD, TITLE_H

USER = os.environ.get("GH_USER", "PINKKAGUY")
OUT  = os.path.join("assets", "contributions.svg")

LEVELS = ["#1d1018", "#5c1338", "#a01f63", "#d92a80", "#FF4DA0"]
MONTHS = ["janv", u"févr", "mars", "avr", "mai", "juin",
          "juil", u"août", "sept", "oct", "nov", u"déc"]
CELL, GAP = 12, 3
STEP = CELL + GAP


def fetch(user):
    req = urllib.request.Request(
        "https://github.com/users/%s/contributions" % user,
        headers={"User-Agent": "profile-readme-heatmap"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8")


def parse(html):
    """-> (jours tries [(date, niveau)], total annuel)"""
    days = [(m.group(1), int(m.group(2))) for m in
            re.finditer(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*data-level="(\d)"', html)]
    if not days:
        sys.exit("aucune donnee de contribution trouvee pour %s" % USER)
    total = sum(int(n) for n in re.findall(r'>\s*(\d+)\s+contributions?\s+on\s', html))
    return sorted(set(days)), total


def build(days, total):
    y, m, d = (int(x) for x in days[0][0].split("-"))
    first_col = (datetime.date(y, m, d).weekday() + 1) % 7   # 0 = dimanche

    cells = []
    for i, (date, level) in enumerate(days):
        idx = first_col + i
        cells.append((idx // 7, idx % 7, date, level))

    n_weeks = max(c[0] for c in cells) + 1
    grid_w = n_weeks * STEP - GAP
    left = (S.W - grid_w) / 2.0
    top = TITLE_H + 14
    h = top + 7 * STEP + 34

    o = S.open_svg(h)
    S.frame(o, h)
    S.section_title(o, u"Mes contributions")
    S.text(o, u"%d cette année" % total, S.W - PAD, 30, 12, PINK, "700", "end")

    seen = None
    for wk, wd, date, _ in cells:
        month = int(date[5:7])
        if wd == 0 and month != seen and int(date[8:10]) <= 7:
            S.text(o, MONTHS[month - 1], left + wk * STEP, top - 8, 9.5, DIM)
            seen = month

    for wk, wd, _, level in cells:
        o.append('<rect x="%.1f" y="%d" width="%d" height="%d" rx="3" fill="%s"/>'
                 % (left + wk * STEP, top + wd * STEP, CELL, CELL, LEVELS[level]))

    ly = top + 7 * STEP + 14
    lx = left + grid_w - (5 * STEP + 70)
    S.text(o, "moins", lx, ly + 4, 9.5, DIM)
    for i, c in enumerate(LEVELS):
        o.append('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="3" fill="%s"/>'
                 % (lx + 36 + i * STEP, ly - CELL / 2.0 + 4, CELL, CELL, c))
    S.text(o, "plus", lx + 36 + 5 * STEP + 6, ly + 4, 9.5, DIM)
    return o


if __name__ == "__main__":
    days, total = parse(fetch(USER))
    if not os.path.isdir("assets"):
        os.makedirs("assets")
    S.write(OUT, build(days, total))
    print("%d jours, %d contributions" % (len(days), total))
