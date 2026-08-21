# -*- coding: utf-8 -*-
"""Primitives de style partagees par tous les panneaux du README."""
from xml.sax.saxutils import escape as X

PINK   = "#FF1F8F"
SOFT   = "#FF9ACB"
WHITE  = "#F3E9EF"
BODY   = "#B9AEB6"
DIM    = "#8A7E86"
BG     = "#0f0810"
CARD   = "#12080f"
CHIP   = "#1c0c16"
FONT   = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

W       = 880          # largeur commune de tous les panneaux
PAD     = 24           # marge interieure
TITLE_H = 52           # hauteur reservee a l'entete de section
CHW     = 0.601        # largeur d'un caractere, en fraction de la taille de police


def open_svg(h, w=W):
    return ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 %d %d" fill="none">' % (w, h, w, h)]


def frame(o, h, w=W):
    """Cadre du panneau : fond sombre, bord rose translucide."""
    o.append('<rect x="0.5" y="0.5" width="%.1f" height="%.1f" rx="14" fill="%s" '
             'stroke="%s" stroke-opacity="0.4"/>' % (w - 1, h - 1, BG, PINK))


def section_title(o, label, x=PAD, y=30):
    """Puce ronde + intitule de section en petites capitales espacees."""
    o.append('<circle cx="%d" cy="%d" r="4" fill="%s"/>' % (x + 4, y - 4, PINK))
    o.append('<text x="%d" y="%d" fill="%s" font-family="%s" font-size="12" '
             'font-weight="700" letter-spacing="2.6">%s</text>'
             % (x + 17, y, PINK, FONT, X(label.upper())))


def text(o, s, x, y, size=12, fill=BODY, weight="400", anchor="start", opacity=None):
    op = '' if opacity is None else ' fill-opacity="%.2f"' % opacity
    o.append('<text x="%.1f" y="%.1f" fill="%s" font-family="%s" font-size="%d" '
             'font-weight="%s" text-anchor="%s"%s>%s</text>'
             % (x, y, fill, FONT, size, weight, anchor, op, X(s)))


def rich(o, parts, x, y, size=12, weight="400"):
    """Une ligne composee de morceaux (texte, couleur)."""
    o.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="%d" font-weight="%s" '
             'xml:space="preserve">%s</text>'
             % (x, y, FONT, size, weight,
                "".join('<tspan fill="%s">%s</tspan>' % (c, X(t)) for t, c in parts)))


def wrap(s, width):
    """Retour a la ligne sur les espaces, sans couper les mots."""
    words, lines, cur = s.split(), [], ""
    for wd in words:
        cand = wd if not cur else cur + " " + wd
        if len(cand) > width and cur:
            lines.append(cur); cur = wd
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def chars_for(px, size):
    """Combien de caracteres tiennent dans px a cette taille de police."""
    return max(8, int(px / (size * CHW)))


def pill(o, x, y, label, icon_path=None, h=34, size=13, pad=14, icon=17, gap=9,
         fill=CARD, stroke_opacity=0.38):
    """Etiquette arrondie, avec logo optionnel. Retourne sa largeur."""
    w = pad * 2 + len(label) * size * CHW + ((icon + gap) if icon_path else 0)
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="9" fill="%s" '
             'stroke="%s" stroke-opacity="%.2f"/>' % (x, y, w, h, fill, PINK, stroke_opacity))
    tx = x + pad
    if icon_path:
        o.append('<g transform="translate(%.1f,%.1f) scale(%.4f)"><path d="%s" fill="%s" '
                 'fill-opacity="0.92"/></g>'
                 % (tx, y + (h - icon) / 2.0, icon / 24.0, icon_path, SOFT))
        tx += icon + gap
    o.append('<text x="%.1f" y="%.1f" fill="%s" font-family="%s" font-size="%d" '
             'font-weight="600" dominant-baseline="middle">%s</text>'
             % (tx, y + h / 2.0 + 1, WHITE, FONT, size, X(label)))
    return w


def write(path, lines):
    import io
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines + ['</svg>']))
    print("  %s" % path)
