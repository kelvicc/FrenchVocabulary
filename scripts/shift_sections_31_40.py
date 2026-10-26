# -*- coding: utf-8 -*-
"""
Shift Section 31 to Section 40 by +110.
Maps No. 391–520 to No. 501–630 to make room for Sections 26–30 expansion.
"""
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
SECTIONS_DIR = os.path.join(BASE_DIR, "sections")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")

OFFSET = 110

# 1. Shift audio files (reverse order to avoid collisions)
print("1. Renaming MP3 files in audio/...")
for n in range(520, 390, -1):
    src = os.path.join(AUDIO_DIR, f"sentence_{n:03d}.mp3")
    dst = os.path.join(AUDIO_DIR, f"sentence_{n + OFFSET:03d}.mp3")
    if os.path.exists(src):
        if os.path.exists(dst):
            os.remove(dst)
        os.rename(src, dst)
print(f"Shifted audio files from 391..520 to {391+OFFSET}..{520+OFFSET}")

# 2. Shift Markdown files for sections 31..40
print("2. Shifting Markdown files sections/section_31.md .. section_40.md...")
for sec in range(31, 41):
    fpath = os.path.join(SECTIONS_DIR, f"section_{sec}.md")
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    def shift_header(m):
        start_n = int(m.group(1)) + OFFSET
        end_n = int(m.group(2)) + OFFSET
        return f"(No. {start_n:03d} – No. {end_n:03d})"

    content = re.sub(r"\(No\.\s*(\d+)\s*[–-]\s*No\.\s*(\d+)\)", shift_header, content)

    def shift_no(m):
        n = int(m.group(1)) + OFFSET
        return f"### No. {n:03d}"

    content = re.sub(r"###\s+No\.\s*(\d+)", shift_no, content)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Shifted section_{sec}.md by +{OFFSET}")

print("Done shifting Sections 31-40.")
