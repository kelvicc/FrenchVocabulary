# -*- coding: utf-8 -*-
import glob
import re

def compare_sec(sec_num):
    t_pattern = f"duo_francais/Duo3.0 original/transcripts/*{sec_num:02d} Section*.txt"
    t_files = glob.glob(t_pattern)
    if not t_files:
        t_pattern = f"duo_francais/Duo3.0 original/transcripts/*Section {sec_num}*.txt"
        t_files = glob.glob(t_pattern)
    t_text = ""
    if t_files:
        with open(t_files[0], 'r', encoding='utf-8') as f:
            t_text = f.read()
    s_path = f"duo_francais/sections/section_{sec_num:02d}.md"
    with open(s_path, 'r', encoding='utf-8') as f:
        s_text = f.read()
    
    fr_sentences = re.findall(r'### No\.\s*(\d+)[^\n]*\n>\s*(.*?)\n', s_text)
    print(f"=== SEC {sec_num:02d} ===")
    print(f"Transcript: {t_text.strip()[:120]}...")
    print(f"FR count: {len(fr_sentences)}")
    for num, fr in fr_sentences:
        print(f"  No.{num}: {fr[:70]}")

for s in [3, 4, 5, 6, 7, 8]:
    compare_sec(s)
