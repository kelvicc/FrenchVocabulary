# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

txt = open('sections/section_23.md', encoding='utf-8').read()
blocks = txt.split('### No.')

for i, b in enumerate(blocks[1:], 265):
    lines = b.strip().splitlines()
    s_orig = lines[0]
    s_fr = lines[1] if len(lines) > 1 else ''
    m = re.search(r'> \*\*«\s*(.*?)\s*»\*\*', s_fr)
    sentence_text = m.group(1) if m else s_fr
    words = sentence_text.split()
    print(f"No. {i:03d} (was {s_orig.split()[0]}): {len(words)} words | Speaker: {s_orig}")
    print(f"   {sentence_text}")
