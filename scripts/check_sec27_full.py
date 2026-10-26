# -*- coding: utf-8 -*-
import subprocess
import re

whisper_exe = r"c:\Users\noid\Documents\antigravity\kind-fermi\tools\whisper.cpp\Release\whisper-cli.exe"
model_bin = r"c:\Users\noid\Documents\antigravity\kind-fermi\tools\whisper.cpp\models\ggml-base.en.bin"
p = r"duo_francais\Duo3.0 original\DUO audio\27 Section 27.mp3"

res = subprocess.run([whisper_exe, "-m", model_bin, "-f", p], capture_output=True, text=True, encoding="utf-8")
lines = [l.strip() for l in res.stdout.splitlines() if '-->' in l]
for l in lines:
    print(l)
