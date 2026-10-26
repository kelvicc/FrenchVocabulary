# -*- coding: utf-8 -*-
from parse_helpers import get_verified_sentences, get_french_sentences

sec19_v = get_verified_sentences(19)
sec19_fr = get_french_sentences(19)

print("=== Section 19 Verified Audio ===")
for i, l in enumerate(sec19_v, 1):
    print(f"[{i:02d}] {l}")

print("\n=== Section 19 French Sentences ===")
for item in sec19_fr:
    print(f"[FR {item['num']}] {item['ja']}")
