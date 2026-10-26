# -*- coding: utf-8 -*-
import glob
import os
import re
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
ORIG_DIR = os.path.join(BASE_DIR, "Duo3.0 original", "transcripts")
SECTIONS_DIR = os.path.join(BASE_DIR, "sections")

print("=" * 70)
print("DUO 3.0 ORIGINAL VS DUO FRANCAIS SENTENCE COVERAGE AUDIT")
print("=" * 70)

total_orig = 0
total_fr = 0

for sec in range(1, 46):
    f_list = glob.glob(os.path.join(ORIG_DIR, f"{sec:02d} Section *.txt"))
    if not f_list:
        f_list = glob.glob(os.path.join(ORIG_DIR, f"{sec} Section *.txt"))

    orig_text = ""
    if f_list:
        with open(f_list[0], "r", encoding="utf-8") as f:
            orig_text = f.read().strip()

    # Clean header e.g. "Section 1. "
    orig_clean = re.sub(r"^(?:Section\s+\d+[\.\s]*)", "", orig_text)

    fr_file = os.path.join(SECTIONS_DIR, f"section_{sec:02d}.md")
    fr_cnt = 0
    fr_nums = []
    if os.path.exists(fr_file):
        with open(fr_file, "r", encoding="utf-8") as f:
            content = f.read()
        fr_nums = re.findall(r"^###\s+No\.\s*(\d+)", content, re.MULTILINE)
        fr_cnt = len(fr_nums)

    total_fr += fr_cnt
    range_str = f"No.{fr_nums[0]}-No.{fr_nums[-1]}" if fr_nums else "NOT CREATED"
    print(f"Sec {sec:02d}: Orig text len={len(orig_clean):4d} chars | FR count={fr_cnt:2d} ({range_str})")

print("=" * 70)
print(f"Total French Sentences Created: {total_fr} (in Sections 01-29)")
print("=" * 70)
