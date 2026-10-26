# -*- coding: utf-8 -*-
from run_full_audit import parse_verified_section, parse_french_section

# Combine all French JA and FR text from Sec 1 to 10
all_fr_text_1_10 = ""
for s in range(1, 11):
    fr_sents = parse_french_section(s)
    for it in fr_sents:
        all_fr_text_1_10 += f" [Sec{s:02d} No.{it['num']}] " + it['ja'] + " " + it['fr']

print("Loaded all FR 1-10 text.")

# Now check each verified audio line in Sec 1 to 10
missing_in_1_10 = []
for s in range(1, 11):
    v_segs = parse_verified_section(s)
    for i, seg in enumerate(v_segs, 1):
        txt = seg['text']
        # check keywords
        pass
