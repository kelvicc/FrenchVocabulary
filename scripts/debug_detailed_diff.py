# -*- coding: utf-8 -*-
import glob
import os
import re

def parse_section_md(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Extract blocks: ### No. XXX ... > **French** ... > [!NOTE] Japanese translation
    pattern = r'### No\.\s*(\d+)[^\n]*\n>\s*(.*?)\n(.*?)(?=(?:### No\.|\Z))'
    matches = re.findall(pattern, text, re.DOTALL)
    
    results = []
    for num, fr_sent, body in matches:
        # extract note
        note_match = re.search(r'>\s*\[!NOTE\]\s*(.*?)(?=\n-|\n&|\n□|\n<|\Z)', body, re.DOTALL)
        note = note_match.group(1).strip() if note_match else ""
        results.append({
            'num': num,
            'fr': fr_sent.strip(),
            'ja': note.strip().splitlines()[0] if note else ""
        })
    return results

def inspect_section_diff(sec_num):
    # Transcript
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
    fr_data = parse_section_md(s_path)
    
    print(f"\n==========================================")
    print(f"SECTION {sec_num:02d}")
    print(f"==========================================")
    print(f"--- Transcript ---")
    print(t_text.strip())
    print(f"\n--- French Edition ({len(fr_data)} sentences) ---")
    for item in fr_data:
        print(f"No. {item['num']}: {item['fr']}")
        print(f"    JA: {item['ja']}")

if __name__ == '__main__':
    for sec in [13, 24, 27, 5, 6]:
        inspect_section_diff(sec)
