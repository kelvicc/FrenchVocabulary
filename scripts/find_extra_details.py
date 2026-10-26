# -*- coding: utf-8 -*-
from run_full_audit import parse_verified_section, parse_french_section
from duo_official_ranges import DUO_OFFICIAL_RANGES

# Let's inspect Section 02, 08, 15, 16, 17, 20 in detail
# to identify the EXACT sentences that were extra / split / original!

def inspect_extra(sec):
    v_segs = parse_verified_section(sec)
    fr_sents = parse_french_section(sec)
    start_no, end_no, off_cnt = DUO_OFFICIAL_RANGES[sec]

    print(f"\n=======================================================")
    print(f"SECTION {sec:02d}: Official={off_cnt} ({start_no}-{end_no}) | French={len(fr_sents)}")
    print(f"=======================================================")
    print("--- Official Audio Segments ---")
    for i, s in enumerate(v_segs, 1):
        print(f"  A{i:02d}: {s['text']}")
    print("--- French Items ---")
    for item in fr_sents:
        print(f"  FR No.{item['num']}: {item['ja']}")
        print(f"       FR text: {item['fr'][:70]}...")

for s in [2, 8, 15, 16, 17, 20]:
    inspect_extra(s)
