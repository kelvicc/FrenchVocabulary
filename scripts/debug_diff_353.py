# -*- coding: utf-8 -*-
import os
import re
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

duo_original = [
    (1, 1, 9),      # 9 sents
    (2, 10, 21),    # 12 sents
    (3, 22, 35),    # 14 sents
    (4, 36, 45),    # 10 sents
    (5, 46, 62),    # 17 sents
    (6, 63, 75),    # 13 sents
    (7, 76, 91),    # 16 sents
    (8, 92, 100),   # 9 sents
    (9, 101, 113),  # 13 sents
    (10, 114, 125), # 12 sents
    (11, 126, 136), # 11 sents
    (12, 137, 145), # 9 sents
    (13, 146, 155), # 10 sents
    (14, 156, 165), # 10 sents
    (15, 166, 176), # 11 sents
    (16, 177, 185), # 9 sents
    (17, 186, 197), # 12 sents
    (18, 198, 211), # 14 sents
    (19, 212, 223), # 12 sents
    (20, 224, 240), # 17 sents
    (21, 241, 255), # 15 sents
    (22, 256, 272), # 17 sents
    (23, 273, 281), # 9 sents
    (24, 282, 293), # 12 sents
    (25, 294, 303), # 10 sents
    (26, 304, 313), # 10 sents
    (27, 314, 328), # 15 sents
    (28, 329, 341), # 13 sents
    (29, 342, 353), # 12 sents
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
SECTIONS_DIR = os.path.join(BASE_DIR, "sections")

print(f"{'Sec':<4} | {'Duo 3.0 Range':<15} | {'Duo Orig':<10} | {'FR Range':<15} | {'FR Cnt':<8} | {'Diff':<6}")
print("-" * 75)

total_orig = 0
total_fr = 0

for sec, start_o, end_o in duo_original:
    cnt_o = end_o - start_o + 1
    total_orig += cnt_o

    fr_file = os.path.join(SECTIONS_DIR, f"section_{sec:02d}.md")
    fr_text = open(fr_file, encoding="utf-8").read()
    fr_sents = re.findall(r"^###\s+No\.\s*(\d+)", fr_text, re.MULTILINE)
    cnt_fr = len(fr_sents)
    total_fr += cnt_fr

    start_fr = int(fr_sents[0]) if fr_sents else 0
    end_fr = int(fr_sents[-1]) if fr_sents else 0
    diff = cnt_fr - cnt_o

    print(f"Sec {sec:02d} | No.{start_o:03d} - No.{end_o:03d} | {cnt_o:2d} sents  | No.{start_fr:03d} - No.{end_fr:03d} | {cnt_fr:2d} sents | {diff:+2d}")

print("=" * 75)
print(f"TOTAL (Sec 01-29): Duo 3.0 = {total_orig} sents (ends at #353)")
print(f"TOTAL (Sec 01-29): FR total = {total_fr} sents (labeled No.001 - No.{end_fr})")
