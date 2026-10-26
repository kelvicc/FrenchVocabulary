# -*- coding: utf-8 -*-
import urllib.request
import re

section_ranges = {}

for s in range(1, 46):
    urls = [
        f"https://yayoi0004.com/duo-section{s}/",
        f"https://yayoi0004.com/duo-section-{s}/",
        f"https://yayoi0004.com/duo-section{s:02d}/"
    ]
    found = False
    for u in urls:
        try:
            req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                # look for title or h1/h2 or text like "英文 No. X〜Y" or "英文X〜Y"
                m = re.search(r'英文\s*(?:No\.?)?\s*(\d+)\s*[〜～\-]\s*(\d+)', html)
                if not m:
                    m = re.search(r'Section\s*' + str(s) + r'[^\d]*?(\d+)\s*[〜～\-]\s*(\d+)', html, re.IGNORECASE)
                if m:
                    start, end = int(m.group(1)), int(m.group(2))
                    section_ranges[s] = (start, end)
                    print(f"Section {s:02d}: {start} - {end} (count: {end - start + 1})")
                    found = True
                    break
        except Exception as e:
            pass
    if not found:
        print(f"Section {s:02d}: NOT FOUND")

print(f"Total found: {len(section_ranges)} / 45")
