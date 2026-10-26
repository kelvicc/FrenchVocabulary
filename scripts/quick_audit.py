# -*- coding: utf-8 -*-
import glob
import os
import subprocess
import re

whisper_exe = r"c:\Users\noid\Documents\antigravity\kind-fermi\tools\whisper.cpp\Release\whisper-cli.exe"
model_bin = r"c:\Users\noid\Documents\antigravity\kind-fermi\tools\whisper.cpp\models\ggml-base.en.bin"
audio_dir = r"duo_francais/Duo3.0 original/DUO audio"
trans_dir = r"duo_francais/Duo3.0 original/transcripts"

print("Auditing whisper transcript drops for Section 1 to 29...")

for sec in [2, 13, 24, 27]:
    p = f"{audio_dir}/{sec:02d} Section {sec}.mp3"
    t_file = f"{trans_dir}/{sec:02d} Section {sec}.txt"
    if not os.path.exists(t_file):
        t_file = f"{trans_dir}/{sec} Section {sec}.txt"
    
    with open(t_file, 'r', encoding='utf-8') as f:
        old_txt = f.read().strip()
    
    # Run whisper with timestamps
    res = subprocess.run([whisper_exe, "-m", model_bin, "-f", p], capture_output=True, text=True, encoding="utf-8")
    lines = [l.strip() for l in res.stdout.splitlines() if '-->' in l]
    
    print(f"\n================ Section {sec:02d} ================")
    print(f"Old transcript length: {len(old_txt)} chars")
    print(f"Whisper timestamped segments: {len(lines)}")
    # compare text length
    full_new = " ".join([re.sub(r'\[.*?\]', '', l).strip() for l in lines])
    print(f"New full text length: {len(full_new)} chars")
    if len(full_new) > len(old_txt) * 1.2:
        print(f"WARNING: Major drop detected! Old={len(old_txt)} vs New={len(full_new)}")
