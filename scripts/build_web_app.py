# -*- coding: utf-8 -*-
"""
DUO Français 3.0 — Interactive Web Application Compiler (Soft Pastel Edition)
Builds the standalone, zero-dependency `duo_francais/index.html` from all 45 section Markdown files and neural audio assets.
Key Layout & Visual Features:
- Soft, Elegant Pastel Color Palette (gentle on the eyes, paper-like readability, reduced saturation).
- Authentic DUO 3.0 Layout: French sentence at top with soft periwinkle banner, separated Japanese translation at bottom.
- Classic 2-Column Vocabulary Layout: Headword + IPA on the left, POS + Meanings/Notes/Derivatives on the right.
- Compact JSON In-Memory Index (reduces file size, eliminates 57,000+ DOM nodes on load).
- On-Demand Tab & Virtualized Search Rendering (60 FPS instant response for all 11,458 vocabulary entries).
- Native CSS `content-visibility: auto` (smooth scrolling across 560 sentence cards).
- Zero external runtime dependencies.
"""

import os
import re
import sys
import json
import html
from daily_vocab_builder import load_daily_vocab_data, get_daily_index_entries, generate_daily_css, generate_daily_sections_html, generate_daily_toc_html, generate_daily_js, generate_app_ui_css
import unicodedata
from collections import defaultdict

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
SECTIONS_DIR = os.path.join(BASE_DIR, "sections")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
SECTION_AUDIO_DIR = os.path.join(BASE_DIR, "audio_sections")
OUTPUT_HTML = os.path.join(BASE_DIR, "index.html")

def remove_accents(input_str):
    nfkd = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])

def normalize_sort_key(word):
    clean = word.lower().strip()
    clean = re.sub(r"^(?:l'|le |la |les |un |une |des |du |de la |de l'|d'|se |s'|en |à )\s*", "", clean)
    clean = remove_accents(clean)
    clean = re.sub(r"\([^)]*\)", "", clean)
    clean = re.sub(r"[^a-z0-9]", "", clean)
    return clean if clean else "zz"

def format_inline_markdown(text):
    if not text:
        return ""
    code_blocks = []
    def save_code(m):
        code_blocks.append(m.group(1))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"

    text = re.sub(r"`([^`]+)`", save_code, text)
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)

    for idx, c in enumerate(code_blocks):
        escaped_c = html.escape(c)
        text = text.replace(f"__CODE_BLOCK_{idx}__", f"<code>{escaped_c}</code>")

    return text

def extract_paren_groups(text):
    synonyms_raw = []
    antonyms_raw = []
    i = 0
    clean_text = []
    while i < len(text):
        if text[i] == '(':
            sub = text[i:]
            is_syn = sub.startswith('(=' ) or sub.startswith('( =')
            is_ant = sub.startswith('(↔' ) or sub.startswith('( ↔')

            if is_syn or is_ant:
                depth = 0
                start = i
                end = -1
                for j in range(i, len(text)):
                    if text[j] == '(':
                        depth += 1
                    elif text[j] == ')':
                        depth -= 1
                        if depth == 0:
                            end = j
                            break
                if end != -1:
                    content = text[start+1:end].strip()
                    if is_syn:
                        content = re.sub(r"^=\s*", "", content)
                        synonyms_raw.append(content)
                    else:
                        content = re.sub(r"^↔\s*", "", content)
                        antonyms_raw.append(content)
                    i = end + 1
                    continue
        clean_text.append(text[i])
        i += 1

    meaning = "".join(clean_text).strip()
    return meaning, synonyms_raw, antonyms_raw

def parse_derivative_or_idiom(line):
    clean = line.replace("&emsp;", "").replace("□", "").replace("◆", "").strip()

    word = ""
    rest = clean
    m_bold = re.match(r"^\s*\*\*([^*]+)\*\*(.*)$", clean)
    if m_bold:
        word = m_bold.group(1).strip()
        rest = m_bold.group(2).strip()
    else:
        m_plain = re.match(r"^\s*([^`/【:]+)(.*)$", clean)
        if m_plain:
            word = m_plain.group(1).strip()
            rest = m_plain.group(2).strip()

    ipa = ""
    m_ipa = re.search(r"(?:`([^`]+)`|/([^/]+)/)", rest)
    if m_ipa:
        ipa = (m_ipa.group(1) or m_ipa.group(2) or "").strip("/ ")
        rest = rest[:m_ipa.start()] + rest[m_ipa.end():]

    pos = ""
    m_pos = re.search(r"【(.*?)】", rest)
    if m_pos:
        pos = m_pos.group(1).strip()
        rest = rest[:m_pos.start()] + rest[m_pos.end():]
    else:
        m_pos2 = re.search(r"\[(.*?)\]", rest)
        if m_pos2 and any(k in m_pos2.group(1) for k in ["名", "形", "動", "副", "他", "自", "前", "間", "熟", "句"]):
            pos = m_pos2.group(1).strip()
            rest = rest[:m_pos2.start()] + rest[m_pos2.end():]

    rest = re.sub(r"^[:\s\-—]+", "", rest).strip()
    return word, ipa, pos, rest

def parse_syn_or_ant_item(raw_item):
    s = raw_item.strip()
    if not s:
        return None

    m_bold = re.match(r"^\s*\*\*([^*]+)\*\*(.*)$", s)
    if m_bold:
        word = m_bold.group(1).strip()
        meaning = m_bold.group(2).strip()
        meaning = re.sub(r"^\[(.*?)\]$", r"\1", meaning).strip()
        return word, meaning

    m_bracket = re.match(r"^([^\[]+)\[(.*?)\]$", s)
    if m_bracket:
        word = m_bracket.group(1).strip()
        meaning = m_bracket.group(2).strip()
        return word, meaning

    m_cjk = re.search(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]", s)
    if m_cjk:
        cjk_pos = m_cjk.start()
        sp_pos = s.rfind(" ", 0, cjk_pos)
        if sp_pos != -1:
            word = s[:sp_pos].strip()
            meaning = s[sp_pos:].strip()
            return word, meaning
        else:
            word = s[:cjk_pos].strip()
            meaning = s[cjk_pos:].strip()
            return word, meaning

    return s, ""

SECTION_SHORT_TITLES = {
    1: "信条・人間関係",
    2: "文学・芸術・学問",
    3: "労働・経済・社会",
    4: "インフラ・環境・法律",
    5: "医療・健康・身体",
    6: "買い物・都市生活",
    7: "議論・説得・論理",
    8: "航空・交通安全",
    9: "家事・料理・生活",
    10: "家庭・トラブル・休息",
    11: "ビジネス・投資・貿易",
    12: "政治・歴史・人道支援",
    13: "学校生活・人間関係",
    14: "学業・論文・研究",
    15: "自然科学・数学・化学",
    16: "恋愛・人生観・自立",
    17: "性格・欠点・人間模様",
    18: "疑惑・口論・仲直り",
    19: "運転・道路・交通事故",
    20: "宇宙・地球環境保護",
    21: "地理・資源・自然災害",
    22: "テクノロジー・IT・革新",
    23: "商業・広告・企業活動",
    24: "仕事・財政・景気動向",
    25: "旅行・空港・手荷物",
    26: "交通・宿泊・外食",
    27: "病気・医療・健康管理",
    28: "教育・大学・就職",
    29: "勇気・成功・逆境克服",
    30: "金銭・適応・求職活動",
    31: "職場・人間関係・面接",
    32: "社会奉仕・選挙・引退",
    33: "政治・権力・機密情報",
    34: "司法・汚職・法廷",
    35: "戦争・テロ・市民権",
    36: "外交・人権・難民支援",
    37: "外交・安保・貿易摩擦",
    38: "犯罪捜査・裁判・刑罰",
    39: "事故・火災・探検",
    40: "歴史・文明・神話・文化",
    41: "社交・マナー・人間関係",
    42: "孤独・適応・日常生活",
    43: "恋愛関係・誤解・家庭",
    44: "失恋・葛藤・新たな一歩",
    45: "人生の節目・死生観",
}

