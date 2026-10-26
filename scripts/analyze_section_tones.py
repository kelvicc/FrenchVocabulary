import os
import re

SECTIONS_DIR = "sections"
files = sorted([f for f in os.listdir(SECTIONS_DIR) if f.endswith(".md")])

results = []

for fname in files:
    fpath = os.path.join(SECTIONS_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()

    m_title = re.search(r"^#\s+(Section\s+\d+.*?)$", text, re.MULTILINE)
    title = m_title.group(1) if m_title else fname

    sentences = re.findall(r"^###\s+No\.\s*\d+.*?\[(.*?)\]", text, re.MULTILINE)
    total_sents = len(sentences)
    dialogues = sum(1 for cast in sentences if "&" in cast)

    results.append({
        "file": fname,
        "title": title,
        "total": total_sents,
        "dialogues": dialogues,
        "pct": (dialogues / total_sents * 100) if total_sents > 0 else 0
    })

for r in results:
    print(f"{r['file']:14s} | sents: {r['total']:2d} | duets: {r['dialogues']:2d} ({r['pct']:4.1f}%) | {r['title']}")
