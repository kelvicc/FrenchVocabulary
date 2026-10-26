# -*- coding: utf-8 -*-
from duo_official_ranges import DUO_OFFICIAL_RANGES
from run_full_audit import parse_verified_section, parse_french_section

# Let's inspect every section from 1 to 29 and check:
# 1. Official sentence count
# 2. French sentence count
# 3. Difference (French - Official)

total_off = 0
total_fr = 0

print(f"{'SEC':<5} | {'Official':<8} | {'French':<8} | {'Diff':<6}")
print("-" * 35)

for s in range(1, 30):
    start, end, off_cnt = DUO_OFFICIAL_RANGES[s]
    fr_sents = parse_french_section(s)
    fr_cnt = len(fr_sents)
    diff = fr_cnt - off_cnt
    total_off += off_cnt
    total_fr += fr_cnt
    print(f"Sec {s:02d} | {off_cnt:<8} | {fr_cnt:<8} | {diff:+d}")

print("-" * 35)
print(f"TOTAL | {total_off:<8} | {total_fr:<8} | {total_fr - total_off:+d}")
