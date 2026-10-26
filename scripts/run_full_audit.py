# -*- coding: utf-8 -*-
import os
import re

def parse_verified_section(sec):
    v_path = f"duo_francais/Duo3.0 original/transcripts_verified/{sec:02d}_Section_{sec}.txt"
    if not os.path.exists(v_path):
        return []
    with open(v_path, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if '-->' in l]
    
    segments = []
    for l in lines:
        m = re.search(r'\[(.*?)\]\s*(.*)', l)
        if m:
            ts, text = m.group(1), m.group(2).strip()
            text = re.sub(r'^Section\s*\d+[\.:\-]?\s*', '', text, flags=re.IGNORECASE).strip()
            if text:
                segments.append({'ts': ts, 'text': text})
    return segments

def parse_french_section(sec):
    fr_path = f"duo_francais/sections/section_{sec:02d}.md"
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
            'ja': ja,
            'body': body
        })
    return results

def full_audit():
    with open("duo_francais/scripts/missing_sentences_report.txt", "w", encoding="utf-8") as out:
        out.write("======================================================================\n")
        out.write("DETAILED AUDIT: DUO 3.0 Audio Sentences vs French Edition (Sec 01-29)\n")
        out.write("======================================================================\n\n")

        for sec in range(1, 30):
            v_segs = parse_verified_section(sec)
            fr_sents = parse_french_section(sec)
            
            out.write(f"\n######################################################################\n")
            out.write(f"### SECTION {sec:02d} (Audio segments: {len(v_segs)} | French sentences: {len(fr_sents)})\n")
            out.write(f"######################################################################\n")
            
            out.write("--- Audio Segments ---\n")
            for i, seg in enumerate(v_segs, 1):
                out.write(f"  [{i:02d}] ({seg['ts']}) {seg['text']}\n")
            
            out.write("\n--- French Edition Sentences ---\n")
            for item in fr_sents:
                out.write(f"  [FR No.{item['num']}] {item['ja']}\n")
                out.write(f"         FR: {item['fr'][:80]}...\n")

if __name__ == '__main__':
    full_audit()
    print("Full audit report written to duo_francais/scripts/missing_sentences_report.txt")
