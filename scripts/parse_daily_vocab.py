# -*- coding: utf-8 -*-
"""
parse_daily_vocab.py
Parses daily_vocab.md into structured data.
"""
import sys, os, re, json, unicodedata

sys.stdout.reconfigure(encoding='utf-8')

def get_initial_letter(word):
    w = unicodedata.normalize('NFD', word)
    w = ''.join(c for c in w if unicodedata.category(c) != 'Mn')
    w = re.sub(r"^[ld]['’]|^(le|la|les|un|une|des|du|de la)\s+", "", w, flags=re.IGNORECASE).strip()
    if not w: return "#"
    c = w[0].upper()
    return c if 'A' <= c <= 'Z' else "#"

def get_clean_lemma(word):
    w = re.sub(r"^[ld]['’]|^(le|la|les|un|une|des|du|de la)\s+", "", word, flags=re.IGNORECASE).strip()
    return w.split('/')[0].strip()

def load_daily_vocab_data():
    vocab_path = "duo_francais/data/daily_vocab.md"
    with open(vocab_path, "r", encoding="utf-8") as f:
        text = f.read()

    themes = []
    current_theme = None
    current_group = None
    word_counter = 0

    for line in text.split("\n"):
        line = line.rstrip()
        if line.startswith("# THEME "):
            m = re.match(r"# THEME (\d+):\s*([^(]+)\s*(?:\(([^)]+)\))?", line)
            if m:
                num = int(m.group(1))
                title_ja = m.group(2).strip()
                title_fr = m.group(3).strip() if m.group(3) else ""
                current_theme = {
                    "num": num,
                    "title_ja": title_ja,
                    "title_fr": title_fr,
                    "groups": []
                }
                themes.append(current_theme)
        elif line.startswith("## "):
            m = re.match(r"##\s*(\d+-\d+)\.\s*([^(]+)\s*(?:\(([^)]+)\))?", line)
            if m and current_theme:
                code = m.group(1).strip()
                title_ja = m.group(2).strip()
                title_fr = m.group(3).strip() if m.group(3) else ""
                current_group = {
                    "code": code,
                    "title_ja": title_ja,
                    "title_fr": title_fr,
                    "words": [],
                    "check": None
                }
                current_theme["groups"].append(current_group)
        elif line.startswith("- "):
            m = re.match(r"- ([^\[]+)\[([^\]]+)\]\s*(.*)", line)
            if m and current_group:
                word_counter += 1
                fr_raw = m.group(1).strip()
                gender = m.group(2).strip()
                meaning = m.group(3).strip()
                did = f"D{word_counter:03d}"
                word_obj = {
                    "did": did,
                    "french": fr_raw,
                    "gender": gender,
                    "meaning": meaning,
                    "phrase_fr": "",
                    "phrase_ja": "",
                    "note": ""
                }
                current_group["words"].append(word_obj)
        elif line.startswith("  ▶ "):
            m = re.match(r"\s*▶\s*([^(]+)\s*(?:\(([^)]+)\))?", line)
            if m and current_group and current_group["words"]:
                w = current_group["words"][-1]
                w["phrase_fr"] = m.group(1).strip()
                w["phrase_ja"] = m.group(2).strip() if m.group(2) else ""
        elif line.startswith("  ★ "):
            if current_group and current_group["words"]:
                w = current_group["words"][-1]
                w["note"] = line.replace("  ★ ", "").strip()
        elif line.startswith("[Check] "):
            parts = line.replace("[Check] ", "").split("|")
            if len(parts) >= 2 and current_group:
                q = parts[0].strip()
                ans = parts[1].strip()
                expl = parts[2].strip() if len(parts) >= 3 else ""
                current_group["check"] = {"q": q, "ans": ans, "expl": expl}

    return themes

if __name__ == "__main__":
    themes = load_daily_vocab_data()
    print(f"Parsed {len(themes)} themes.")
    total = 0
    for t in themes:
        w_cnt = sum(len(g["words"]) for g in t["groups"])
        total += w_cnt
        print(f"Theme {t['num']:02d}: {t['title_ja']} ({len(t['groups'])} groups, {w_cnt} words)")
    print(f"Total words: {total}")
