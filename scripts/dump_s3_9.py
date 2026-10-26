# -*- coding: utf-8 -*-
from run_full_audit import parse_verified_section, parse_french_section

# Let's inspect Audio sentences in Sec 3 to 9 that don't match any French sentence
for sec in range(3, 10):
    v_segs = parse_verified_section(sec)
    print(f"\n=== SEC {sec:02d} AUDIO ({len(v_segs)}) ===")
    for i, s in enumerate(v_segs, 1):
        print(f"[{i:02d}] {s['text']}")
