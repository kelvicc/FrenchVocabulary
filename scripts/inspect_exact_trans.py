# -*- coding: utf-8 -*-
import glob
import re

# Let's inspect transcripts in detail
# How are sentences separated in transcripts?
# Let's print out the exact text of Section 24 in transcripts:
with open('duo_francais/Duo3.0 original/transcripts/24 Section 24.txt', 'r', encoding='utf-8') as f:
    t24 = f.read()

print("--- 24 Section 24.txt ---")
print(t24)

with open('duo_francais/Duo3.0 original/transcripts/27 Section 27.txt', 'r', encoding='utf-8') as f:
    t27 = f.read()

print("\n--- 27 Section 27.txt ---")
print(t27)
