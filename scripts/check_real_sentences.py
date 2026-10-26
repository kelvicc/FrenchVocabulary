# -*- coding: utf-8 -*-
import glob
import os
import re

# Let's inspect the actual audio files of DUO audio!
# Can we check how many tracks or tags there are?
# Or can we read transcripts and count DUO sentences accurately?

# In DUO 3.0, each sentence is a distinct entity.
# Let's write a script that analyzes all 45 transcript files and splits them into DUO sentences.
# Let's see how each transcript is structured.

trans_files = sorted(glob.glob('duo_francais/Duo3.0 original/transcripts/*.txt'))

# Let's print out transcripts of Sec 1 to 5 to see
for f in trans_files[:5]:
    print("="*40)
    print(os.path.basename(f))
    with open(f, 'r', encoding='utf-8') as fp:
        print(fp.read())
