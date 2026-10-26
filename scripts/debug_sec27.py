# -*- coding: utf-8 -*-
with open('duo_francais/Duo3.0 original/transcripts/27 Section 27.txt', 'r', encoding='utf-8') as f:
    t_text = f.read()

with open('duo_francais/sections/section_27.md', 'r', encoding='utf-8') as f:
    s_text = f.read()

import re
pattern = r'### No\.\s*(\d+)[^\n]*\n>\s*(.*?)\n(.*?)(?=(?:### No\.|\Z))'
matches = re.findall(pattern, s_text, re.DOTALL)

print("=== Section 27 Full Comparison ===")
print("Transcript:")
print(t_text)

print("\nFrench section sentences:")
for num, fr, body in matches:
    note_m = re.search(r'>\s*\[!NOTE\]\s*(.*?)(?=\n-|\n&|\n□|\n<|\Z)', body, re.DOTALL)
    ja = note_m.group(1).strip().splitlines()[0] if note_m else ""
    print(f"No. {num}: {fr}")
    print(f"    JA: {ja}")
