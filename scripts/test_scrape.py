# -*- coding: utf-8 -*-
import urllib.request
import re

def scrape_duo_section(sec):
    for u in [f"https://yayoi0004.com/duo-section{sec}/", f"https://yayoi0004.com/duo-section-{sec}/"]:
        try:
            req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                # find headings like <h3>282. ...</h3> or similar
                # let's see how sentences are numbered
                items = re.findall(r'<h[234][^>]*?>\s*(\d+)\.\s*(.*?)</h[234]>', html)
                if not items:
                    items = re.findall(r'<p[^>]*?>\s*<strong>\s*(\d+)\.\s*(.*?)</strong>', html)
                if items:
                    print(f"Sec {sec}: Found {len(items)} items from {u}")
                    for num, text in items[:3]:
                        print(f"   {num}: {text[:50]}")
                    return items
        except Exception as e:
            pass
    print(f"Sec {sec}: Failed")
    return []

scrape_duo_section(24)
scrape_duo_section(13)
