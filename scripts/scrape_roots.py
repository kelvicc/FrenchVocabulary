# -*- coding: utf-8 -*-
import urllib.request
import re

roots_ranges = {}

for s in range(1, 46):
    url = f"https://roots-ruru.com/duo3-0-section-{s}/"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # find title like <title>...SECTION X(XXX~YYY)...</title>
            m = re.search(r'SECTION\s*' + str(s) + r'\s*\((\d+)[～~](\d+)\)', html, re.IGNORECASE)
            if not m:
                m = re.search(r'SECTION\s*' + str(s) + r'[^\(]*?\((\d+)[～~](\d+)\)', html, re.IGNORECASE)
            if m:
                start, end = int(m.group(1)), int(m.group(2))
                roots_ranges[s] = (start, end, end - start + 1)
                print(f"Section {s:02d}: {start} - {end} ({end - start + 1} sentences)")
            else:
                print(f"Section {s:02d}: Pattern not matched in HTML")
    except Exception as e:
        print(f"Section {s:02d}: {e}")

print(f"Total resolved from roots-ruru: {len(roots_ranges)} / 45")