def parse_all_sections():
    sections_data = []
    all_words_index = []
    total_sentences = 0
    total_lemmas = 0

    index_counts = {"headword": 0, "deriv": 0, "idiom": 0, "syn": 0, "ant": 0}

    for sec_num in range(1, 46):
        fname = f"section_{sec_num:02d}.md"
        fpath = os.path.join(SECTIONS_DIR, fname)
        if not os.path.exists(fpath):
            print(f"Warning: {fname} not found!")
            continue

        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        header_match = re.search(r"^#\s*Section\s*(\d+)(?:\s*[—\-–:]\s*(.*?))?$", content, re.MULTILINE)
        sec_title = f"Section {sec_num:02d}"
        sec_subtitle = SECTION_SHORT_TITLES.get(sec_num)
        if not sec_subtitle:
            raw_sub = header_match.group(2).strip() if (header_match and header_match.group(2)) else ""
            sec_subtitle = re.sub(r"\(No\..*?\)", "", raw_sub).strip()

        opus_file = f"section_{sec_num:02d}.opus"
        has_opus = os.path.exists(os.path.join(SECTION_AUDIO_DIR, opus_file))

        sentences_list = []
        blocks = re.split(r"\n(?=###\s+No\.\s*\d+)", content)

        for b in blocks:
            hm = re.search(r"###\s+No\.\s*(\d+)(?:\s*\[(.*?)\])?", b)
            if not hm:
                continue

            sid = hm.group(1).zfill(3)
            cast_str = hm.group(2).strip() if hm.group(2) else ""

            sm = re.search(r">\s*\*\*(.*?)\*\*", b)
            fr_text = sm.group(1).strip() if sm else ""

            jm = re.search(r">\s*\[!NOTE\]\s*(?:\r?\n>\s*)?(.*)", b)
            jp_text = jm.group(1).strip() if jm else ""

            raw_word_blocks = re.split(r"\n(?=-\s+\*\*)", b)
            words_list = []

            for wb in raw_word_blocks[1:]:
                lines = wb.strip().split("\n")
                if not lines:
                    continue

                header_line = lines[0]
                wm = re.match(r"^-\s+\*\*(?:(?:\d+\s*\|\s*)?)([^*]+?)\*\*\s*(?:`([^`]+)`|/([^/]+)/)?\s*(?:【(.*?)】)?\s*(.*)", header_line)
                if not wm:
                    continue

                lemma = wm.group(1).strip()
                raw_ipa = wm.group(2) or wm.group(3) or ""
                ipa = raw_ipa.strip("/ ")
                pos = wm.group(4) or ""
                rest = wm.group(5) or ""

                meaning, syns_raw, ants_raw = extract_paren_groups(rest)

                notes = []
                etymology = []
                derivatives = []
                idioms = []

                for sub in lines[1:]:
                    s = sub.strip()
                    if s.startswith("[") and s.endswith("]"):
                        notes.append(s[1:-1].strip())
                    elif s.startswith("<") and s.endswith(">"):
                        etymology.append(s[1:-1].strip())
                    elif "□" in s:
                        dw, dipa, dpos, dmeaning = parse_derivative_or_idiom(s)
                        if dw:
                            derivatives.append({
                                "word": dw,
                                "ipa": dipa,
                                "pos": dpos,
                                "meaning": dmeaning
                            })
                    elif "◆" in s:
                        iw, iipa, ipos, imeaning = parse_derivative_or_idiom(s)
                        if iw:
                            idioms.append({
                                "word": iw,
                                "ipa": iipa,
                                "pos": ipos or "成句",
                                "meaning": imeaning
                            })

                word_obj = {
                    "lemma": lemma,
                    "ipa": ipa,
                    "pos": pos,
                    "meaning": meaning,
                    "synonyms_raw": syns_raw,
                    "antonyms_raw": ants_raw,
                    "notes": notes,
                    "etymology": etymology,
                    "derivatives": derivatives,
                    "idioms": idioms,
                    "sid": sid,
                    "sec": sec_num
                }
                words_list.append(word_obj)

                # 1. Global Index: Headword
                sort_key = normalize_sort_key(lemma)
                letter = sort_key[0].upper() if sort_key and sort_key[0].isalpha() else "#"
                all_words_index.append({
                    "word": lemma,
                    "type": "headword",
                    "sort_key": sort_key,
                    "letter": letter,
                    "pos": pos,
                    "ipa": ipa,
                    "meaning": meaning,
                    "sid": sid
                })
                index_counts["headword"] += 1

                # 2. Global Index: Synonyms
                for s_str in syns_raw:
                    for p in re.split(r"[,、;；]\s*", s_str):
                        res = parse_syn_or_ant_item(p)
                        if res and res[0] and len(res[0]) > 1:
                            sw, sm = res
                            sk = normalize_sort_key(sw)
                            sletter = sk[0].upper() if sk and sk[0].isalpha() else "#"
                            all_words_index.append({
                                "word": sw,
                                "type": "syn",
                                "sort_key": sk,
                                "letter": sletter,
                                "pos": pos,
                                "ipa": "",
                                "meaning": sm or f"(= {lemma})",
                                "sid": sid
                            })
                            index_counts["syn"] += 1

                # 3. Global Index: Antonyms
                for a_str in ants_raw:
                    for p in re.split(r"[,、;；]\s*", a_str):
                        res = parse_syn_or_ant_item(p)
                        if res and res[0] and len(res[0]) > 1:
                            aw, am = res
                            ak = normalize_sort_key(aw)
                            aletter = ak[0].upper() if ak and ak[0].isalpha() else "#"
                            all_words_index.append({
                                "word": aw,
                                "type": "ant",
                                "sort_key": ak,
                                "letter": aletter,
                                "pos": pos,
                                "ipa": "",
                                "meaning": am or f"(↔ {lemma})",
                                "sid": sid
                            })
                            index_counts["ant"] += 1

                # 4. Global Index: Derivatives
                for d in derivatives:
                    dw = d["word"]
                    dk = normalize_sort_key(dw)
                    dletter = dk[0].upper() if dk and dk[0].isalpha() else "#"
                    all_words_index.append({
                        "word": dw,
                        "type": "deriv",
                        "sort_key": dk,
                        "letter": dletter,
                        "pos": d["pos"] or pos,
                        "ipa": d["ipa"],
                        "meaning": d["meaning"],
                        "sid": sid
                    })
                    index_counts["deriv"] += 1

                # 5. Global Index: Idioms
                for i in idioms:
                    iw = i["word"]
                    ik = normalize_sort_key(iw)
                    iletter = ik[0].upper() if ik and ik[0].isalpha() else "#"
                    all_words_index.append({
                        "word": iw,
                        "type": "idiom",
                        "sort_key": ik,
                        "letter": iletter,
                        "pos": i["pos"],
                        "ipa": i["ipa"],
                        "meaning": i["meaning"],
                        "sid": sid
                    })
                    index_counts["idiom"] += 1

            mp3_file = f"sentence_{sid}.mp3"
            has_mp3 = os.path.exists(os.path.join(AUDIO_DIR, mp3_file))

            sentences_list.append({
                "id": sid,
                "cast": cast_str,
                "fr": fr_text,
                "jp": jp_text,
                "has_mp3": has_mp3,
                "words": words_list
            })
            total_sentences += 1
            total_lemmas += len(words_list)

        sections_data.append({
            "num": sec_num,
            "title": sec_title,
            "subtitle": sec_subtitle,
            "has_opus": has_opus,
            "opus_file": opus_file,
            "sentences": sentences_list
        })

    all_words_index.sort(key=lambda x: (x["sort_key"], x["word"]))
    print(f"Index Statistics: {index_counts}")
    return sections_data, all_words_index, index_counts, total_sentences, total_lemmas

def get_pos_class(pos_str):
    p = pos_str.lower()
    if any(k in p for k in ["女", "n.f.", "fem"]):
        return "pos-f"
    elif any(k in p for k in ["男", "n.m.", "masc"]):
        return "pos-m"
    elif any(k in p for k in ["他", "自", "動", "v."]):
        return "pos-v"
    elif any(k in p for k in ["形", "adj"]):
        return "pos-adj"
    elif any(k in p for k in ["副", "adv"]):
        return "pos-adv"
    elif any(k in p for k in ["熟", "句", "成句", "loc"]):
        return "pos-expr"
    return "pos-other"

def get_actor_class(cast_str):
    if "&" in cast_str:
        return "cast-duet"
    elif "♀" in cast_str or "Vivienne" in cast_str or "Denise" in cast_str:
        return "cast-female"
    return "cast-male"

