# -*- coding: utf-8 -*-
import os
import re

# We will load the verified transcripts for Sec 1 to 29
# and extract the exact DUO English sentences.
# Let's inspect transcripts_verified for Sec 1 to 29.

def get_clean_audio_sentences(sec):
    p = f"duo_francais/Duo3.0 original/transcripts_verified/{sec:02d}_Section_{sec}.txt"
    with open(p, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if '-->' in l]
    sents = []
    for l in lines:
        text = re.sub(r'\[.*?\]\s*', '', l).strip()
        text = re.sub(r'^Section\s*\d+[\.:\-]?\s*', '', text, flags=re.IGNORECASE).strip()
        if text:
            sents.append(text)
    return sents

# Let's count total audio segments across Sec 1 to 29
total_segs = 0
for s in range(1, 30):
    sents = get_clean_audio_sentences(s)
    total_segs += len(sents)

print(f"Total audio segments Sec 1-29: {total_segs}")
