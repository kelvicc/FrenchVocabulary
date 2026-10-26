# -*- coding: utf-8 -*-
"""
Verification script for duo_francais/index.html and duo_francais/mobile.html
"""
import os
import re
import sys
import json

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)


def verify_html_file(filename, is_mobile=False):
    html_path = os.path.join(BASE_DIR, filename)
    assert os.path.exists(html_path), f"{filename} does not exist"
    size_kb = os.path.getsize(html_path) / 1024
    print(f"[{filename}] HTML Size: {size_kb:.1f} KB ({size_kb / 1024:.2f} MB)")
    assert size_kb < 7000, f"{filename} file size too large ({size_kb:.1f} KB > 7000 KB)"

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Check card IDs
    card_ids = re.findall(r'id="card-(\d+)"', html)
    print(f"[{filename}] Found {len(card_ids)} cards. Range: {card_ids[0]} to {card_ids[-1]}")
    assert len(card_ids) == 560, f"Expected 560 cards, found {len(card_ids)}"

    # 2. Check section IDs
    sec_ids = re.findall(r'id="section-(\d+)"', html)
    print(f"[{filename}] Found {len(sec_ids)} section containers. Range: {sec_ids[0]} to {sec_ids[-1]}")
    assert len(sec_ids) == 45, f"Expected 45 sections, found {len(sec_ids)}"

    # 3. Check audio file existence on disk
    missing_audio = []
    for cid in card_ids:
        mp3 = os.path.join(BASE_DIR, "audio", f"sentence_{cid}.mp3")
        if not os.path.exists(mp3):
            missing_audio.append(mp3)
    assert len(missing_audio) == 0, f"Missing MP3s: {missing_audio[:5]}"

    # 4. Check section opus existence on disk
    missing_opus = []
    for s in sec_ids:
        opus = os.path.join(BASE_DIR, "audio_sections", f"section_{s}.opus")
        if not os.path.exists(opus):
            missing_opus.append(opus)
    assert len(missing_opus) == 0, f"Missing OPUS: {missing_opus[:5]}"

    # 5. Check compact JSON index entries
    json_match = re.search(r'const INDEX_DATA = (\[.*?\]);\s*\n', html, re.DOTALL)
    assert json_match, f"INDEX_DATA array not found in {filename}"
    index_data = json.loads(json_match.group(1))
    print(f"[{filename}] Found {len(index_data):,} A-Z Index Entries in compact INDEX_DATA.")
    assert len(index_data) >= 11000, f"Expected >= 11000 index entries, found {len(index_data)}"

    # 6. Check for strikethrough tags and literal **
    s_tags = re.findall(r'<s\b[^>]*>', html)
    assert len(s_tags) == 0, f"Unexpected <s> tags found in {filename}: {len(s_tags)}"

    body_match = re.search(r'<body>(.*?)</body>', html, re.DOTALL)
    if body_match:
        body_text = body_match.group(1)
        asterisk_in_text = re.findall(r'>[^<]*\*\*[a-zA-Z0-9À-ÿ\s~]+?\*\*[^<]*<', body_text)
        assert len(asterisk_in_text) == 0, f"Literal ** found in {filename}: {len(asterisk_in_text)}"

    # 7. Check UI elements & performance styles
    assert 'id="global-search"' in html, "Search input missing"
    assert 'id="modal-sections"' in html, "Sections drawer modal missing"
    assert 'id="modal-index"' in html, "A-Z index modal missing"
    assert 'id="player-dock"' in html, "Player dock missing"
    assert 'tool-mask-jp' in html, "Mask JP tool missing"
    assert 'tool-mask-meaning' in html, "Mask meaning tool missing"
    assert 'tool-mask-cloze' in html, "Mask cloze tool missing"
    assert 'az-search-input' in html, "A-Z quick search missing"
    assert 'content-visibility: auto;' in html, "content-visibility optimization missing"
    assert '<span class="syn-badge">＝</span>' in html, "Expected ＝ syn-badge"
    assert '<span class="ant-badge">⇔</span>' in html, "Expected ⇔ ant-badge"

    if is_mobile:
        assert 'class="thumb-nav-bar"' in html, "Mobile thumb navigation bar missing"
        assert 'touchstart' in html and 'touchend' in html, "Mobile swipe handlers missing"
        assert 'id="nav-prev-sentence"' in html and 'id="nav-next-sentence"' in html, "Mobile prev/next buttons missing"
        assert 'flex: 0 0 33%;' in html, "Mobile 2-column side-by-side layout missing"


if __name__ == "__main__":
    verify_html_file("index.html", is_mobile=False)
    print("-" * 60)
    verify_html_file("mobile.html", is_mobile=True)
    print("=" * 60)
    print("✅ ALL AUTOMATED VERIFICATION CHECKS (DESKTOP & MOBILE) PASSED 100%!")
    print("=" * 60)
