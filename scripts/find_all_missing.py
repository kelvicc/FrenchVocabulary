# -*- coding: utf-8 -*-
import os
import re

# We will analyze all sections from 1 to 29 and identify EVERY missing sentence.
# Let's inspect Section by Section and output a structured list of missing sentences.

from run_full_audit import parse_verified_section, parse_french_section

def analyze_all_missing():
    missing_by_section = {}

    # Section 13:
    # [04] They are hostile to Richard because they are jealous of his wealth and status.
    # [05] I hate him. He behaves as if he were somebody.
    
    # Let's write an automated search for each audio line against French text / Japanese translation
    for sec in range(1, 30):
        v_segs = parse_verified_section(sec)
        fr_sents = parse_french_section(sec)
        
        # Combine all French and Japanese text in this section
        all_fr_text = " ".join([item['fr'] + " " + item['ja'] + " " + item['body'] for item in fr_sents]).lower()
        
        # Also check adjacent sections (sec-1, sec+1) in case of slide
        prev_fr = parse_french_section(sec - 1) if sec > 1 else []
        next_fr = parse_french_section(sec + 1) if sec < 29 else []
        combined_context = all_fr_text + " " + " ".join([item['fr'] + " " + item['ja'] for item in prev_fr + next_fr]).lower()

        missing_in_sec = []
        for i, s in enumerate(v_segs, 1):
            txt = s['text']
            
            # Extract key words (alphanumeric words >= 4 chars)
            # ignore very common words
            words = [w.lower() for w in re.findall(r'[a-zA-Z]{4,}', txt) if w.lower() not in {
                'this', 'that', 'with', 'from', 'have', 'were', 'what', 'when', 'will', 'your', 'about', 'there', 'they', 'would', 'could', 'should'
            }]
            
            # Check if any significant trace of this sentence exists in French section
            # For DUO, let's manually inspect sections where discrepancy exists
            pass

analyze_all_missing()
