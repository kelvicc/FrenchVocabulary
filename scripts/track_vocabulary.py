# -*- coding: utf-8 -*-
"""
DUO Français Vocabulary Tracker & Quality Auditor
Scans section markdown files, extracts all lemmas/words, checks for duplicates,
and reports coverage and gender distribution.
"""
import os
import re
import sys
from collections import Counter

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
SECTIONS_DIR = os.path.join(BASE_DIR, "sections")
os.makedirs(SECTIONS_DIR, exist_ok=True)

def audit_sections():
    files = sorted([f for f in os.listdir(SECTIONS_DIR) if f.endswith(".md")])
    if not files:
        print(f"No section markdown files found in {SECTIONS_DIR} yet.")
        return

    # Optional section filter: --until 22 or --max-section 22
    max_sec = None
    for i, arg in enumerate(sys.argv):
        if arg in ("--until", "--max-section", "-m") and i + 1 < len(sys.argv):
            try:
                max_sec = int(sys.argv[i + 1])
            except ValueError:
                pass

    if max_sec:
        files = [f for f in files if re.search(r'\d+', f) and int(re.search(r'\d+', f).group()) <= max_sec]

    all_lemmas = []
    file_map = {}
    total_sentences = 0
    gender_counts = Counter()

    for fname in files:
        fpath = os.path.join(SECTIONS_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # Count sentences
        sentences = re.findall(r"^###\s+No\.\s*\d+", content, re.MULTILINE)
        total_sentences += len(sentences)

        # Extract lemma items: e.g. - **respecter** or - **001 | prévoir...**
        lemmas = re.findall(r"^-\s+\*\*(?:(?:\d+\s*\|\s*)?)([^*]+?)\*\*", content, flags=re.MULTILINE)
        for lemma in lemmas:
            clean = lemma.strip().replace("...", "").lower()
            all_lemmas.append(clean)
            if clean not in file_map:
                file_map[clean] = []
            file_map[clean].append(fname)

        # Count genders
        gender_counts["masc"] += len(re.findall(r"【名・男】", content))
        gender_counts["fem"] += len(re.findall(r"【名・女】", content))

    counts = Counter(all_lemmas)
    duplicates = {word: count for word, count in counts.items() if count > 1}

    print("=" * 60)
    print(f"DUO Français Progress Report")
    print(f"  Processed files   : {len(files)} sections")
    print(f"  Total sentences   : {total_sentences} sentences")
    print(f"  Total lemmas      : {len(all_lemmas)} items ({len(counts)} unique)")
    print(f"  Gender balance    : Masculine {gender_counts['masc']} / Feminine {gender_counts['fem']}")
    print("=" * 60)

    if duplicates:
        print(f"⚠️ DUPLICATE WARNING: {len(duplicates)} words appear more than once!")
        for word, cnt in duplicates.items():
            print(f"   - '{word}' ({cnt} times in {file_map[word]})")
        print("=" * 60)
        if "--strict" in sys.argv:
            sys.exit(1)
    else:
        print("✅ No duplicates found. Perfect DUO compression integrity maintained!")
        print("=" * 60)

    if len(sys.argv) > 1:
        skip_next = False
        cands = []
        for i, a in enumerate(sys.argv[1:], 1):
            if skip_next:
                skip_next = False
                continue
            if a in ("--until", "--max-section", "-m"):
                skip_next = True
                continue
            if not a.startswith("--"):
                cands.append(a)
        if cands:
            existing_set = set(all_lemmas)
            for w in list(existing_set):
                s = re.sub(r"^(le|la|l'|les|un|une|des)\s+", "", w)
                existing_set.add(s)
            for c in cands:
                cl = c.lower().strip()
                st = re.sub(r"^(le|la|l'|les|un|une|des)\s+", "", cl)
                status = "DUP" if (cl in existing_set or st in existing_set) else "OK"
                print(f"  [{status}] {c}")

if __name__ == "__main__":
    audit_sections()

