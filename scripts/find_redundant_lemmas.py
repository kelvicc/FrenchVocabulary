# -*- coding: utf-8 -*-
import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTIONS_DIR = os.path.join(BASE_DIR, 'sections')

for i in range(1, 23):
    fpath = os.path.join(SECTIONS_DIR, f'section_{i:02d}.md')
    txt = open(fpath, encoding='utf-8').read()
    blocks = txt.split('### No.')
    for b in blocks[1:]:
        lines = b.strip().splitlines()
        s_num = lines[0].split()[0]
        s_text = lines[1] if len(lines) > 1 else ''
        lemmas = re.findall(r'-\s+\*\*(\d+)\s*\|\s*([^*]+?)\*\*', b)
        for num1, l1 in lemmas:
            c1 = l1.strip().lower()
            for num2, l2 in lemmas:
                if num1 == num2:
                    continue
                c2 = l2.strip().lower()
                c1_core = re.sub(r"^(le|la|l'|les|un|une|des)\s+", '', c1)
                c2_core = re.sub(r"^(le|la|l'|les|un|une|des)\s+", '', c2)
                if len(c2_core) > 3 and c2_core in c1_core and c1_core != c2_core:
                    print(f'Sec {i:02d} No.{s_num}: #{num1} "{l1}" contains #{num2} "{l2}"')
