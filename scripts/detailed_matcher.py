# -*- coding: utf-8 -*-
import os
import re

# Let's inspect sections 11 to 29 in detail to find missing sentences precisely
from run_full_audit import parse_verified_section, parse_french_section

# For each section, let's print out the exact sentences in Audio that are NOT in French edition
def find_missing_in_section(sec):
    v_segs = parse_verified_section(sec)
    fr_sents = parse_french_section(sec)
    
    # We will print all audio segments and French sentences side by side
    print(f"\n=======================================================")
    print(f"SECTION {sec:02d}: Audio={len(v_segs)} segments, FR={len(fr_sents)} sentences")
    print(f"=======================================================")
    for i, s in enumerate(v_segs, 1):
        print(f"AUDIO [{i:02d}] {s['text']}")
    print("-------------------------------------------------------")
    for item in fr_sents:
        print(f"FR [{item['num']}] {item['ja']}")

if __name__ == '__main__':
    for sec in [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]:
        find_missing_in_section(sec)
