# -*- coding: utf-8 -*-
import sys
import os
import re
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTIONS_DIR = os.path.join(BASE_DIR, 'sections')

# Load all lemmas from Section 01 to Section 22
sec1_22_lemmas = set()
for i in range(1, 23):
    fpath = os.path.join(SECTIONS_DIR, f'section_{i:02d}.md')
    txt = open(fpath, encoding='utf-8').read()
    for m in re.finditer(r'-\s+\*\*(\d+)\s*\|\s*([^*]+?)\*\*', txt):
        w = m.group(2).strip().replace('...', '').lower()
        sec1_22_lemmas.add(w)

sec23_candidates = [
    # 265
    "le cadavre", "le crime", "sanglant(e)",
    # 266
    "le mobile", "le meurtre", "assassiner",
    # 267
    "le commissaire", "une enquête", "discrètement",
    # 268
    "une empreinte", "un indice", "la piste",
    # 269
    "un cambrioleur", "s'introduire", "une effraction",
    # 270
    "un bijou", "le butin", "le complice",
    # 271
    "une agression", "la plainte", "le témoin", "identifier",
    # 272
    "le suspect / la suspecte", "interroger", "le délit", "un alibi",
    # 273
    "une arrestation", "le policier / la policière", "les menottes", "la fuite",
    # 274
    "le voleur / la voleuse", "le commissariat", "détenir",
    # 275
    "un enlèvement", "le ravisseur / la ravisseuse", "audacieux(-euse)", "un héritier / une héritière",
    # 276
    "séquestrer", "un otage", "la rançon",
    # 277
    "la corruption", "le scandale", "le pot-de-vin", "dénoncer",
    # 278
    "détourner", "blanchir",
    # 279
    "coupable", "une escroquerie", "un épargnant / une épargnante",
    # 280
    "un faussaire / une faussaire", "falsifier", "contrefaire",
    # 281
    "le gendarme / la gendarme", "la patrouille", "traquer", "le trafic", "la drogue",
    # 282
    "cerner", "le fugitif / la fugitive", "catégoriquement", "une arme",
    # 283
    "le revolver", "tirer", "la balle", "grièvement",
    # 284
    "méfiant(e)", "le pickpocket", "commettre", "le vol",
    # 285
    "la foule", "fouiller", "la poche",
    # 286
    "la cavale", "le malfaiteur / la malfaitrice", "neutraliser", "éradiquer", "la criminalité"
]

print(f"Total candidates in Section 23: {len(sec23_candidates)}")
counts = Counter(sec23_candidates)
if len(counts) != len(sec23_candidates):
    print("Internal duplicates in candidates:")
    for w, c in counts.items():
        if c > 1:
            print(f"  {w} ({c} times)")
else:
    print("Zero internal duplicates in candidates!")

collisions = []
for c in sec23_candidates:
    clean = c.lower().strip()
    if clean in sec1_22_lemmas:
        collisions.append(c)
    # Check core word without article
    core = re.sub(r"^(le|la|l'|les|un|une|des)\s+", "", clean)
    for existing in sec1_22_lemmas:
        ex_core = re.sub(r"^(le|la|l'|les|un|une|des)\s+", "", existing)
        if core == ex_core and clean != existing:
            collisions.append(f"{c} (matches core of {existing})")

if collisions:
    print("Collisions with Section 01-22:")
    for col in collisions:
        print(f"  ⚠️ {col}")
else:
    print("🎉 100% UNIQUE! Zero collisions with Section 01-22!")
