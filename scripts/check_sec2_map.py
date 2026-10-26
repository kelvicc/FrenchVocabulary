# -*- coding: utf-8 -*-
import json
import re
from run_full_audit import parse_verified_section, parse_french_section

# Let's inspect Section 2, 3, 4, 5, 6, 7, 8, 9
# In Section 2:
# AUDIO 01: Bob was so beside himself that he could scarcely tell fact from fiction. -> MISSING
# AUDIO 02: His new novel, which combines prose with his gift for poetry, is going to be published. -> MISSING
# AUDIO 03: An up-to-date edition of the Encyclopedia will come out next month. -> In Sec 8? (No.085: 百科事典の新版)
# AUDIO 04: Miziamara translated the fascinating fairy tale into plain Japanese. -> MISSING
# AUDIO 05: The following passage is quoted from a well-known fable. -> FR 013
# AUDIO 06 & 07: Are you familiar with contemporary literature? / I know next to nothing about it. -> FR 014
# AUDIO 08: At times, I confuse "curve" with "carve". -> FR 015
# AUDIO 09: Don't be shy. Your pronunciation is more or less correct. -> FR 016
# AUDIO 10: This article contains tips for those who are eager to increase their vocabulary. -> FR 017
# AUDIO 11 & 12: His latest works are on display at the city hall. / They are fabulous beyond description. -> FR 018
# AUDIO 13 & 14: Could you move over a little? / Oh, sorry. I didn't realize I was taking up so much space. -> FR 019
# AUDIO 15 & 16: What's this ugly object? / This is a piece of abstract art. -> MISSING (FR 020 is "要するに、この実用的な著作は...")

print("Sec 02 mapping clear.")
