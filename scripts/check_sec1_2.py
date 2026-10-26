# -*- coding: utf-8 -*-
import re

def show_section(sec_num):
    with open(f'duo_francais/sections/section_{sec_num:02d}.md', 'r', encoding='utf-8') as f:
        text = f.read()
    matches = re.findall(r'### No\.\s*(\d+)[^\n]*\n>\s*(.*?)\n(.*?)(?=(?:### No\.|\Z))', text, re.DOTALL)
    print(f"=== SECTION {sec_num:02d} ({len(matches)} sentences) ===")
    for num, fr, body in matches:
        note_m = re.search(r'>\s*\[!NOTE\]\s*(.*?)(?=\n-|\n&|\n□|\n<|\Z)', body, re.DOTALL)
        ja = note_m.group(1).strip().splitlines()[0] if note_m else ""
        print(f"No. {num}: {ja}")

show_section(1)
show_section(2)
