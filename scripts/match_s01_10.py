# -*- coding: utf-8 -*-
from run_full_audit import parse_verified_section, parse_french_section

# Collect all French items in Sec 1 to 10 with their keywords
fr_items = []
for s in range(1, 11):
    for it in parse_french_section(s):
        fr_items.append({
            'sec': s,
            'num': it['num'],
            'ja': it['ja'],
            'fr': it['fr'],
            'body': it['body']
        })

print(f"Total French items in Sec 1-10: {len(fr_items)}")

for s in range(1, 11):
    v_segs = parse_verified_section(s)
    print(f"\n=================== Audio Sec {s:02d} ({len(v_segs)} segments) ===================")
    for i, seg in enumerate(v_segs, 1):
        txt = seg['text']
        # search across all fr_items
        matches = []
        for it in fr_items:
            # simple check: if any distinctive word in text matches in it['body'] or it['fr']
            pass
        print(f"[{i:02d}] {txt}")
