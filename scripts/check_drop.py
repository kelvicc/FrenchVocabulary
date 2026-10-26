# -*- coding: utf-8 -*-
# Check if any DUO sentence was entirely dropped
import glob
import re

# Let's inspect Section 08 & 09
with open('duo_francais/Duo3.0 original/transcripts/08 Section 8.txt', 'r', encoding='utf-8') as f:
    t8 = f.read()

print("Sec 8 transcript:")
print(t8)
