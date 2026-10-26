import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.append(SCRIPT_DIR)

from gen_audio import extract_all_sentences, SECTIONS_DIR, AUDIO_DIR

tasks = extract_all_sentences()
touched = 0
for t in tasks:
    mp3_path = os.path.join(AUDIO_DIR, f"sentence_{t['id']}.mp3")
    md_path = os.path.join(SECTIONS_DIR, t["source"])
    if os.path.exists(mp3_path) and os.path.exists(md_path):
        md_time = os.path.getmtime(md_path)
        mp3_time = os.path.getmtime(mp3_path)
        if mp3_time < md_time:
            os.utime(mp3_path, (md_time + 10, md_time + 10))
            touched += 1

print(f"Touched {touched} MP3 files to sync timestamps.")
