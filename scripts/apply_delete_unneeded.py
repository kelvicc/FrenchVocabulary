# -*- coding: utf-8 -*-
import os
import re
import sys
from collections import Counter
from simulate_delete_unneeded import ITEMS_TO_DELETE, ITEMS_TO_MODIFY, remove_lemma_entry

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTIONS_DIR = os.path.join(BASE_DIR, 'sections')

def apply_delete_and_renumber():
    modified_contents = {}

    for i in range(1, 23):
        fname = f'section_{i:02d}.md'
        fpath = os.path.join(SECTIONS_DIR, fname)
        content = open(fpath, 'r', encoding='utf-8').read()

        # Apply modifications first
        for (sec_name, num), (old_pat, new_pat) in ITEMS_TO_MODIFY.items():
            if sec_name == fname:
                if old_pat not in content:
                    print(f"ERROR: old pattern not in {fname}: {old_pat[:40]}")
                    sys.exit(1)
                content = content.replace(old_pat, new_pat)

        # Apply deletions
        for sec_name, pat in ITEMS_TO_DELETE:
            if sec_name == fname:
                content = remove_lemma_entry(content, pat)

        modified_contents[fname] = content

    # Renumber continuously from 0001
    current_num = 1
    all_lemmas = []
    file_map = {}

    for i in range(1, 23):
        fname = f'section_{i:02d}.md'
        fpath = os.path.join(SECTIONS_DIR, fname)
        content = modified_contents[fname]

        def renumber_match(m):
            nonlocal current_num
            old_num = m.group(1)
            lemma_text = m.group(2)
            formatted = f"- **{current_num:04d} | {lemma_text}**"
            current_num += 1
            return formatted

        new_content = re.sub(r'-\s+\*\*(\d+)\s*\|\s*([^*]+?)\*\*', renumber_match, content)

        # Write to disk
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        lemmas = re.findall(r'-\s+\*\*(\d+)\s*\|\s*([^*]+?)\*\*', new_content)
        for num, lemma in lemmas:
            clean = lemma.strip().replace('...', '').lower()
            all_lemmas.append((num, clean, lemma.strip(), fname))
            if clean not in file_map:
                file_map[clean] = []
            file_map[clean].append((num, lemma.strip(), fname))

        print(f"Updated {fname}: {len(lemmas)} lemmas (range: {lemmas[0][0]} ~ {lemmas[-1][0]})")

    counts = Counter([clean for num, clean, orig, f in all_lemmas])
    dups = {w: entries for w, entries in file_map.items() if len(entries) > 1}

    print("=" * 60)
    print("FINAL SUMMARY FOR SECTIONS 01-22:")
    print(f"  Total sections        : 22")
    print(f"  Total items           : {len(all_lemmas)} (Deletions applied: {1073 - len(all_lemmas)})")
    print(f"  Unique lemmas         : {len(counts)}")
    print(f"  Duplicate count       : {len(dups)}")
    print(f"  Continuous numbering  : {all_lemmas[0][0]} ~ {all_lemmas[-1][0]}")
    print("=" * 60)

    if dups:
        print("ERROR: Duplicates found:", dups)
        sys.exit(1)
    else:
        print("SUCCESS! All unneeded headings deleted and sections cleanly renumbered.")

if __name__ == '__main__':
    apply_delete_and_renumber()
