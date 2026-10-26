# -*- coding: utf-8 -*-
from run_full_audit import parse_verified_section, parse_french_section

for s in [8, 9]:
    v_segs = parse_verified_section(s)
    fr_sents = parse_french_section(s)
    print(f"\n================ SEC {s:02d} ================")
    print(f"AUDIO ({len(v_segs)}):")
    for i, seg in enumerate(v_segs, 1):
        print(f"  [{i:02d}] {seg['text']}")
    print(f"FR ({len(fr_sents)}):")
    for it in fr_sents:
        print(f"  [{it['num']}] {it['ja']}")
