# -*- coding: utf-8 -*-
import os
import re
from duo_official_ranges import DUO_OFFICIAL_RANGES
from parse_helpers import get_verified_sentences, get_french_sentences

def inspect_section_alignment(sec_num):
    start_no, end_no, official_count = DUO_OFFICIAL_RANGES[sec_num]
    verified = get_verified_sentences(sec_num)
    french = get_french_sentences(sec_num)
    
    print(f"\n=================================================================")
    print(f"SECTION {sec_num:02d} (Official No.{start_no:03d} - No.{end_no:03d}, Expected: {official_count} sentences)")
    print(f"Verified segments: {len(verified)} | French sentences: {len(french)}")
    print(f"=================================================================")
    print("--- Verified Audio Lines ---")
    for i, line in enumerate(verified, 1):
        print(f"  [{i:02d}] {line}")
    print("\n--- Current French Sentences ---")
    for item in french:
        print(f"  [FR No.{item['num']}] {item['ja']}")

if __name__ == '__main__':
    for s in [13, 14, 19, 24, 27]:
        inspect_section_alignment(s)
