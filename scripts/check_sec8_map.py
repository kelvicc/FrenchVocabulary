# -*- coding: utf-8 -*-
import os
import re

# We will exhaustively verify every single sentence of DUO 3.0 (No. 001 to 353)
# and determine EXACTLY which ones are missing from the French edition.

from run_full_audit import parse_verified_section, parse_french_section

# Let's inspect Section 08 and 09 as well:
# In Sec 08 audio:
# [01] Bringing flammable items into the cabin is prohibited.
# [02] Our flight to Vienna was delayed on account of a minor accident.
# [03] The plane blew up and plunged into the ocean, killing all the people on board.
# [04] They are working around the clock, looking into the cause of the crash.
# [05] Unfortunately, few passengers survived the catastrophe.
# [06] The aviation expert analyzed the statistics in detail.
# [07] On behalf of all the staff, I'd like to express our sympathy for the victims.
# [08] In a sense, he is to blame for the disaster.
# [09] The vehicles are inspected for defects every three months.

# In FR 08:
# No. 085: 百科事典
# No. 086: 行間を読む
# No. 087: 飛行機空中爆発 (Audio [03])
# No. 088: 原因究明 (Audio [04])
# No. 089: 生存者わずか (Audio [05])
# No. 090: 再発防止 (not in audio? or [07] sympathy?)
# No. 091: 盲目的な暴力 (where from?)
# No. 092: 車両定期点検 (Audio [09])
# No. 093: 電気代 (Sec 09 Audio [01])
# No. 094: 蛇口 (Sec 09 Audio [02])
# No. 095: 蓋 (Sec 09 Audio [03])
# No. 096: 賞味期限 (Audio [04] scissors missing?)

print("Sec 08 detailed scan ready.")
