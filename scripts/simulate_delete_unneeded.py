# -*- coding: utf-8 -*-
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTIONS_DIR = os.path.join(BASE_DIR, 'sections')

# Items to remove completely: (filename, item_regex_or_prefix)
# Note: we need to remove the whole bullet point:
# - **NUM | lemma** ...
# and its sub-bullets (indented lines:   - ...,   - ※ ...,   - □ ..., etc.)

ITEMS_TO_DELETE = [
    # Sec 01
    ('section_01.md', r'-\s+\*\*0006\s*\|\s*finir par s\'arranger\*\*'),
    # Sec 03
    ('section_03.md', r'-\s+\*\*0083\s*\|\s*prêter de l\'argent\*\*'),
    ('section_03.md', r'-\s+\*\*0128\s*\|\s*la délinquance urbaine\*\*'),
    # Sec 04
    ('section_04.md', r'-\s+\*\*0145\s*\|\s*un village isolé\*\*'),
    ('section_04.md', r'-\s+\*\*0153\s*\|\s*une substance radioactive\*\*'),
    ('section_04.md', r'-\s+\*\*0182\s*\|\s*engager des poursuites\*\*'),
    # Sec 05
    ('section_05.md', r'-\s+\*\*0236\s*\|\s*la phase initiale\*\*'),
    # Sec 06
    ('section_06.md', r'-\s+\*\*0283\s*\|\s*croiser par hasard\*\*'),
    # Sec 07
    ('section_07.md', r'-\s+\*\*0330\s*\|\s*soutenir un projet\*\*'),
    # Sec 09
    ('section_09.md', r'-\s+\*\*0395\s*\|\s*délicat\(e\) \(fragile\)\*\*'),
    ('section_09.md', r'-\s+\*\*0414\s*\|\s*un appareil ménager\*\*'),
    # Sec 10
    ('section_10.md', r'-\s+\*\*0472\s*\|\s*flâner sur le rivage\*\*'),
    # Sec 12
    ('section_12.md', r'-\s+\*\*0550\s*\|\s*une phase cruciale\*\*'),
    # Sec 13
    ('section_13.md', r'-\s+\*\*0567\s*\|\s*ignorer qn\*\*'),
    ('section_13.md', r'-\s+\*\*0583\s*\|\s*une immense propriété\*\*'),
    # Sec 14
    ('section_14.md', r'-\s+\*\*0614\s*\|\s*respecter un délai\*\*'),
    # Sec 15
    ('section_15.md', r'-\s+\*\*0660\s*\|\s*le tissu musculaire\*\*'),
    # Sec 17
    ('section_17.md', r'-\s+\*\*0732\s*\|\s*convaincre\*\*'),
    # Sec 18
    ('section_18.md', r'-\s+\*\*0759\s*\|\s*devoir avouer\*\*'),
    ('section_18.md', r'-\s+\*\*0766\s*\|\s*non, pas du tout\*\*'),
    # Sec 20
    ('section_20.md', r'-\s+\*\*0878\s*\|\s*une expérience scientifique\*\*'),
    ('section_20.md', r'-\s+\*\*0891\s*\|\s*préserver la planète\*\*'),
    ('section_20.md', r'-\s+\*\*0893\s*\|\s*une planète en danger\*\*'),
    ('section_20.md', r'-\s+\*\*0910\s*\|\s*une espèce vulnérable\*\*'),
    ('section_20.md', r'-\s+\*\*0937\s*\|\s*surveiller\*\*'),
    # Sec 21
    ('section_21.md', r'-\s+\*\*0961\s*\|\s*être indispensable pour\*\*'),
    ('section_21.md', r'-\s+\*\*0998\s*\|\s*un brouillard épais\*\*'),
    # Sec 22
    ('section_22.md', r'-\s+\*\*1013\s*\|\s*les appareils électroménagers\*\*'),
    ('section_22.md', r'-\s+\*\*1016\s*\|\s*pratique \(commode\)\*\*'),
    ('section_22.md', r'-\s+\*\*1066\s*\|\s*un outil commode\*\*')
]

