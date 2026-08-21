# -*- coding: utf-8 -*-
"""Genere les panneaux statiques du README dans assets/.

Tous les panneaux partagent le meme cadre et le meme entete de section, pour que
le README se lise comme une seule page et non comme un empilement de widgets.
Aucun n'est anime : GitHub bloque les animations dans les images distantes.
"""
import os, sys
from xml.sax.saxutils import escape
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import style as S
from style import PINK, SOFT, WHITE, BODY, DIM, CARD, CHIP, W, PAD, TITLE_H
from icons import path as icon

OUT = "assets"
STR = "#FFC2DE"


# ---------------------------------------------------------------- a propos
def build_about():
    LINES = [
        [("const ", PINK), ("pinkkaguy", WHITE), (" = {", DIM)],
        [("  role", SOFT), (": ", DIM), (u'"Développeur — web & mobile"', STR), (",", DIM)],
        [("  stack", SOFT), (": ", DIM), (u'["TypeScript", "Next.js", "React Native", "NestJS"]', STR), (",", DIM)],
        [("  builds", SOFT), (": ", DIM), (u'["apps web & mobile", "backends", "extensions Chrome"]', STR), (",", DIM)],
        [("  bots", SOFT), (": ", DIM), (u'["Discord"]', STR), (",", DIM)],
        [("  ia", SOFT), (": ", DIM), (u'"Gemini dans mes produits, Claude Code dans mon workflow"', STR), (",", DIM)],
        [("};", DIM)],
    ]
    LH, TOP = 22, TITLE_H + 34
    h = TOP + len(LINES) * LH + PAD + 6
    o = S.open_svg(h)
    S.frame(o, h)
    S.section_title(o, u"À propos")

    y0 = TITLE_H - 4
    o.append('<rect x="%d" y="%d" width="%d" height="28" rx="8" fill="#180b14"/>'
             % (PAD, y0, W - PAD * 2))
    for i, op in enumerate((1.0, 0.6, 0.32)):
        o.append('<circle cx="%d" cy="%d" r="4.5" fill="%s" fill-opacity="%.2f"/>'
                 % (PAD + 16 + i * 16, y0 + 14, PINK, op))
    S.text(o, "pinkkaguy.ts", PAD + 74, y0 + 18, 11, DIM)

    for i, parts in enumerate(LINES):
        S.rich(o, parts, PAD + 12, TOP + i * LH + 14, 13, "500")
    S.write(os.path.join(OUT, "about.svg"), o)


# ---------------------------------------------------------------- l'IA
def build_ai():
    COLS = [
        (u"Dans mes produits",
         u"J'intègre des modèles (Gemini, Claude). scandocs-ia classe automatiquement "
         u"des documents scannés ; geo-aeo mesure la visibilité d'une marque dans les "
         u"réponses des IA."),
        (u"Dans ma façon de construire",
         u"Je développe avec des outils comme Claude Code. Je conçois l'architecture, "
         u"j'oriente, je relis et je livre. L'IA accélère mon travail ; les décisions "
         u"techniques et la responsabilité du résultat restent les miennes."),
    ]
    QUOTE = u"Utiliser ces outils correctement, c'est une compétence — pas un raccourci."

    GAP, SIZE, LH = 22, 12, 19
    cw = (W - PAD * 2 - GAP) / 2.0
    wrapped = [S.wrap(body, S.chars_for(cw - 36, SIZE)) for _, body in COLS]
    col_h = 52 + max(len(l) for l in wrapped) * LH

    top, qh = TITLE_H, 46
    h = top + col_h + 18 + qh + PAD
    o = S.open_svg(h)
    S.frame(o, h)
    S.section_title(o, u"L'IA dans mon travail, c'est assumé")

    for i, (title, _) in enumerate(COLS):
        x = PAD + i * (cw + GAP)
        o.append('<rect x="%.1f" y="%d" width="%.1f" height="%.1f" rx="11" fill="%s" '
                 'stroke="%s" stroke-opacity="0.28"/>' % (x, top, cw, col_h, CARD, PINK))
        o.append('<rect x="%.1f" y="%d" width="3" height="%.1f" rx="1.5" fill="%s"/>'
                 % (x, top, col_h, PINK))
        S.text(o, title, x + 18, top + 30, 13, PINK, "700")
        for j, line in enumerate(wrapped[i]):
            S.text(o, line, x + 18, top + 56 + j * LH, SIZE, BODY)

    qy = top + col_h + 18
    o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="11" fill="#170b13" '
             'stroke="%s" stroke-opacity="0.22"/>' % (PAD, qy, W - PAD * 2, qh, PINK))
    S.text(o, u"“", PAD + 16, qy + 34, 24, PINK, "700")
    S.text(o, QUOTE, PAD + 42, qy + 28, 12.5, SOFT, "600")
    S.write(os.path.join(OUT, "ai.svg"), o)


