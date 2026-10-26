# -*- coding: utf-8 -*-
import os
import re
from duo_official_ranges import DUO_OFFICIAL_RANGES

def audit_all_sections():
    print("===============================================================")
    print("AUDIT: Official DUO 3.0 (560 Sentences) vs French Edition")
    print("===============================================================")
    
    total_official_sentences = 0
    total_fr_sentences = 0
    discrepancies = []

    for sec in range(1, 30):
        start_no, end_no, official_count = DUO_OFFICIAL_RANGES[sec]
        total_official_sentences += official_count
        
        # Load French edition section
        fr_file = f"duo_francais/sections/section_{sec:02d}.md"
        fr_sentences = []
        if os.path.exists(fr_file):
            with open(fr_file, 'r', encoding='utf-8') as f:
                content = f.read()
            matches = re.findall(r'### No\.\s*(\d+)[^\n]*\n>\s*(.*?)\n', content)
            fr_sentences = matches
        
        fr_count = len(fr_sentences)
        total_fr_sentences += fr_count
        
        # Load verified transcript
        v_file = f"duo_francais/Duo3.0 original/transcripts_verified/{sec:02d}_Section_{sec}.txt"
        v_lines = []
        if os.path.exists(v_file):
            with open(v_file, 'r', encoding='utf-8') as f:
                v_lines = [l.strip() for l in f if '-->' in l]
        
        diff = fr_count - official_count
        status = "OK" if diff == 0 else f"DIFF ({diff:+d})"
        
        print(f"Sec {sec:02d}: Official No.{start_no:03d}-{end_no:03d} ({official_count:2d}文) | FR: {fr_count:2d}文 (No.{fr_sentences[0][0] if fr_sentences else '???'} - No.{fr_sentences[-1][0] if fr_sentences else '???'}) -> {status}")
        
        if diff != 0:
            discrepancies.append({
                'sec': sec,
                'official_range': (start_no, end_no),
                'official_count': official_count,
                'fr_count': fr_count,
                'diff': diff,
                'fr_range': (fr_sentences[0][0], fr_sentences[-1][0]) if fr_sentences else (None, None)
            })

    print("===============================================================")
    print(f"Total Official Sentences (Sec 1-29): {total_official_sentences}")
    print(f"Total French Sentences (Sec 1-29):   {total_fr_sentences}")
    print(f"Net Gap: {total_fr_sentences - total_official_sentences} sentences")
    print(f"Discrepancies found in {len(discrepancies)} sections.")
    print("===============================================================")

if __name__ == '__main__':
    audit_all_sections()
