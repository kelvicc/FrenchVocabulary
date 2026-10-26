# -*- coding: utf-8 -*-
import glob
import re

# We know the official DUO 3.0 has 560 sentences across 45 sections.
# Let's count how many sentences each section has in transcripts
# by parsing the sentences accurately.

# Let's check the audio files or transcripts.
# In transcripts, sentences are written. Let's see how many sentences are in each transcript file!
def split_duo_sentences(text):
    # Remove "Section X." header
    text = re.sub(r'^Section\s*\d+[\.:]?\s*', '', text, flags=re.IGNORECASE).strip()
    
    # Let's see: in transcripts, how are dialogue sentences written?
    # e.g., "Please estimate the losses by Friday at the latest. I'll manage it somehow." -> 1 DUO sentence
    # e.g., "Nick, I'm counting on you. Okay, I'll see to it." -> 1 DUO sentence
    # e.g., "Thanks. I appreciate it. Don't mention it." -> 1 DUO sentence
    pass

# Instead of guessing, let's write a script to look at Section 10 to 29
# where French edition was created directly following transcripts!
