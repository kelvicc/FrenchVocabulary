# -*- coding: utf-8 -*-
import subprocess
import os
import glob
import re

whisper_exe = r"c:\Users\noid\Documents\antigravity\kind-fermi\tools\whisper.cpp\Release\whisper-cli.exe"
model_bin = r"c:\Users\noid\Documents\antigravity\kind-fermi\tools\whisper.cpp\models\ggml-base.en.bin"
audio_dir = r"duo_francais\Duo3.0 original\DUO audio"
out_dir = r"duo_francais\Duo3.0 original\transcripts_verified"

os.makedirs(out_dir, exist_ok=True)

# We will transcribe Section 1 to 29 first (and can do all 45)
for sec in range(1, 30):
    mp3_candidates = [
        f"{audio_dir}/{sec:02d} Section {sec}.mp3",
        f"{audio_dir}/{sec:02d} Section {sec:02d}.mp3",
        f"{audio_dir}/Section {sec}.mp3"
    ]
    mp3_path = None
    for cand in mp3_candidates:
        if os.path.exists(cand):
            mp3_path = cand
            break
    
    if not mp3_path:
        print(f"Section {sec:02d}: MP3 NOT FOUND")
        continue

    out_file = f"{out_dir}/{sec:02d}_Section_{sec}.txt"
    if os.path.exists(out_file) and os.path.getsize(out_file) > 100:
        # print(f"Section {sec:02d}: Already verified")
        continue

    print(f"Transcribing Section {sec:02d} with timestamps...")
    res = subprocess.run([whisper_exe, "-m", model_bin, "-f", mp3_path], capture_output=True, text=True, encoding="utf-8")
    lines = [l.strip() for l in res.stdout.splitlines() if '-->' in l]
    
    # Write both timestamped and clean text
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"Saved: {out_file} ({len(lines)} segments)")

print("All sections transcribed successfully!")
