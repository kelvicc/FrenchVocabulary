# -*- coding: utf-8 -*-
import glob
import os
import re

# Load verified transcripts and parse sentences
def get_verified_sentences(sec_num):
    v_path = f"duo_francais/Duo3.0 original/transcripts_verified/{sec_num:02d}_Section_{sec_num}.txt"
    if not os.path.exists(v_path):
        return []
    with open(v_path, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if '-->' in l]
    
    # Extract clean text without timestamps
    clean_lines = []
    for l in lines:
        text = re.sub(r'\[.*?\]\s*', '', l).strip()
        # remove "Section X." header if present
        text = re.sub(r'^Section\s*\d+[\.:\-]?\s*', '', text, flags=re.IGNORECASE).strip()
        if text:
            clean_lines.append(text)
    return clean_lines

def get_french_sentences(sec_num):
    fr_path = f"duo_francais/sections/section_{sec_num:02d}.md"
    if not os.path.exists(fr_path):
        return []
    with open(fr_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = re.findall(r'### No\.\s*(\d+)[^\n]*\n>\s*(.*?)\n(.*?)(?=(?:### No\.|\Z))', content, re.DOTALL)
    results = []
    for num, fr_sent, body in matches:
        note_m = re.search(r'>\s*\[!NOTE\]\s*(.*?)(?=\n-|\n&|\n□|\n<|\Z)', body, re.DOTALL)
        ja = note_m.group(1).strip().splitlines()[0] if note_m else ""
        results.append({
            'num': num,
            'fr': fr_sent.strip(),
            'ja': ja
        })
    return results

print("Helper loaded.")
