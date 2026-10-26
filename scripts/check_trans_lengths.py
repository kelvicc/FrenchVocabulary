# -*- coding: utf-8 -*-
import glob
import os

trans_files = sorted(glob.glob('duo_francais/Duo3.0 original/transcripts/*.txt'))
for f in trans_files:
    with open(f, 'r', encoding='utf-8') as fp:
        lines = fp.read().strip()
    words = len(lines.split())
    print(f"{os.path.basename(f)}: {words} words, {len(lines)} chars")
