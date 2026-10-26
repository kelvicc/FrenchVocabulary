# -*- coding: utf-8 -*-
import os
import re

from run_full_audit import parse_verified_section, parse_french_section
from duo_official_ranges import DUO_OFFICIAL_RANGES

def detailed_section_audit(sec):
    v_segs = parse_verified_section(sec)
    fr_sents = parse_french_section(sec)
    start_no, end_no, count = DUO_OFFICIAL_RANGES[sec]

    print(f"\n=======================================================")
    print(f"SECTION {sec:02d}: Official No.{start_no:03d}-No.{end_no:03d} ({count} sentences)")
    print(f"Audio lines: {len(v_segs)} | French items: {len(fr_sents)}")
    print(f"=======================================================")

    for i, s in enumerate(v_segs, 1):
        txt = s['text']
        # search if text or key concept is in any fr_sents
        found = False
        match_info = ""
        for item in fr_sents:
            # simple keyword check
            # We check both JA translation and English in body (like (= ...))
            pass

for s in [13, 14, 15, 16, 17, 18, 19, 20, 24, 27]:
    v_segs = parse_verified_section(s)
    fr_sents = parse_french_section(s)
    print(f"\n*** SEC {s:02d} ***")
    for i, seg in enumerate(v_segs, 1):
        print(f"  AUDIO {i:02d}: {seg['text']}")
    for item in fr_sents:
        print(f"  FR {item['num']}: {item['ja']}")
