# -*- coding: utf-8 -*-
import os
import sys
from test_dry_run import REPLACEMENTS

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTIONS_DIR = os.path.join(BASE_DIR, 'sections')

def apply_replacements():
    modified_files = 0
    total_replacements = 0

    for fname, pairs in REPLACEMENTS.items():
        fpath = os.path.join(SECTIONS_DIR, fname)
        content = open(fpath, 'r', encoding='utf-8').read()
        file_changed = False

        for old_pat, new_pat in pairs:
            if old_pat not in content:
                print(f"❌ Error in {fname}: pattern not found:\n{old_pat}")
                sys.exit(1)
            content = content.replace(old_pat, new_pat)
            file_changed = True
            total_replacements += 1

        if file_changed:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated {fname} ({len(pairs)} replacements)")
            modified_files += 1

    print(f"\nSuccessfully applied {total_replacements} replacements across {modified_files} section files.")

if __name__ == '__main__':
    apply_replacements()
