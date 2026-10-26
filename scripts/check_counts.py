# -*- coding: utf-8 -*-
import glob
import re

# Let's count total sentences in transcripts 1 to 29
trans_files = sorted(glob.glob('duo_francais/Duo3.0 original/transcripts/*.txt'))
sec_trans = {}
for f in trans_files:
    m = re.search(r'(\d+)\s*Section', f) or re.search(r'Section\s*(\d+)', f)
    if m:
        sec_num = int(m.group(1))
        with open(f, 'r', encoding='utf-8') as fp:
            sec_trans[sec_num] = fp.read()

total_trans_sentences = 0
for s in range(1, 30):
    text = sec_trans.get(s, "")
    # clean header
    text = re.sub(r'Section\s*\d+\.?', '', text, flags=re.IGNORECASE).strip()
    # rough sentence split by . ! ?
    # but not inside quotes
    sentences = [st.strip() for st in re.split(r'(?<=[.!?])\s+', text) if st.strip()]
    total_trans_sentences += len(sentences)
    # print(f"Sec {s:02d}: {len(sentences)} sentences")

print(f"Total transcripts sentences (1-29): {total_trans_sentences}")