def generate_html(sections_data, all_words_index, index_counts, total_sentences, total_lemmas):
    daily_themes = load_daily_vocab_data()
    compact_index_data = [
        [
            w["word"],
            w["type"],
            w["pos"],
            re.sub(r"<[^>]+>", "", format_inline_markdown(w["meaning"])),
            w["sid"],
            w["letter"]
        ]
        for w in all_words_index
    ]
    compact_index_data.extend(get_daily_index_entries(daily_themes))
    compact_index_data.sort(key=lambda x: (x[5] if x[5] != '#' else 'Z~', x[0].lower()))
    json_index_str = json.dumps(compact_index_data, ensure_ascii=False, separators=(',', ':'))

    all_letters = sorted(list(set(w["letter"] for w in all_words_index if w["letter"] != "#")))
    if any(w["letter"] == "#" for w in all_words_index):
        all_letters.append("#")

    html_out = []
    html_out.append(f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>DUO Français 3.0 — 完全製品版 フランス語総合学習システム</title>
  <meta name="description" content="全45セクション・560例文・2,221見出し語・巻末11,458総合索引。本家DUO 3.0と完全合致するフランス語版学習Webアプリケーション。">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Noto+Sans+JP:wght@400;500;700;900&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">

  <style>
    :root {{
      --primary: #3b82f6;
      --primary-light: #60a5fa;
      --primary-bg: #f1f5fa;
      --navy-dark: #1e293b;
      --text-main: #334155;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --border-dark: #cbd5e1;
      --bg-page: #f8fafc;
      --bg-card: #ffffff;
      
      --accent-star: #eab308;
      --mask-bg: #e2e8f0;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: 'Noto Sans JP', sans-serif;
      background-color: var(--bg-page);
      color: var(--text-main);
      line-height: 1.6;
      padding-bottom: 110px;
    }}

    code {{
      font-family: 'JetBrains Mono', Consolas, monospace;
      background: #f1f5f9;
      color: #334155;
      padding: 0.1rem 0.35rem;
      border-radius: 3px;
      font-size: 0.88em;
      border: 1px solid #e2e8f0;
    }}

    strong {{
      font-weight: 700;
      color: #0f172a;
    }}

    em {{
      font-style: italic;
      font-family: 'Source Serif 4', Georgia, serif;
    }}

    /* ==========================================================================
       HEADER & NAVIGATION (SOFT MUTED SLATE THEME)
       ========================================================================== */
    header {{
      background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
      color: white;
      padding: 0.75rem 1.5rem;
      position: sticky;
      top: 0;
      z-index: 500;
      box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }}
    .header-inner {{
      max-width: 1300px;
      margin: 0 auto;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 0.8rem;
    }}
    .logo-group {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      cursor: pointer;
    }}
    .tricolor-flag {{
      display: flex;
      width: 22px;
      height: 16px;
      border-radius: 2px;
      overflow: hidden;
      box-shadow: 0 1px 3px rgba(0,0,0,0.25);
    }}
    .flag-b {{ width: 33.3%; background: #2563eb; }}
    .flag-w {{ width: 33.3%; background: #ffffff; }}
    .flag-r {{ width: 33.3%; background: #ef4444; }}

    .logo-group h1 {{
      font-family: 'Cinzel', serif;
      font-size: 1.4rem;
      font-weight: 800;
      letter-spacing: 0.05em;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      color: #ffffff;
    }}
    .badge-pro {{
      background: #fee2e2;
      color: #dc2626;
      border: 1px solid #fca5a5;
      font-size: 0.65rem;
      padding: 0.12rem 0.45rem;
      border-radius: 3px;
      font-weight: 700;
      font-family: sans-serif;
      letter-spacing: 0.05em;
    }}
    .sub-stats {{
      font-size: 0.75rem;
      color: #cbd5e1;
      font-weight: 500;
    }}

    /* Controls Bar */
    .header-controls {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.5rem;
    }}
    .nav-btn {{
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #f1f5f9;
      padding: 0.38rem 0.7rem;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.78rem;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.2s;
      user-select: none;
    }}
    .nav-btn:hover {{
      background: rgba(255, 255, 255, 0.18);
      border-color: rgba(255, 255, 255, 0.35);
      transform: translateY(-1px);
    }}
    .nav-btn.active {{
      background: #38bdf8;
      color: #0f172a;
      border-color: #38bdf8;
      font-weight: 700;
    }}
    .nav-btn.star-active {{
      background: #fef08a;
      color: #854d0e;
      border-color: #facc15;
    }}

    /* Search Box */
    .search-wrapper {{
      position: relative;
      display: flex;
      align-items: center;
    }}
    .search-input {{
      background: rgba(255, 255, 255, 0.12);
      border: 1px solid rgba(255, 255, 255, 0.25);
      color: white;
      padding: 0.38rem 2rem 0.38rem 0.75rem;
      border-radius: 20px;
      font-size: 0.8rem;
      outline: none;
      width: 175px;
      transition: all 0.25s ease;
    }}
    .search-input::placeholder {{ color: #94a3b8; }}
    .search-input:focus {{
      background: white;
      color: #0f172a;
      width: 250px;
      border-color: #93c5fd;
      box-shadow: 0 0 10px rgba(147, 197, 253, 0.4);
    }}
    .search-clear {{
      position: absolute;
      right: 8px;
      color: #94a3b8;
      cursor: pointer;
      display: none;
      font-size: 0.9rem;
      line-height: 1;
    }}

    /* Sub Toolbar */
    .sub-strip {{
      background: #ffffff;
      border-bottom: 1px solid var(--border);
      padding: 0.5rem 1.5rem;
      font-size: 0.78rem;
      position: sticky;
      top: 55px;
      z-index: 400;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }}
    .sub-strip-inner {{
      max-width: 1300px;
      margin: 0 auto;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 0.8rem;
    }}
    .tool-group {{
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}
    .tool-label {{
      color: var(--text-muted);
      font-weight: 700;
      margin-right: 0.3rem;
      font-size: 0.73rem;
    }}
    .tool-btn {{
      background: #f8fafc;
      border: 1px solid var(--border);
      color: var(--text-main);
      padding: 0.25rem 0.55rem;
      border-radius: 5px;
      cursor: pointer;
      font-size: 0.74rem;
      font-weight: 600;
      transition: all 0.15s;
    }}
    .tool-btn:hover {{ background: #f1f5f9; }}
    .tool-btn.active {{
      background: #fee2e2;
      color: #dc2626;
      border-color: #fca5a5;
      font-weight: 700;
    }}

    /* Memorization Masks */
    body.mask-jp .japanese-translation {{
      filter: blur(5px);
      user-select: none;
      background: var(--mask-bg) !important;
      color: transparent !important;
    }}
    body.mask-jp .japanese-translation:hover {{
      filter: none;
      color: inherit !important;
      background: transparent !important;
    }}

    body.mask-meaning .meaning,
    body.mask-meaning .word-note,
    body.mask-meaning .word-etym,
    body.mask-meaning .rel-meaning,
    body.mask-meaning .syn-content,
    body.mask-meaning .ant-content {{
      filter: blur(5px);
      user-select: none;
    }}
    body.mask-meaning .word-row:hover .meaning,
    body.mask-meaning .word-row:hover .word-note,
    body.mask-meaning .word-row:hover .word-etym,
    body.mask-meaning .word-row:hover .rel-meaning,
    body.mask-meaning .word-row:hover .syn-content,
    body.mask-meaning .word-row:hover .ant-content {{
      filter: none;
    }}

    body.mask-cloze .word-token {{
      background: #e2e8f0;
      color: transparent;
      border-radius: 3px;
      padding: 0 4px;
      user-select: none;
      border-bottom: 2px solid #93c5fd;
    }}
    body.mask-cloze .word-token:hover {{
      background: transparent;
      color: inherit;
    }}

    /* Gender Highlights */
    body.highlight-gender .pos-m {{
      box-shadow: 0 0 0 2px #60a5fa;
      background-color: #dbeafe;
    }}
    body.highlight-gender .pos-f {{
      box-shadow: 0 0 0 2px #f472b6;
      background-color: #fce7f3;
    }}

    /* ==========================================================================
       MAIN CONTENT CONTAINER
       ========================================================================== */
    main {{
      max-width: 1300px;
      margin: 1.8rem auto;
      padding: 0 1.25rem;
    }}

    .section-container {{
      margin-bottom: 3.5rem;
      scroll-margin-top: 120px;
      content-visibility: auto;
      contain-intrinsic-size: 0 1500px;
    }}

    .section-banner {{
      background: white;
      border: 1px solid var(--border);
      border-left: 5px solid #93c5fd;
      padding: 1rem 1.5rem;
      border-radius: 8px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.03);
      margin-bottom: 1.75rem;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
    }}
    .section-title-wrap h2 {{
      font-family: 'Cinzel', serif;
      font-size: 1.35rem;
      font-weight: 700;
      color: #1e3a8a;
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }}
    .section-sub-theme {{
      font-size: 0.86rem;
      color: var(--text-muted);
      margin-top: 0.2rem;
      font-weight: 500;
    }}
    .section-actions {{
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }}
    .btn-section-opus {{
      background: #ecfdf5;
      color: #047857;
      border: 1px solid #a7f3d0;
      padding: 0.45rem 0.85rem;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.2s;
    }}
    .btn-section-opus:hover {{
      background: #d1fae5;
      border-color: #6ee7b7;
      transform: translateY(-1px);
    }}
    .btn-section-opus.playing {{
      background: #fee2e2;
      color: #dc2626;
      border-color: #fca5a5;
      animation: pulse-btn 1.4s infinite;
    }}
    @keyframes pulse-btn {{
      0% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.3); }}
      70% {{ box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }}
      100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
    }}

    /* ==========================================================================
       DUO AUTHENTIC SPREAD CARD (SOFT PASTEL PALETTE)
       ========================================================================== */
    .duo-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      margin-bottom: 2.2rem;
      box-shadow: 0 2px 12px rgba(0,0,0,0.03);
      overflow: hidden;
      transition: all 0.25s ease;
      scroll-margin-top: 130px;
      content-visibility: auto;
      contain-intrinsic-size: 0 350px;
    }}
    .duo-card:hover {{
      box-shadow: 0 6px 20px rgba(0,0,0,0.06);
      border-color: #cbd5e1;
    }}
    .duo-card.active-playback {{
      border: 2px solid #60a5fa;
      box-shadow: 0 0 20px rgba(96, 165, 250, 0.25);
      transform: scale(1.004);
    }}
    .duo-card.is-starred {{
      border-left: 5px solid #facc15;
    }}
    .duo-card.highlight-pulse {{
      animation: cardPulse 1.8s ease;
    }}
    @keyframes cardPulse {{
      0% {{ box-shadow: 0 0 0 0 rgba(96, 165, 250, 0.6); }}
      50% {{ box-shadow: 0 0 0 10px rgba(96, 165, 250, 0); }}
      100% {{ box-shadow: 0 2px 12px rgba(0,0,0,0.03); }}
    }}

    /* 1. TOP: French Sentence Header (ソフトなペールブルー背景) */
    .sentence-header {{
      background: #f1f5fa;
      border-left: 5px solid #93c5fd;
      border-bottom: 1px solid #e2e8f0;
      padding: 1.15rem 1.6rem;
      display: flex;
      gap: 1.2rem;
      align-items: flex-start;
      position: relative;
    }}
    .sentence-badge-col {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 0.4rem;
      min-width: 52px;
    }}
    .sentence-number {{
      font-family: 'Cinzel', serif;
      font-size: 1.15rem;
      font-weight: 800;
      color: #2563eb;
      background: white;
      border: 1px solid #bfdbfe;
      text-align: center;
      padding: 0.2rem 0.45rem;
      border-radius: 6px;
      line-height: 1;
      width: 100%;
    }}
    .btn-star {{
      background: none;
      border: none;
      color: #94a3b8;
      cursor: pointer;
      font-size: 1.2rem;
      line-height: 1;
      transition: all 0.2s;
    }}
    .btn-star:hover {{
      color: #eab308;
      transform: scale(1.2);
    }}
    .btn-star.starred {{
      color: #eab308;
    }}

    .sentence-main-col {{
      flex: 1;
    }}
    .meta-tags {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin-bottom: 0.35rem;
    }}
    .cast-pill {{
      font-size: 0.72rem;
      font-weight: 700;
      padding: 0.12rem 0.45rem;
      border-radius: 4px;
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
    }}
    .cast-male {{
      background: #eff6ff;
      color: #2563eb;
      border: 1px solid #dbeafe;
    }}
    .cast-female {{
      background: #fdf2f8;
      color: #db2777;
      border: 1px solid #fce7f3;
    }}
    .cast-duet {{
      background: #f5f3ff;
      color: #7c3aed;
      border: 1px solid #ede9fe;
    }}

    .french-sentence {{
      font-family: 'Source Serif 4', Georgia, serif;
      font-size: 1.36rem;
      font-weight: 600;
      color: #0f172a;
      line-height: 1.5;
      letter-spacing: 0.01em;
    }}

    .sentence-audio-col {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 0.35rem;
    }}
    .btn-play-single {{
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 50%;
      width: 42px;
      height: 42px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: #2563eb;
      transition: all 0.2s;
      box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }}
    .btn-play-single:hover {{
      background: #eff6ff;
      border-color: #93c5fd;
      transform: scale(1.06);
      color: #1d4ed8;
    }}
    .btn-play-single.playing {{
      background: #fee2e2;
      color: #dc2626;
      border-color: #fca5a5;
      box-shadow: 0 0 10px rgba(239,68,68,0.3);
    }}

    /* 2. MIDDLE: Classic 2-Column Vocabulary Table (見出し語左、日本語右) */
    .words-table {{
      display: flex;
      flex-direction: column;
      background: white;
    }}
    .word-row {{
      display: flex;
      border-bottom: 1px solid #f1f5f9;
      padding: 1.1rem 1.6rem;
      gap: 1.8rem;
      align-items: flex-start;
      transition: background 0.15s;
    }}
    .word-row:last-child {{
      border-bottom: none;
    }}
    .word-row:hover {{
      background: #fafcff;
    }}

    /* Left Column: Headword + IPA + Checkbox */
    .word-left-col {{
      flex: 0 0 220px;
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
      border-right: 1px dashed #e2e8f0;
      padding-right: 1.4rem;
    }}
    .word-head-line {{
      display: flex;
      align-items: baseline;
      gap: 0.45rem;
    }}
    .word-checkbox {{
      color: #94a3b8;
      font-size: 0.95rem;
      user-select: none;
      flex-shrink: 0;
    }}
    .lemma-title {{
      font-size: 1.16rem;
      font-weight: 700;
      color: #0f172a;
      letter-spacing: 0.01em;
      word-break: break-word;
    }}
    .phonetic-ipa {{
      font-family: 'Source Serif 4', serif;
      font-size: 0.88rem;
      color: #64748b;
      padding-left: 1.35rem;
    }}

    /* Right Column: POS, Meaning, Synonyms, Antonyms, Notes, Derivatives */
    .word-right-col {{
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
      min-width: 0;
    }}
    .word-meaning-line {{
      display: flex;
      flex-wrap: wrap;
      align-items: baseline;
      gap: 0.5rem;
    }}

    /* SOFT PASTEL POS BADGES (優しいパステル配色) */
    .pos-pill {{
      font-size: 0.72rem;
      font-weight: 700;
      padding: 0.12rem 0.45rem;
      border-radius: 4px;
      border: 1px solid transparent;
      flex-shrink: 0;
    }}
    .pos-m {{
      background-color: #eff6ff;
      color: #1d4ed8;
      border-color: #bfdbfe;
    }}
    .pos-f {{
      background-color: #fdf2f8;
      color: #be185d;
      border-color: #fbcfe8;
    }}
    .pos-v {{
      background-color: #f0fdf4;
      color: #15803d;
      border-color: #bbf7d0;
    }}
    .pos-adj {{
      background-color: #faf5ff;
      color: #7e22ce;
      border-color: #e9d5ff;
    }}
    .pos-adv {{
      background-color: #f8fafc;
      color: #475569;
      border-color: #cbd5e1;
    }}
    .pos-expr {{
      background-color: #fffbeb;
      color: #b45309;
      border-color: #fde68a;
    }}
    .pos-other {{
      background-color: #f3f4f6;
      color: #4b5563;
      border-color: #e5e7eb;
    }}

    .meaning {{
      font-size: 0.95rem;
      font-weight: 600;
      color: #1e293b;
      line-height: 1.5;
    }}

    /* Synonyms & Antonyms (Monochrome / Paper DUO style) */
    .word-synonyms, .word-antonyms {{
      font-size: 0.83rem;
      line-height: 1.45;
      display: flex;
      align-items: baseline;
      gap: 0.45rem;
      margin-top: 0.15rem;
      color: #334155;
    }}
    .syn-badge, .ant-badge {{
      background: transparent;
      color: #475569;
      border: none;
      padding: 0;
      font-weight: 700;
      font-size: 0.85rem;
      white-space: nowrap;
      flex-shrink: 0;
      line-height: 1;
    }}
    .syn-content, .ant-content {{
      color: #1e293b;
    }}

    .word-note {{
      font-size: 0.82rem;
      color: #0369a1;
      background: #f0f9ff;
      border-left: 3px solid #38bdf8;
      padding: 0.3rem 0.6rem;
      border-radius: 0 4px 4px 0;
      line-height: 1.45;
      margin-top: 0.15rem;
    }}
    .word-etym {{
      font-size: 0.8rem;
      color: #92400e;
      background: #fffbeb;
      border-left: 3px solid #fcd34d;
      padding: 0.25rem 0.55rem;
      border-radius: 0 4px 4px 0;
      line-height: 1.45;
      margin-top: 0.15rem;
    }}
    .word-rel-list {{
      margin-top: 0.35rem;
      font-size: 0.82rem;
      color: var(--text-muted);
      line-height: 1.5;
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }}
    .rel-item {{
      display: flex;
      flex-wrap: wrap;
      align-items: baseline;
      gap: 0.35rem;
    }}
    .rel-icon {{ font-weight: 700; font-size: 0.75rem; }}
    .rel-icon.deriv {{ color: #64748b; }}
    .rel-icon.idiom {{ color: #d97706; }}
    .rel-word {{ font-weight: 700; color: #1e293b; }}
    .rel-meaning {{ color: #475569; }}

    /* 3. BOTTOM: Separated Japanese Translation Box (落ち着いた枠線ボックス) */
    .card-translation-box {{
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
      padding: 0.85rem 1.6rem;
      display: flex;
      align-items: baseline;
      gap: 0.85rem;
    }}
    .translation-tag {{
      font-size: 0.72rem;
      font-weight: 700;
      color: #64748b;
      background: white;
      border: 1px solid #cbd5e1;
      padding: 0.15rem 0.5rem;
      border-radius: 4px;
      flex-shrink: 0;
      letter-spacing: 0.05em;
    }}
    .japanese-translation {{
      font-size: 0.96rem;
      color: #1e293b;
      font-weight: 500;
      line-height: 1.55;
      flex: 1;
    }}

    /* ==========================================================================
       MODALS & DRAWERS (SOFT THEME)
       ========================================================================== */
    .modal-overlay {{
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(15, 23, 42, 0.55);
      backdrop-filter: blur(4px);
      z-index: 1000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
      animation: fadeIn 0.2s ease;
    }}
    .modal-overlay.open {{ display: flex; }}
    @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}

    .modal-card {{
      background: white;
      border-radius: 12px;
      width: 100%;
      max-width: 960px;
      max-height: 88vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 16px 36px rgba(0,0,0,0.18);
      overflow: hidden;
    }}
    .modal-header {{
      background: #1e293b;
      color: white;
      padding: 1rem 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .modal-header h3 {{
      font-family: 'Cinzel', serif;
      font-size: 1.2rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .modal-close {{
      background: none;
      border: none;
      color: #94a3b8;
      font-size: 1.5rem;
      cursor: pointer;
      line-height: 1;
      padding: 0.2rem;
    }}
    .modal-close:hover {{ color: white; }}

    .modal-body {{
      padding: 1.25rem 1.5rem;
      overflow-y: auto;
      flex: 1;
    }}

    /* Section Drawer Content */
    .sections-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 0.85rem;
    }}
    .sec-jump-card {{
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.75rem 1rem;
      cursor: pointer;
      transition: all 0.2s;
      background: #f8fafc;
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }}
    .sec-jump-card:hover {{
      background: #eff6ff;
      border-color: #93c5fd;
      transform: translateY(-2px);
    }}
    .sec-jump-num {{
      font-family: 'Cinzel', serif;
      font-size: 0.9rem;
      font-weight: 800;
      color: #2563eb;
    }}
    .sec-jump-sub {{
      font-size: 0.75rem;
      color: var(--text-muted);
      line-height: 1.35;
    }}

    """ + generate_app_ui_css(is_mobile=False) + generate_daily_css() + """</style>
</head>
<body>

  <!-- HEADER -->
  <header>
    <div class="header-inner">
      <div class="logo-group" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">
        <div class="tricolor-flag">
          <div class="flag-b"></div>
          <div class="flag-w"></div>
          <div class="flag-r"></div>
        </div>
        <div>
          <h1>DUO Français <span class="badge-pro">PRO 3.0</span></h1>
          <div class="sub-stats">全45セクション・560例文・2,221見出し語・巻末{len(all_words_index):,}総合語彙</div>
        </div>
      </div>

      <div class="header-controls">
        <div class="search-wrapper">
          <input type="text" id="global-search" class="search-input" placeholder="🔍 単語・日本語・例文検索...">
          <span id="search-clear-btn" class="search-clear">×</span>
        </div>
        <button id="btn-open-sections" class="nav-btn">📑 セクション目次</button>
        <button id="btn-open-index" class="nav-btn">📖 A-Z 巻末索引 ({len(all_words_index):,})</button>
        <button id="btn-filter-star" class="nav-btn">⭐ 要復習 (<span id="star-count">0</span>)</button>
        <a href="mobile.html" class="nav-btn" style="text-decoration:none;">📱 スマホ版</a>
      </div>
    </div>
  </header>

  <!-- SUB-STRIP: STUDY TOOLS -->
  <div class="sub-strip">
    <div class="sub-strip-inner">
      <div class="tool-group">
        <span class="tool-label">暗記マスク (赤シート):</span>
        <button id="tool-mask-jp" class="tool-btn">🇯🇵 日本語訳隠し</button>
        <button id="tool-mask-meaning" class="tool-btn">📖 単語の意味隠し</button>
        <button id="tool-mask-cloze" class="tool-btn">✏️ 穴埋めテスト</button>
      </div>
      <div class="tool-group">
        <span class="tool-label">視覚サポート:</span>
        <button id="tool-highlight-gender" class="tool-btn">🚻 名詞の性強調</button>
      </div>
    </div>
  </div>

  <!-- MAIN SPREAD CONTAINER -->
  <main id="main-content">
""")

    # Render all 45 sections
    for sec in sections_data:
        sec_num = sec["num"]
        sec_title = sec["title"]
        sec_subtitle = sec["subtitle"]
        has_opus = sec["has_opus"]

        html_out.append(f"""
    <!-- SECTION {sec_num:02d} -->
    <section class="section-container" id="section-{sec_num:02d}" data-sec="{sec_num}">
      <div class="section-banner">
        <div class="section-title-wrap">
          <h2>Section {sec_num:02d}</h2>
          <div class="section-sub-theme">{sec_subtitle}</div>
        </div>
        <div class="section-actions">
          {f'<button class="btn-section-opus" data-opus="audio_sections/{sec["opus_file"]}" data-sec="{sec_num}">▶ セクション通し再生 (OPUS)</button>' if has_opus else ''}
        </div>
      </div>
      <div class="sentences-list">
""")

        for s in sec["sentences"]:
            sid = s["id"]
            cast_str = s["cast"]
            actor_cls = get_actor_class(cast_str)
            fr_text = s["fr"]
            jp_text = s["jp"]

            cloze_text = re.sub(r"\b([A-Za-zÀ-ÿ\-']+)\b", r'<span class="word-token">\1</span>', fr_text)

            html_out.append(f"""
        <!-- CARD No. {sid} -->
        <article class="duo-card" id="card-{sid}" data-id="{sid}" data-sec="{sec_num}">
          <!-- 1. TOP: French Sentence (仏文エリア) -->
          <div class="sentence-header">
            <div class="sentence-badge-col">
              <div class="sentence-number">{sid}</div>
              <button class="btn-star" data-id="{sid}" title="要復習ブックマーク">☆</button>
            </div>
            <div class="sentence-main-col">
              <div class="meta-tags">
                <span class="cast-pill {actor_cls}">{cast_str}</span>
              </div>
              <div class="french-sentence">{cloze_text}</div>
            </div>
            <div class="sentence-audio-col">
              <button class="btn-play-single" data-mp3="audio/sentence_{sid}.mp3" data-id="{sid}" title="音声を再生">▶</button>
            </div>
          </div>
          
          <!-- 2. MIDDLE: Classic 2-Column Vocabulary Table (見出し語左、日本語右) -->
          <div class="words-table">
""")

            for w in s["words"]:
                lemma = w["lemma"]
                ipa = w["ipa"]
                pos = w["pos"]
                pos_cls = get_pos_class(pos)
                meaning = w["meaning"]
                syns_raw = w["synonyms_raw"]
                ants_raw = w["antonyms_raw"]
                notes = w["notes"]
                etym = w["etymology"]
                derivs = w["derivatives"]
                idioms = w["idioms"]

                search_kw = [lemma, meaning]
                for sr in syns_raw: search_kw.append(sr)
                for ar in ants_raw: search_kw.append(ar)
                for d in derivs: search_kw.append(f"{d['word']} {d['meaning']}")
                for i in idioms: search_kw.append(f"{i['word']} {i['meaning']}")
                search_attr = html.escape(" ".join(search_kw).lower())

                syn_html = ""
                if syns_raw:
                    formatted_syns = format_inline_markdown(", ".join(syns_raw))
                    syn_html = f'<div class="word-synonyms"><span class="syn-badge">＝</span> <span class="syn-content">{formatted_syns}</span></div>'

                ant_html = ""
                if ants_raw:
                    formatted_ants = format_inline_markdown(", ".join(ants_raw))
                    ant_html = f'<div class="word-antonyms"><span class="ant-badge">⇔</span> <span class="ant-content">{formatted_ants}</span></div>'

                notes_html = "".join([f'<div class="word-note">💡 {format_inline_markdown(n)}</div>' for n in notes])
                etym_html = "".join([f'<div class="word-etym">🏛️ {format_inline_markdown(e)}</div>' for e in etym])

                rel_items = []
                for d in derivs:
                    dw = format_inline_markdown(d["word"])
                    dipa = f'<span class="phonetic-ipa">/{d["ipa"]}/</span>' if d["ipa"] else ""
                    dpos = f'<span class="pos-pill {get_pos_class(d["pos"])}">{d["pos"]}</span>' if d["pos"] else ""
                    dm = format_inline_markdown(d["meaning"])
                    rel_items.append(f'<div class="rel-item"><span class="rel-icon deriv">□</span> <strong class="rel-word">{dw}</strong> {dipa} {dpos} <span class="rel-meaning">{dm}</span></div>')

                for i in idioms:
                    iw = format_inline_markdown(i["word"])
                    iipa = f'<span class="phonetic-ipa">/{i["ipa"]}/</span>' if i["ipa"] else ""
                    ipos = f'<span class="pos-pill pos-expr">{i["pos"]}</span>' if i["pos"] else ""
                    im = format_inline_markdown(i["meaning"])
                    rel_items.append(f'<div class="rel-item"><span class="rel-icon idiom">◆</span> <strong class="rel-word">{iw}</strong> {iipa} {ipos} <span class="rel-meaning">{im}</span></div>')

                rel_list_html = f'<div class="word-rel-list">{"".join(rel_items)}</div>' if rel_items else ""

                html_out.append(f"""
            <!-- Word Entry -->
            <div class="word-row" data-lemma="{html.escape(lemma.lower())}" data-search="{search_attr}">
              <div class="word-left-col">
                <div class="word-head-line">
                  <span class="word-checkbox">□</span>
                  <span class="lemma-title">{lemma}</span>
                </div>
                {f'<div class="phonetic-ipa">/{ipa}/</div>' if ipa else ''}
              </div>
              <div class="word-right-col">
                <div class="word-meaning-line">
                  {f'<span class="pos-pill {pos_cls}">{pos}</span>' if pos else ''}
                  <span class="meaning">{format_inline_markdown(meaning)}</span>
                </div>
                {syn_html}
                {ant_html}
                {notes_html}
                {etym_html}
                {rel_list_html}
              </div>
            </div>
""")

            html_out.append(f"""
          </div>
          
          <!-- 3. BOTTOM: Separated Japanese Translation Box (和訳エリア) -->
          {f'''<div class="card-translation-box">
            <span class="translation-tag">和訳</span>
            <div class="japanese-translation">{jp_text}</div>
          </div>''' if jp_text else ''}
        </article>
""")

        html_out.append("""
      </div>
    </section>
""")

    # Append Everyday Vocabulary Themes (THEME 01 - 08, 336 words)
    html_out.append(generate_daily_sections_html(daily_themes, is_mobile=False))

    html_out.append(f"""
  </main>

  <!-- MODAL: SECTION DRAWER -->
  <div id="modal-sections" class="modal-overlay">
    <div class="modal-card">
      <div class="modal-header">
        <h3>📑 全45セクション目次</h3>
        <button class="modal-close" data-close="modal-sections">×</button>
      </div>
      <div class="modal-body">
        <div class="sections-grid">
""")

    for sec in sections_data:
        first_sid = sec["sentences"][0]["id"] if sec["sentences"] else "001"
        html_out.append(f"""
          <div class="sec-jump-card" data-jump="section-{sec['num']:02d}">
            <div class="sec-jump-num">Section {sec['num']:02d} (No.{first_sid}〜)</div>
            <div class="sec-jump-sub">{sec['subtitle']}</div>
          </div>
""")

    html_out.append(f"""
        </div>
        """ + generate_daily_toc_html(daily_themes) + f"""
      </div>
    </div>
  </div>

  <!-- MODAL: A-Z COMPREHENSIVE INDEX (ULTRA-FAST ON-DEMAND RENDERING) -->
  <div id="modal-index" class="modal-overlay">
    <div class="modal-card">
      <div class="modal-header">
        <h3>📖 A-Z 巻末総合単語索引 (全{len(all_words_index):,}項目)</h3>
        <button class="modal-close" data-close="modal-index">×</button>
      </div>
      <div class="modal-body">
        <div class="index-toolbar">
          <div class="index-search-row">
            <input type="text" id="az-search-input" class="az-search-input" placeholder="🔍 索引内クイック検索 (例: respect, 尊重, etc.)...">
          </div>
          <div class="az-type-filters">
            <button class="az-type-btn active" data-type="all">すべて ({len(all_words_index):,})</button>
            <button class="az-type-btn" data-type="headword">見出し語 ({index_counts['headword']:,})</button>
            <button class="az-type-btn" data-type="deriv">派生語 ({index_counts['deriv']:,})</button>
            <button class="az-type-btn" data-type="idiom">成句 ({index_counts['idiom']:,})</button>
            <button class="az-type-btn" data-type="syn">同意語 ({index_counts['syn']:,})</button>
            <button class="az-type-btn" data-type="ant">反意語 ({index_counts['ant']:,})</button>
            <button class="az-type-btn" data-type="日常">日常語 ({len(get_daily_index_entries(daily_themes)):,})</button>
          </div>
          <div class="az-nav-tabs">
""")

    for letter in all_letters:
        active_cls = ' active' if letter == 'A' else ''
        html_out.append(f'<button class="az-tab{active_cls}" data-letter="{letter}">{letter}</button>')

    html_out.append("""
          </div>
        </div>
        
        <div class="index-content-wrap">
          <div id="az-status-bar" class="index-status-bar"></div>
          <div id="az-words-container" class="index-words-list"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- FLOATING AUDIO DOCK -->
  <div class="player-dock" id="player-dock">
    <div class="dock-now-playing">
      <div id="dock-indicator" class="dock-indicator"></div>
      <div>
        <div id="dock-title" class="dock-info-title">再生待機中</div>
        <div id="dock-sub" class="dock-info-sub">カードの ▶ を押すと個別の文を再生します</div>
      </div>
    </div>

    <div class="dock-controls">
      <button id="dock-prev-btn" class="dock-btn" title="前の文へ">⏮</button>
      <button id="dock-play-btn" class="dock-btn main-play" title="再生 / 一時停止">▶</button>
      <button id="dock-next-btn" class="dock-btn" title="次の文へ">⏭</button>
    </div>

    <div class="dock-settings">
      <select id="dock-repeat" class="dock-select" title="リピートモード">
        <option value="1">1回再生</option>
        <option value="3">3回リピート (シャドーイング)</option>
        <option value="loop">エンドレスリピート</option>
        <option value="seq">連続自動送り再生</option>
      </select>
      <select id="dock-speed" class="dock-select" title="再生速度">
        <option value="0.75">0.75x</option>
        <option value="0.9">0.9x</option>
        <option value="1.0" selected>1.0x (標準)</option>
        <option value="1.1">1.1x</option>
        <option value="1.25">1.25x</option>
        <option value="1.5">1.5x</option>
      </select>
    </div>
  </div>

  <!-- EMBEDDED AUDIO ELEMENT -->
  <audio id="audio-engine" preload="none"></audio>

  <!-- COMPACT JSON INDEX DATA -->
  <script>
    const INDEX_DATA = """)

    html_out.append(json_index_str)

    html_out.append(""";

    (function() {
      const audio = document.getElementById('audio-engine');
      const dockTitle = document.getElementById('dock-title');
      const dockSub = document.getElementById('dock-sub');
      const dockIndicator = document.getElementById('dock-indicator');
      const dockPlayBtn = document.getElementById('dock-play-btn');
      const dockPrevBtn = document.getElementById('dock-prev-btn');
      const dockNextBtn = document.getElementById('dock-next-btn');
      const dockSpeed = document.getElementById('dock-speed');
      const dockRepeat = document.getElementById('dock-repeat');

      let currentSentenceId = null;
      let currentSectionNum = null;
      let isPlaying = false;
      let repeatCountRemaining = 0;
      let currentMode = 'single';

      // Star Bookmarks
      let starredIds = new Set(JSON.parse(localStorage.getItem('duo_starred') || '[]'));
      const starCountEl = document.getElementById('star-count');
      function updateStarUI() {
        starCountEl.textContent = starredIds.size;
        document.querySelectorAll('.btn-star').forEach(btn => {
          const sid = btn.dataset.id;
          const card = document.getElementById(`card-${sid}`);
          if (starredIds.has(sid)) {
            btn.textContent = '★';
            btn.classList.add('starred');
            if (card) card.classList.add('is-starred');
          } else {
            btn.textContent = '☆';
            btn.classList.remove('starred');
            if (card) card.classList.remove('is-starred');
          }
        });
        localStorage.setItem('duo_starred', JSON.stringify([...starredIds]));
      }

      document.addEventListener('click', (e) => {
        if (e.target.classList.contains('btn-star')) {
          const sid = e.target.dataset.id;
          if (starredIds.has(sid)) {
            starredIds.delete(sid);
          } else {
            starredIds.add(sid);
          }
          updateStarUI();
        }
      });

      // Star filter
      let isStarFilterActive = false;
      const btnFilterStar = document.getElementById('btn-filter-star');
      btnFilterStar.addEventListener('click', () => {
        isStarFilterActive = !isStarFilterActive;
        btnFilterStar.classList.toggle('star-active', isStarFilterActive);
        document.querySelectorAll('.duo-card').forEach(card => {
          const sid = card.dataset.id;
          if (isStarFilterActive) {
            card.style.display = starredIds.has(sid) ? '' : 'none';
          } else {
            card.style.display = '';
          }
        });
      });

      // Study Masks
      const toolMaskJp = document.getElementById('tool-mask-jp');
      toolMaskJp.addEventListener('click', () => {
        document.body.classList.toggle('mask-jp');
        toolMaskJp.classList.toggle('active');
      });

      const toolMaskMeaning = document.getElementById('tool-mask-meaning');
      toolMaskMeaning.addEventListener('click', () => {
        document.body.classList.toggle('mask-meaning');
        toolMaskMeaning.classList.toggle('active');
      });

      const toolMaskCloze = document.getElementById('tool-mask-cloze');
      toolMaskCloze.addEventListener('click', () => {
        document.body.classList.toggle('mask-cloze');
        toolMaskCloze.classList.toggle('active');
      });

      const toolHighlightGender = document.getElementById('tool-highlight-gender');
      toolHighlightGender.addEventListener('click', () => {
        document.body.classList.toggle('highlight-gender');
        toolHighlightGender.classList.toggle('active');
      });

      // Speed change
      dockSpeed.addEventListener('change', () => {
        audio.playbackRate = parseFloat(dockSpeed.value);
      });

      // Playback Highlight
      function highlightCard(sid) {
        document.querySelectorAll('.duo-card').forEach(c => c.classList.remove('active-playback'));
        document.querySelectorAll('.btn-play-single').forEach(b => {
          b.classList.remove('playing');
          b.textContent = '▶';
        });

        if (sid) {
          const card = document.getElementById(`card-${sid}`);
          if (card) {
            card.classList.add('active-playback');
            const btn = card.querySelector('.btn-play-single');
            if (btn) {
              btn.classList.add('playing');
              btn.textContent = '⏸';
            }
          }
        }
      }

      function playSentence(sid, startPlay = true) {
        currentSentenceId = sid;
        currentMode = 'single';
        const card = document.getElementById(`card-${sid}`);
        if (!card) return;

        const fr = card.querySelector('.french-sentence').textContent;
        dockTitle.textContent = `No. ${sid} 再生中`;
        dockSub.textContent = fr;
        dockIndicator.classList.add('live');
        dockPlayBtn.textContent = '⏸';

        const repMode = dockRepeat.value;
        if (repMode === '3') repeatCountRemaining = 2;
        else repeatCountRemaining = 0;

        audio.src = `audio/sentence_${sid}.mp3`;
        audio.playbackRate = parseFloat(dockSpeed.value);
        if (startPlay) {
          audio.play().catch(e => console.log('Autoplay:', e));
          isPlaying = true;
          highlightCard(sid);
        }
      }

      // Audio Event Handlers
      audio.addEventListener('play', () => {
        isPlaying = true;
        dockPlayBtn.textContent = '⏸';
        dockIndicator.classList.add('live');
      });

      audio.addEventListener('pause', () => {
        isPlaying = false;
        dockPlayBtn.textContent = '▶';
        dockIndicator.classList.remove('live');
        highlightCard(null);
      });

      audio.addEventListener('ended', () => {
        const repMode = dockRepeat.value;
        if (repMode === 'loop') {
          audio.currentTime = 0;
          audio.play();
        } else if (repMode === '3' && repeatCountRemaining > 0) {
          repeatCountRemaining--;
          audio.currentTime = 0;
          audio.play();
        } else if (repMode === 'seq') {
          const nextId = String(parseInt(currentSentenceId, 10) + 1).padStart(3, '0');
          if (parseInt(nextId, 10) <= 560) {
            playSentence(nextId, true);
            const nextCard = document.getElementById(`card-${nextId}`);
            if (nextCard) nextCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
          } else {
            highlightCard(null);
          }
        } else {
          highlightCard(null);
        }
      });

      // Card audio button
      document.addEventListener('click', (e) => {
        const btn = e.target.closest('.btn-play-single');
        if (btn) {
          const sid = btn.dataset.id;
          if (currentSentenceId === sid && isPlaying) {
            audio.pause();
          } else {
            playSentence(sid, true);
          }
        }
      });

      // Section OPUS
      document.addEventListener('click', (e) => {
        const btn = e.target.closest('.btn-section-opus');
        if (btn) {
          const opusSrc = btn.dataset.opus;
          const sec = btn.dataset.sec;
          if (currentSectionNum === sec && isPlaying && currentMode === 'opus') {
            audio.pause();
            btn.classList.remove('playing');
            btn.textContent = '▶ セクション通し再生 (OPUS)';
          } else {
            document.querySelectorAll('.btn-section-opus').forEach(b => {
              b.classList.remove('playing');
              b.textContent = '▶ セクション通し再生 (OPUS)';
            });
            currentSectionNum = sec;
            currentMode = 'opus';
            dockTitle.textContent = `Section ${sec} 通し再生中 (OPUS)`;
            dockSub.textContent = `セクション統合連続音声`;
            audio.src = opusSrc;
            audio.playbackRate = parseFloat(dockSpeed.value);
            audio.play();
            btn.classList.add('playing');
            btn.textContent = '⏸ 一時停止';
            highlightCard(null);
          }
        }
      });

      // Dock controls
      dockPlayBtn.addEventListener('click', () => {
        if (!audio.src) {
          playSentence('001', true);
          return;
        }
        if (isPlaying) {
          audio.pause();
        } else {
          audio.play();
        }
      });

      dockPrevBtn.addEventListener('click', () => {
        if (!currentSentenceId) return;
        const prevId = String(Math.max(1, parseInt(currentSentenceId, 10) - 1)).padStart(3, '0');
        playSentence(prevId, true);
        const card = document.getElementById(`card-${prevId}`);
        if (card) card.scrollIntoView({ behavior: 'smooth', block: 'center' });
      });

      dockNextBtn.addEventListener('click', () => {
        if (!currentSentenceId) return;
        const nextId = String(Math.min(560, parseInt(currentSentenceId, 10) + 1)).padStart(3, '0');
        playSentence(nextId, true);
        const card = document.getElementById(`card-${nextId}`);
        if (card) card.scrollIntoView({ behavior: 'smooth', block: 'center' });
      });

      // Modal Controls
      const modalSections = document.getElementById('modal-sections');
      const modalIndex = document.getElementById('modal-index');

      function closeAllModalsDesktop() {
        if (modalSections) modalSections.classList.remove('open');
        if (modalIndex) modalIndex.classList.remove('open');
      }

      const btnOpdBannerD = document.getElementById('btn-open-opd-banner');
      if (btnOpdBannerD) btnOpdBannerD.addEventListener('click', openOpdCuisineDesktop);
      const btnOpdCardD = document.getElementById('btn-open-opd-card');
      if (btnOpdCardD) btnOpdCardD.addEventListener('click', openOpdCuisineDesktop);

      document.getElementById('btn-open-sections').addEventListener('click', () => {
        closeAllModalsDesktop();
        modalSections.classList.add('open');
      });
      document.getElementById('btn-open-index').addEventListener('click', () => {
        closeAllModalsDesktop();
        modalIndex.classList.add('open');
        if (!isIndexInitialized) {
          initIndexView();
        }
      });

      document.querySelectorAll('.modal-close, .modal-overlay').forEach(el => {
        el.addEventListener('click', (e) => {
          if (e.target === el || e.target.classList.contains('modal-close')) {
            closeAllModalsDesktop();
          }
        });
      });

      // Quick Jump Link (DUO Core & Everyday Vocabulary)
      document.addEventListener('click', (e) => {
        const dailyJump = e.target.closest('[data-jump-daily]');
        if (dailyJump) {
          closeAllModalsDesktop();
          activateDailyTheme(dailyJump.dataset.jumpDaily);
          return;
        }

        const jumpEl = e.target.closest('[data-jump]');
        if (jumpEl) {
          const targetId = jumpEl.dataset.jump;
          if (targetId.startsWith('card-daily-')) {
            const did = targetId.replace('card-daily-', '');
            closeAllModalsDesktop();
            jumpToDailyWord(did);
            return;
          }
          const target = document.getElementById(targetId);
          if (target) {
            closeAllModalsDesktop();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            if (target.classList.contains('duo-card')) {
              target.classList.add('highlight-pulse');
              setTimeout(() => target.classList.remove('highlight-pulse'), 2000);
            }
          }
        }
      });

      // =========================================================================
      // ULTRA-FAST A-Z INDEX VIRTUAL RENDERING SYSTEM (60 FPS)
      // =========================================================================
      const typeLabels = {
        'headword': '見出',
        'deriv': '派生',
        'idiom': '成句',
        'syn': '類義',
        'ant': '反意',
        '日常': '日常'
      };

      function escapeHtml(str) {
        if (!str) return '';
        return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
      }

      const azContainer = document.getElementById('az-words-container');
      const azStatusBar = document.getElementById('az-status-bar');
      const azSearchInput = document.getElementById('az-search-input');
      const azTypeBtns = document.querySelectorAll('.az-type-btn');
      const azTabs = document.querySelectorAll('.az-tab');
      const modalIndexBody = document.querySelector('#modal-index .modal-body');

      let currentLetter = 'A';
      let currentType = 'all';
      let currentQuery = '';
      let isIndexInitialized = false;
      let currentRenderedCount = 0;
      let currentMatchingPool = [];
      const PAGE_CHUNK = 500;

      function renderIndexCards(items, append = false) {
        let htmlBuffer = [];
        for (let i = 0; i < items.length; i++) {
          const item = items[i];
          const word = item[0];
          const type = item[1];
          const pos = item[2];
          const meaning = item[3];
          const sid = item[4];

          const isDaily = sid.startsWith('daily-');
          const tLabel = typeLabels[type] || (isDaily ? '日常' : '語彙');
          const isDailyClass = (type === '日常' || isDaily) ? ' tag-daily' : '';
          const targetText = isDaily ? `生活語 #${sid.replace('daily-','')}` : `No. ${sid}`;
          const posText = pos ? `【${escapeHtml(pos)}】` : '';

          htmlBuffer.push(`
            <div class="index-entry" data-jump="card-${sid}">
              <div class="index-lemma-wrap">
                <span class="index-tag-type${isDailyClass}">[${tLabel}]</span>
                <span class="index-lemma">${escapeHtml(word)}</span>
                ${posText ? `<span class="index-tag-pos">${posText}</span>` : ''}
                ${meaning ? `<span class="index-preview">${escapeHtml(meaning)}</span>` : ''}
              </div>
              <span class="index-target-link">${targetText}</span>
            </div>
          `);
        }

        if (append) {
          const temp = document.createElement('div');
          temp.innerHTML = htmlBuffer.join('');
          while (temp.firstChild) {
            azContainer.appendChild(temp.firstChild);
          }
        } else {
          azContainer.innerHTML = htmlBuffer.join('');
        }
      }

      function updateLoadMoreButton() {
        const existingBtn = document.getElementById('az-load-more');
        if (existingBtn) existingBtn.remove();

        if (currentRenderedCount < currentMatchingPool.length) {
          const moreBtn = document.createElement('button');
          moreBtn.id = 'az-load-more';
          moreBtn.className = 'btn-more-results';
          moreBtn.textContent = `さらに読み込む (全 ${currentMatchingPool.length.toLocaleString()} 件中 ${currentRenderedCount.toLocaleString()} 件表示中)`;
          moreBtn.addEventListener('click', loadMoreIndexItems);
          azContainer.appendChild(moreBtn);
        }
      }

      function loadMoreIndexItems() {
        if (currentRenderedCount >= currentMatchingPool.length) return;
        const nextCount = Math.min(currentRenderedCount + PAGE_CHUNK, currentMatchingPool.length);
        renderIndexCards(currentMatchingPool.slice(currentRenderedCount, nextCount), true);
        currentRenderedCount = nextCount;
        updateLoadMoreButton();
      }

            function updateIndexResults() {
        const q = currentQuery.toLowerCase().trim();

        if (q) {
          const isAscii = /^[\x00-\x7F]+$/.test(q);
          const escapedQ = q.replace(/[\-\/\\^$*+?.()|[\]{}]/g, '\\$&');
          const regexWordStart = new RegExp('(?:^|[\\s\\-\'’])' + escapedQ);

          let scored = [];
          for (let i = 0; i < INDEX_DATA.length; i++) {
            const item = INDEX_DATA[i];
            if (currentType !== 'all' && item[1] !== currentType) continue;

            const w = item[0].toLowerCase();
            const m = item[3].toLowerCase();

            let score = 0;
            if (w === q) {
              score = 100; // Exact match on French word
            } else if (w.startsWith(q)) {
              score = 80;  // Prefix match on French word (e.g. "gant" -> "gants")
            } else if (regexWordStart.test(w)) {
              score = 70;  // Word component prefix match (e.g. "boîte à gants")
            } else if (m === q) {
              score = 60;  // Exact match on Japanese meaning
            } else if (m.startsWith(q) || m.includes('、' + q) || m.includes('(' + q) || m.includes('（' + q)) {
              score = 50;  // Japanese component match
            } else if (!isAscii && m.includes(q)) {
              score = 30;  // Japanese partial match (only for Japanese search query)
            }

            if (score > 0) {
              scored.push({ score, item });
            }
          }

          // Sort: highest score first, then shorter word length, then alphabetical
          scored.sort((a, b) => {
            if (b.score !== a.score) return b.score - a.score;
            if (a.item[0].length !== b.item[0].length) return a.item[0].length - b.item[0].length;
            return a.item[0].localeCompare(b.item[0]);
          });

          currentMatchingPool = scored.map(s => s.item);
          azStatusBar.textContent = `「${escapeHtml(q)}」の検索結果: 全 ${currentMatchingPool.length.toLocaleString()} 件`;
        } else {
          currentMatchingPool = INDEX_DATA.filter(item => {
            if (currentType !== 'all' && item[1] !== currentType) return false;
            return item[5] === currentLetter;
          });
          azStatusBar.textContent = `アルファベット [${currentLetter}] (全 ${currentMatchingPool.length.toLocaleString()} 件)`;
        }

        currentRenderedCount = Math.min(PAGE_CHUNK, currentMatchingPool.length);
        renderIndexCards(currentMatchingPool.slice(0, currentRenderedCount), false);
        updateLoadMoreButton();
      }

      if (modalIndexBody) {
        modalIndexBody.addEventListener('scroll', () => {
          if (currentRenderedCount >= currentMatchingPool.length) return;
          if (modalIndexBody.scrollTop + modalIndexBody.clientHeight >= modalIndexBody.scrollHeight - 350) {
            loadMoreIndexItems();
          }
        }, { passive: true });
      }

      function initIndexView() {
        isIndexInitialized = true;
        updateIndexResults();
      }

      // Letter tab switching
      azTabs.forEach(tab => {
        tab.addEventListener('click', () => {
          azTabs.forEach(t => t.classList.remove('active'));
          tab.classList.add('active');
          currentLetter = tab.dataset.letter;
          if (azSearchInput.value) {
            azSearchInput.value = '';
            currentQuery = '';
          }
          updateIndexResults();
          if (modalIndexBody) modalIndexBody.scrollTop = 0;
        });
      });

      // Type filter buttons
      azTypeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          azTypeBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          currentType = btn.dataset.type;
          updateIndexResults();
        });
      });

      // Search debounce
      let azSearchTimer = null;
      azSearchInput.addEventListener('input', () => {
        clearTimeout(azSearchTimer);
        azSearchTimer = setTimeout(() => {
          currentQuery = azSearchInput.value;
          updateIndexResults();
        }, 120);
      });

      // =========================================================================
      // REALTIME GLOBAL SEARCH (WITH 150MS DEBOUNCE FOR SMOOTH PERFORMANCE)
      // =========================================================================
      const searchInput = document.getElementById('global-search');
      const searchClear = document.getElementById('search-clear-btn');
      let globalSearchTimer = null;

      searchInput.addEventListener('input', () => {
        clearTimeout(globalSearchTimer);
        const q = searchInput.value.toLowerCase().trim();
        searchClear.style.display = q ? 'block' : 'none';

        globalSearchTimer = setTimeout(() => {
          requestAnimationFrame(() => {
            if (!q) {
              document.querySelectorAll('.duo-card').forEach(c => c.style.display = '');
              return;
            }

            document.querySelectorAll('.duo-card').forEach(card => {
              const fr = (card.querySelector('.french-sentence') || {}).textContent || '';
              const jp = (card.querySelector('.japanese-translation') || {}).textContent || '';
              const wordsSearch = Array.from(card.querySelectorAll('.word-row')).map(w => 
                w.dataset.search || ''
              ).join(' ').toLowerCase();

              const match = fr.toLowerCase().includes(q) || jp.toLowerCase().includes(q) || wordsSearch.includes(q);
              card.style.display = match ? '' : 'none';
            });
          });
        }, 150);
      });

      searchClear.addEventListener('click', () => {
        searchInput.value = '';
        searchInput.dispatchEvent(new Event('input'));
        searchInput.focus();
      });

      """ + generate_daily_js() + """
    })();
  </script>
</body>
</html>
""")

    full_html = "".join(html_out)
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(full_html)

    print("=" * 60)
    print("DUO Français Web App (Soft Pastel Edition) compiled successfully!")
    print(f"Output File     : {OUTPUT_HTML}")
    print(f"File Size       : {len(full_html) / 1024:.1f} KB ({len(full_html) / 1024 / 1024:.2f} MB)")
    print(f"Total Sentences : {total_sentences} sentences")
    print(f"Total Lemmas    : {total_lemmas} headwords")
    print(f"Total Index     : {len(all_words_index):,} vocabulary items")
    print("=" * 60)

if __name__ == "__main__":
    print("Parsing all 45 section markdown files...")
    sections_data, all_words_index, index_counts, total_sentences, total_lemmas = parse_all_sections()
    print(f"Parsed {len(sections_data)} sections, {total_sentences} sentences, {len(all_words_index)} vocabulary items.")
    print("Compiling interactive HTML web app (Soft Pastel Edition)...")
    generate_html(sections_data, all_words_index, index_counts, total_sentences, total_lemmas)
