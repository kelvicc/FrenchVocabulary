# -*- coding: utf-8 -*-
from run_full_audit import parse_verified_section, parse_french_section

for s in [20, 21, 22, 23]:
    v_segs = parse_verified_section(s)
    fr_sents = parse_french_section(s)
    print(f"\n*** SEC {s:02d} ***")
    for i, seg in enumerate(v_segs, 1):
        print(f"  AUDIO {i:02d}: {seg['text']}")
    for item in fr_sents:
        print(f"  FR {item['num']}: {item['ja']}")