# ---------------------------------------------------------------- stack
def build_stack():
    GROUPS = [
        (u"Langages", [("TypeScript", "typescript"), ("JavaScript", "javascript"),
                       ("HTML5", "html5"), ("CSS3", "css3")]),
        (u"Frontend", [("Next.js", "nextdotjs"), ("React", "react"), ("React Native", "react"),
                       ("Expo", "expo"), ("Tailwind", "tailwindcss"), ("Framer Motion", "framer")]),
        (u"Backend & outils", [("Node.js", "nodedotjs"), ("NestJS", "nestjs"), ("Turborepo", "turborepo"),
                               ("Vercel", "vercel"), ("Gemini", "googlegemini"), ("Git", "git")]),
    ]
    PH, GAP, ROWGAP, GROUPGAP = 34, 10, 10, 24
    SIZE, PADX, ICON, IGAP = 13, 14, 17, 9

    def pw(label):
        return PADX * 2 + ICON + IGAP + len(label) * SIZE * S.CHW

    plan, y = [], TITLE_H + 2
    for gtitle, items in GROUPS:
        plan.append(("g", gtitle, y))
        y += 24
        rows, row, rw = [], [], 0.0
        for label, slug in items:
            w = pw(label)
            if row and rw + GAP + w > W - PAD * 2:
                rows.append((row, rw))
                row, rw = [], 0.0
            rw += (GAP if row else 0) + w
            row.append((label, slug, w))
        if row:
            rows.append((row, rw))
        for row, rw in rows:
            x = (W - rw) / 2.0
            for label, slug, w in row:
                plan.append(("p", (label, slug, x, y), 0))
                x += w + GAP
            y += PH + ROWGAP
        y += GROUPGAP - ROWGAP

    h = y - (GROUPGAP - ROWGAP) - ROWGAP + PAD
    o = S.open_svg(h)
    S.frame(o, h)
    S.section_title(o, u"Ma stack")
    for kind, data, yy in plan:
        if kind == "g":
            o.append('<text x="%.1f" y="%d" fill="%s" font-family="%s" font-size="10.5" '
                     'font-weight="700" letter-spacing="2.2" text-anchor="middle">%s</text>'
                     % (W / 2.0, yy + 8, PINK, S.FONT, escape(data.upper())))
        else:
            label, slug, x, py = data
            S.pill(o, x, py, label, icon(slug), PH, SIZE, PADX, ICON, IGAP)
    S.write(os.path.join(OUT, "stack.svg"), o)


# ---------------------------------------------------------------- projets
def build_projects():
    PROJECTS = [
        ("olivae", u"Landing page premium pour un restaurant méditerranéen à Dubaï.",
         [("Next.js", "nextdotjs"), ("TypeScript", "typescript")]),
        ("pinkkblock", u"Extension Chrome MV3 : bloque pubs, popups et détecteurs d'adblock.",
         [("JavaScript", "javascript"), ("Chrome", "googlechrome")]),
        ("pratice-design", u"Showcase design : typographie, layouts et animations CSS.",
         [("CSS3", "css3"), ("HTML5", "html5")]),
    ]
    NOTE = (u"Plusieurs autres projets sont en cours en privé : une marketplace de formations "
            u"(Turborepo + NestJS + Next.js), un outil de visibilité de marque dans les moteurs IA, "
            u"une app mobile de scan de documents (React Native + Gemini).")

    GAP, CARD_H = 12, 176
    cw = (W - PAD * 2 - GAP * 2) / 3.0
    top = TITLE_H

    nl = S.wrap(NOTE, S.chars_for(W - PAD * 2 - 46, 12))
    nh = 24 + len(nl) * 18
    h = top + CARD_H + 16 + nh + PAD
    o = S.open_svg(h)
    S.frame(o, h)
    S.section_title(o, u"Projets publics")

    for i, (name, desc, techs) in enumerate(PROJECTS):
        x = PAD + i * (cw + GAP)
        o.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" rx="12" fill="%s" '
                 'stroke="%s" stroke-opacity="0.4"/>' % (x, top, cw, CARD_H, CARD, PINK))
        o.append('<rect x="%.1f" y="%d" width="%.1f" height="3" rx="1.5" fill="%s"/>'
                 % (x, top, cw, PINK))
        S.text(o, name, x + 18, top + 38, 15, PINK, "700")
        for j, line in enumerate(S.wrap(desc, S.chars_for(cw - 36, 11))[:3]):
            S.text(o, line, x + 18, top + 64 + j * 17, 11, BODY)
        tx = x + 18
        for label, slug in techs:
            tx += S.pill(o, tx, top + CARD_H - 42, label, icon(slug), 24, 10, 8, 12, 6, CHIP, 0.3) + 7

    ny = top + CARD_H + 16
    o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="11" fill="#170b13" '
             'stroke="%s" stroke-opacity="0.22"/>' % (PAD, ny, W - PAD * 2, nh, PINK))
    o.append('<rect x="%d" y="%d" width="3" height="%d" rx="1.5" fill="%s"/>' % (PAD, ny, nh, PINK))
    for j, line in enumerate(nl):
        S.text(o, line, PAD + 20, ny + 28 + j * 18, 12, BODY)
    S.write(os.path.join(OUT, "projects.svg"), o)


# ---------------------------------------------------------------- pied de page
def build_footer():
    h = 94
    o = S.open_svg(h)
    S.frame(o, h)
    o.append('<rect x="0.5" y="0.5" width="%.1f" height="3" rx="1.5" fill="%s"/>' % (W - 1, PINK))
    S.text(o, "PINKKAGUY", W / 2.0, 44, 17, PINK, "700", "middle")
    S.text(o, u"Visuels générés sur mesure et hébergés dans ce dépôt — voir assets/",
           W / 2.0, 68, 11, DIM, "400", "middle")
    S.write(os.path.join(OUT, "footer.svg"), o)


if __name__ == "__main__":
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    print("panneaux generes :")
    build_about()
    build_ai()
    build_stack()
    build_projects()
    build_footer()