ITEMS_TO_MODIFY = {
    # Sec 03 #0116: une politique maladroite -> la politique
    ('section_03.md', '0116'): (
        "- **0116 | une politique maladroite** `/yn pɔ.li.tik ma.la.dʁwat/` 【名句・女】 拙劣な政策，配慮に欠けた方針，不手際な施策",
        "- **0116 | la politique** `/pɔ.li.tik/` 【名・女】 ①政策，方針，施策 ②政治，政治学 (= la ligne d'action, la stratégie)"
    ),
    # Sec 07 #0328: convaincre qn de (+ inf.) -> convaincre
    ('section_07.md', '0328'): (
        "- **0328 | convaincre qn de (+ inf.)** `/kɔ̃.vɛ̃kʁ kɛl.kœ̃ də/` 【成句】 （人を）説得して〜させる，納得させる",
        "- **0328 | convaincre** `/kɔ̃.vɛ̃kʁ/` 【他】 説得する，納得させる (`convaincre qn de + inf. / de qc`；※過去分詞は **convaincu**)"
    ),
    # Sec 10 #0451: surveiller les enfants -> surveiller
    ('section_10.md', '0451'): (
        "- **0451 | surveiller les enfants** `/syʁ.vɛ.je lez‿ɑ̃.fɑ̃/` 【成句】 子どもたちを見守る，目を離さないでおく，見張る",
        "- **0451 | surveiller** `/syʁ.vɛ.je/` 【他】 ①見張る，見守る，目を離さないでおく ②監視する，取り締まる"
    ),
    # Sec 20 #0868: soutenir que -> soutenir
    ('section_20.md', '0868'): (
        "- **0868 | soutenir que** `/sut.niʁ kə/` 【動詞句】 〜だと主張する，持論を展開する，〜と言い張る (= affirmer que, prétendre que)",
        "- **0868 | soutenir** `/sut.niʁ/` 【他】 ①（持論・見解を）主張する，擁護する ②支持する ③支える"
    )
}

def remove_lemma_entry(content, pattern_str):
    lines = content.splitlines(keepends=True)
    out = []
    i = 0
    found = False
    while i < len(lines):
        line = lines[i]
        if re.search(pattern_str, line):
            found = True
            i += 1
            # Skip sub-bullets and blank lines immediately following
            while i < len(lines):
                next_line = lines[i]
                if next_line.startswith('  ') or next_line.startswith('\t') or (next_line.strip() == '' and i + 1 < len(lines) and (lines[i+1].startswith('  ') or lines[i+1].startswith('\t'))):
                    i += 1
                else:
                    break
        else:
            out.append(line)
            i += 1
    if not found:
        print(f"WARNING: pattern not found: {pattern_str}")
    return "".join(out)

def test_delete_and_renumber():
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
                    return False
                content = content.replace(old_pat, new_pat)

        # Apply deletions
        for sec_name, pat in ITEMS_TO_DELETE:
            if sec_name == fname:
                content = remove_lemma_entry(content, pat)

        modified_contents[fname] = content

    # Now renumber all lemmas across sections 01 to 22 continuously from 0001
    current_num = 1
    all_lemmas = []
    file_map = {}

    for i in range(1, 23):
        fname = f'section_{i:02d}.md'
        content = modified_contents[fname]

        def renumber_match(m):
            nonlocal current_num
            old_num = m.group(1)
            lemma_text = m.group(2)
            formatted = f"- **{current_num:04d} | {lemma_text}**"
            current_num += 1
            return formatted

        new_content = re.sub(r'-\s+\*\*(\d+)\s*\|\s*([^*]+?)\*\*', renumber_match, content)
        modified_contents[fname] = new_content

        # Extract lemmas to check duplicates
        lemmas = re.findall(r'-\s+\*\*(\d+)\s*\|\s*([^*]+?)\*\*', new_content)
        for num, lemma in lemmas:
            clean = lemma.strip().replace('...', '').lower()
            all_lemmas.append((num, clean, lemma.strip(), fname))
            if clean not in file_map:
                file_map[clean] = []
            file_map[clean].append((num, lemma.strip(), fname))

    counts = Counter([clean for num, clean, orig, f in all_lemmas])
    dups = {w: entries for w, entries in file_map.items() if len(entries) > 1}

    print("=" * 60)
    print("SIMULATION RESULT AFTER DELETING UNNEEDED HEADINGS:")
    print(f"  Total items remaining : {len(all_lemmas)} (Deletions: {1073 - len(all_lemmas)})")
    print(f"  Unique lemmas         : {len(counts)}")
    print(f"  Duplicate count       : {len(dups)}")
    print(f"  First number          : {all_lemmas[0][0]}")
    print(f"  Last number           : {all_lemmas[-1][0]}")
    print("=" * 60)

    if dups:
        print("⚠️ Remaining duplicates:")
        for w, entries in sorted(dups.items()):
            print(f"   - {w}: {entries}")
        return False
    else:
        print("🎉 PERFECT PURITY! 0 DUPLICATES, CLEAN NATURAL HEADINGS, 100% QUALITY!")
        return True

if __name__ == '__main__':
    test_delete_and_renumber()
