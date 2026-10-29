# -*- coding: utf-8 -*-
"""
DUO Français 3.0 — Smartphone-Optimized Web Application Compiler (Mobile Edition)
Builds `duo_francais/mobile.html` from all 45 section Markdown files and audio assets.
Key Mobile Features:
- Dedicated Smartphone 2-Column Side-by-Side Layout (Left 33%: Headword + IPA, Right 67%: POS + Meaning + =/⇔ + Notes + Derivatives).
- Horizontal Swipe Navigation between sentences (No. 001 to No. 560) + Thumb-friendly Prev/Next controls.
- No tap-to-expand accordions: all vocabulary information is immediately visible at a glance.
- One-Handed Thumb-Zone Bottom Navigation Bar (Prev, Sections, A-Z Index, Search/Tools, Next) + 1-Line Compact Audio Bar.
- Ultra-lightweight Monochrome A-Z Index with 500-item batch + automatic infinite scroll.
"""

import os
import re
import sys
import json
import html
from daily_vocab_builder import load_daily_vocab_data, get_daily_index_entries, generate_daily_css, generate_daily_sections_html, generate_daily_toc_html, generate_daily_js, generate_app_ui_css

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from build_web_app import (
    BASE_DIR,
    parse_all_sections,
    format_inline_markdown,
    get_pos_class,
    get_actor_class,
)

OUTPUT_MOBILE_HTML = os.path.join(BASE_DIR, "mobile.html")


def generate_mobile_html(sections_data, all_words_index, index_counts, total_sentences, total_lemmas):
    daily_themes = load_daily_vocab_data()
    # Prepare Section Quiz Data: lemma, pos, clean short meaning, sid
    sec_quiz_map = {}
    for sec in sections_data:
        s_items = []
        for s in sec["sentences"]:
            for w in s["words"]:
                m_clean = re.sub(r"<[^>]+>", "", format_inline_markdown(w["meaning"]))
                m_short = m_clean.split("；")[0].split(";")[0].strip()
                s_items.append([w["lemma"], w["pos"], m_short, s["id"]])
        sec_quiz_map[sec["num"]] = s_items
    json_sec_quiz_str = json.dumps(sec_quiz_map, ensure_ascii=False, separators=(',', ':'))

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
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <title>DUO Français 3.0 Mobile — スマホ最適化版</title>
  <meta name="description" content="全45セクション・560例文・2,221見出し語・巻末11,458総合索引。2カラム横並び＆左右スワイプ移動対応のスマホ最適化版。">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Noto+Sans+JP:wght@400;500;700;900&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">

  <style>
    :root {{
      --primary: #2563eb;
      --primary-light: #60a5fa;
      --primary-bg: #f1f5fa;
      --navy-dark: #1e293b;
      --text-main: #1e293b;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --border-dark: #cbd5e1;
      --bg-page: #f1f5f9;
      --bg-card: #ffffff;
      --mask-bg: #cbd5e1;
      --safe-bottom: env(safe-area-inset-bottom, 0px);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }}
    html, body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Noto Sans JP', sans-serif;
      background-color: var(--bg-page);
      color: var(--text-main);
      line-height: 1.5;
      overscroll-behavior-x: none;
    }}
    body {{
      padding-bottom: calc(48px + var(--safe-bottom));
    }}
    body.audio-open {{
      padding-bottom: calc(88px + var(--safe-bottom));
    }}

    code {{
      font-family: 'JetBrains Mono', Consolas, monospace;
      background: #f1f5f9;
      color: #334155;
      padding: 0.05rem 0.28rem;
      border-radius: 3px;
      font-size: 0.86em;
      border: 1px solid #e2e8f0;
    }}
    strong {{ font-weight: 700; color: #0f172a; }}
    em {{ font-style: italic; font-family: 'Source Serif 4', Georgia, serif; }}

    /* ==========================================================================
       SUPER COMPACT MOBILE TOP BAR
       ========================================================================== */
    header {{
      background: #1e293b;
      color: white;
      padding: 0.3rem 0.6rem;
      position: sticky;
      top: 0;
      z-index: 500;
      box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    }}
    .header-inner {{
      max-width: 640px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.4rem;
    }}
    .header-left {{
      display: flex;
      align-items: center;
      gap: 0.4rem;
      min-width: 0;
      flex: 1;
    }}
    .sec-badge-pill {{
      font-family: 'Cinzel', serif;
      font-size: 0.76rem;
      font-weight: 800;
      color: #93c5fd;
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.18);
      padding: 0.12rem 0.45rem;
      border-radius: 4px;
      white-space: nowrap;
      cursor: pointer;
    }}
    .sec-title-text {{
      font-size: 0.74rem;
      font-weight: 600;
      color: #e2e8f0;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}

    .header-right {{
      display: flex;
      align-items: center;
      gap: 0.3rem;
      flex-shrink: 0;
    }}
    .btn-top-mini {{
      background: rgba(255,255,255,0.1);
      border: 1px solid rgba(255,255,255,0.2);
      color: #f1f5f9;
      font-size: 0.68rem;
      font-weight: 700;
      padding: 0.18rem 0.42rem;
      border-radius: 4px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.15rem;
    }}
    .btn-top-mini.active {{
      background: #fee2e2;
      color: #dc2626;
      border-color: #fca5a5;
    }}
    .btn-top-mini.star-active {{
      background: #fef08a;
      color: #854d0e;
      border-color: #facc15;
    }}

    /* Thin Progress Strip */
    .mobile-nav-strip {{
      background: #e2e8f0;
      height: 3px;
      width: 100%;
      position: sticky;
      top: 32px;
      z-index: 490;
    }}
    .progress-bar-fill {{
      height: 100%;
      background: #2563eb;
      width: 0.18%;
      transition: width 0.15s ease;
    }}

    /* ==========================================================================
       MEMORIZATION MASKS (赤シート統合モード: 和訳 + 意味 + 派生語 + 成句を一括隠蔽)
       ========================================================================== */
    body.mask-redsheet .japanese-translation,
    body.mask-redsheet .meaning,
    body.mask-redsheet .meaning *,
    body.mask-redsheet .rel-meaning,
    body.mask-redsheet .rel-meaning *,
    body.mask-redsheet .word-note,
    body.mask-redsheet .word-etym {{
      background: #cbd5e1 !important;
      color: transparent !important;
      border-radius: 4px;
      user-select: none;
      -webkit-user-select: none;
      display: inline-block;
      cursor: pointer;
    }}
    body.mask-redsheet .word-note,
    body.mask-redsheet .word-etym {{
      display: block;
      border-left-color: #cbd5e1 !important;
    }}

    body.mask-cloze .word-token {{
      background: #cbd5e1;
      color: transparent;
      border-radius: 3px;
      padding: 0 3px;
      user-select: none;
      border-bottom: 2px solid #93c5fd;
    }}
    body.highlight-gender .pos-m {{
      box-shadow: 0 0 0 2px #60a5fa;
      background-color: #dbeafe;
    }}
    body.highlight-gender .pos-f {{
      box-shadow: 0 0 0 2px #f472b6;
      background-color: #fce7f3;
    }}

    /* ==========================================================================
       MAIN CONTAINER & SWIPE STAGE
       ========================================================================== */
    main {{
      max-width: 640px;
      margin: 0.5rem auto;
      padding: 0 0.5rem;
      min-height: calc(100vh - 210px);
      touch-action: pan-y;
    }}

    .section-container {{
      display: none;
    }}
    .section-container.active-sec {{
      display: block;
    }}
    .section-banner {{
      display: none;
    }}

    /* ==========================================================================
       DUO MOBILE CARD (2-COLUMN SIDE-BY-SIDE LAYOUT)
       ========================================================================== */
    .duo-card {{
      display: none;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 10px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.04);
      overflow: hidden;
      content-visibility: auto;
    }}
    .duo-card.active-card {{
      display: block;
    }}
    .duo-card.is-starred {{
      border-left: 4px solid #facc15;
    }}

    /* 1. TOP: French Sentence Header */
    .sentence-header {{
      background: #f1f5fa;
      border-left: 4px solid #93c5fd;
      border-bottom: 1px solid #e2e8f0;
      padding: 0.75rem 0.85rem;
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
    }}
    .sentence-top-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .sentence-badge-group {{
      display: flex;
      align-items: center;
      gap: 0.45rem;
    }}
    .sentence-number {{
      font-family: 'Cinzel', serif;
      font-size: 0.85rem;
      font-weight: 800;
      color: #2563eb;
      background: white;
      border: 1px solid #bfdbfe;
      padding: 0.1rem 0.45rem;
      border-radius: 5px;
      line-height: 1.2;
    }}
    .cast-pill {{
      font-size: 0.68rem;
      font-weight: 700;
      padding: 0.1rem 0.4rem;
      border-radius: 4px;
    }}
    .cast-male {{ background: #eff6ff; color: #2563eb; border: 1px solid #dbeafe; }}
    .cast-female {{ background: #fdf2f8; color: #db2777; border: 1px solid #fce7f3; }}
    .cast-duet {{ background: #f5f3ff; color: #7c3aed; border: 1px solid #ede9fe; }}

    .sentence-top-actions {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .btn-star {{
      background: none;
      border: none;
      color: #94a3b8;
      cursor: pointer;
      font-size: 1.25rem;
      line-height: 1;
      padding: 0.1rem 0.25rem;
    }}
    .btn-star.starred {{ color: #eab308; }}

    .btn-play-single {{
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 50%;
      width: 34px;
      height: 34px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: #2563eb;
      font-size: 0.85rem;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .btn-play-single.playing {{
      background: #fee2e2;
      color: #dc2626;
      border-color: #fca5a5;
    }}

    .french-sentence {{
      font-family: 'Source Serif 4', Georgia, serif;
      font-size: 1.15rem;
      font-weight: 600;
      color: #0f172a;
      line-height: 1.45;
      letter-spacing: 0.01em;
    }}

    /* 2. MIDDLE: Smartphone 2-Column Side-by-Side Vocabulary Table */
    .words-table {{
      display: flex;
      flex-direction: column;
      background: white;
    }}
    .word-row {{
      display: flex;
      flex-direction: row;
      border-bottom: 1px solid #f1f5f9;
      padding: 0.65rem 0.7rem;
      gap: 0.6rem;
      align-items: flex-start;
    }}
    .word-row:last-child {{
      border-bottom: none;
    }}

    /* Left Column (33% width): Headword + IPA */
    .word-left-col {{
      flex: 0 0 33%;
      max-width: 33%;
      display: flex;
      flex-direction: column;
      gap: 0.15rem;
      border-right: 1px dashed #e2e8f0;
      padding-right: 0.45rem;
      overflow-wrap: break-word;
      word-break: break-word;
    }}
    .word-head-line {{
      display: flex;
      align-items: baseline;
      gap: 0.25rem;
    }}
    .word-checkbox {{
      color: #94a3b8;
      font-size: 0.78rem;
      user-select: none;
      flex-shrink: 0;
    }}
    .lemma-title {{
      font-size: 0.92rem;
      font-weight: 700;
      color: #0f172a;
      line-height: 1.3;
    }}
    .phonetic-ipa {{
      font-family: 'Source Serif 4', serif;
      font-size: 0.74rem;
      color: #64748b;
      padding-left: 0.9rem;
      line-height: 1.25;
    }}

    /* Right Column (67% width): POS, Meaning, =, ⇔, Notes, Derivatives */
    .word-right-col {{
      flex: 1;
      min-width: 0;
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }}
    .word-meaning-line {{
      display: flex;
      flex-wrap: wrap;
      align-items: baseline;
      gap: 0.35rem;
    }}

    .pos-pill {{
      font-size: 0.66rem;
      font-weight: 700;
      padding: 0.06rem 0.35rem;
      border-radius: 3px;
      border: 1px solid transparent;
      flex-shrink: 0;
    }}
    .pos-m {{ background-color: #eff6ff; color: #1d4ed8; border-color: #bfdbfe; }}
    .pos-f {{ background-color: #fdf2f8; color: #be185d; border-color: #fbcfe8; }}
    .pos-v {{ background-color: #f0fdf4; color: #15803d; border-color: #bbf7d0; }}
    .pos-adj {{ background-color: #faf5ff; color: #7e22ce; border-color: #e9d5ff; }}
    .pos-adv {{ background-color: #f8fafc; color: #475569; border-color: #cbd5e1; }}
    .pos-expr {{ background-color: #fffbeb; color: #b45309; border-color: #fde68a; }}
    .pos-other {{ background-color: #f3f4f6; color: #4b5563; border-color: #e5e7eb; }}

    .meaning {{
      font-size: 0.84rem;
      font-weight: 600;
      color: #1e293b;
      line-height: 1.42;
    }}

    /* Synonyms & Antonyms (= and ⇔ only, monochrome black text) */
    .word-synonyms, .word-antonyms {{
      font-size: 0.76rem;
      line-height: 1.4;
      display: flex;
      align-items: baseline;
      gap: 0.35rem;
      color: #1e293b;
    }}
    .syn-badge, .ant-badge {{
      background: transparent;
      color: #475569;
      border: none;
      padding: 0;
      font-weight: 700;
      font-size: 0.8rem;
      white-space: nowrap;
      flex-shrink: 0;
      line-height: 1;
    }}
    .syn-content, .ant-content {{
      color: #1e293b;
    }}

    .word-note {{
      font-size: 0.75rem;
      color: #0369a1;
      background: #f0f9ff;
      border-left: 2.5px solid #38bdf8;
      padding: 0.22rem 0.45rem;
      border-radius: 0 3px 3px 0;
      line-height: 1.4;
    }}
    .word-etym {{
      font-size: 0.74rem;
      color: #92400e;
      background: #fffbeb;
      border-left: 2.5px solid #fcd34d;
      padding: 0.2rem 0.45rem;
      border-radius: 0 3px 3px 0;
      line-height: 1.4;
    }}
    .word-rel-list {{
      margin-top: 0.15rem;
      font-size: 0.76rem;
      color: var(--text-muted);
      line-height: 1.4;
      display: flex;
      flex-direction: column;
      gap: 0.18rem;
    }}
    .rel-item {{
      display: flex;
      flex-wrap: wrap;
      align-items: baseline;
      gap: 0.25rem;
    }}
    .rel-item .phonetic-ipa {{
      padding-left: 0;
      font-size: 0.72rem;
    }}
    .rel-icon {{ font-weight: 700; font-size: 0.7rem; }}
    .rel-icon.deriv {{ color: #64748b; }}
    .rel-icon.idiom {{ color: #d97706; }}
    .rel-word {{ font-weight: 700; color: #1e293b; }}
    .rel-meaning {{ color: #475569; }}

    /* 3. BOTTOM: Separated Japanese Translation Box */
    .card-translation-box {{
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
      padding: 0.65rem 0.85rem;
      display: flex;
      align-items: baseline;
      gap: 0.55rem;
    }}
    .translation-tag {{
      font-size: 0.66rem;
      font-weight: 700;
      color: #64748b;
      background: white;
      border: 1px solid #cbd5e1;
      padding: 0.1rem 0.4rem;
      border-radius: 3px;
      flex-shrink: 0;
    }}
    .japanese-translation {{
      font-size: 0.86rem;
      color: #1e293b;
      font-weight: 500;
      line-height: 1.5;
      flex: 1;
    }}

    /* ==========================================================================
       SECTION END QUIZ BANNER & POPUP MODAL
       ========================================================================== */
    .sec-quiz-banner {{
      margin-top: 0.8rem;
      background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%);
      border: 1.5px dashed #93c5fd;
      border-radius: 10px;
      padding: 0.85rem;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 0.4rem;
    }}
    .sec-quiz-title {{
      font-size: 0.82rem;
      font-weight: 700;
      color: #1e40af;
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }}
    .sec-quiz-sub {{
      font-size: 0.72rem;
      color: #64748b;
    }}
    .btn-start-quiz {{
      background: #2563eb;
      color: white;
      border: none;
      padding: 0.45rem 1.2rem;
      border-radius: 20px;
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 2px 6px rgba(37,99,235,0.25);
      margin-top: 0.2rem;
    }}
    .btn-start-quiz:active {{
      background: #1d4ed8;
      transform: scale(0.98);
    }}

    /* Quiz Modal */
    .quiz-card {{
      background: white;
      border-radius: 16px 16px 0 0;
      width: 100%;
      max-width: 640px;
      max-height: 85vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 -8px 28px rgba(0,0,0,0.2);
      overflow: hidden;
      animation: sheetUp 0.2s ease-out;
    }}
    .quiz-header {{
      background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
      color: white;
      padding: 0.8rem 1rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .quiz-header h3 {{
      font-size: 0.95rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}
    .quiz-body {{
      padding: 1.1rem 1rem;
      overflow-y: auto;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 0.9rem;
    }}
    .quiz-progress-text {{
      font-size: 0.75rem;
      font-weight: 700;
      color: #64748b;
      display: flex;
      justify-content: space-between;
    }}
    .quiz-question-box {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 10px;
      padding: 1rem;
      text-align: center;
    }}
    .quiz-q-word {{
      font-size: 1.35rem;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: 0.02em;
    }}
    .quiz-q-pos {{
      display: inline-block;
      margin-top: 0.25rem;
      font-size: 0.72rem;
      font-weight: 700;
      color: #2563eb;
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      padding: 0.1rem 0.45rem;
      border-radius: 4px;
    }}
    .quiz-choices {{
      display: flex;
      flex-direction: column;
      gap: 0.55rem;
    }}
    .quiz-choice-btn {{
      background: #ffffff;
      border: 1.5px solid #cbd5e1;
      border-radius: 8px;
      padding: 0.65rem 0.85rem;
      text-align: left;
      font-size: 0.86rem;
      font-weight: 600;
      color: #1e293b;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.12s;
    }}
    .quiz-choice-btn:active {{
      background: #f1f5f9;
    }}
    .quiz-choice-btn.correct {{
      background: #dcfce7 !important;
      border-color: #22c55e !important;
      color: #15803d !important;
    }}
    .quiz-choice-btn.incorrect {{
      background: #fee2e2 !important;
      border-color: #ef4444 !important;
      color: #b91c1c !important;
    }}
    .quiz-choice-num {{
      font-family: 'Cinzel', serif;
      font-size: 0.76rem;
      font-weight: 800;
      color: #64748b;
      width: 18px;
    }}
    .quiz-feedback {{
      display: none;
      border-radius: 8px;
      padding: 0.65rem 0.85rem;
      font-size: 0.82rem;
      font-weight: 600;
      line-height: 1.4;
      animation: fadeIn 0.15s ease;
    }}
    .quiz-feedback.show {{ display: block; }}
    .quiz-feedback.ok {{
      background: #f0fdf4;
      border: 1px solid #86efac;
      color: #166534;
    }}
    .quiz-feedback.ng {{
      background: #fef2f2;
      border: 1px solid #fca5a5;
      color: #991b1b;
    }}
    .quiz-next-btn {{
      background: #2563eb;
      color: white;
      border: none;
      padding: 0.6rem;
      border-radius: 8px;
      font-size: 0.86rem;
      font-weight: 700;
      cursor: pointer;
      display: none;
      width: 100%;
      text-align: center;
    }}
    .quiz-next-btn.show {{ display: block; }}

    /* Quiz Result View */
    .quiz-result-box {{
      text-align: center;
      padding: 1.5rem 1rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 0.8rem;
    }}
    .quiz-result-score {{
      font-size: 2.2rem;
      font-weight: 800;
      color: #2563eb;
    }}
    .quiz-result-msg {{
      font-size: 0.92rem;
      font-weight: 700;
      color: #1e293b;
    }}
    .quiz-result-actions {{
      display: flex;
      gap: 0.6rem;
      width: 100%;
      margin-top: 0.6rem;
    }}
    .quiz-result-btn {{
      flex: 1;
      padding: 0.6rem;
      border-radius: 8px;
      font-size: 0.84rem;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid #cbd5e1;
      background: white;
    }}
    .quiz-result-btn.primary {{
      background: #2563eb;
      color: white;
      border-color: #2563eb;
    }}
    .modal-overlay {{
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(15, 23, 42, 0.55);
      backdrop-filter: blur(3px);
      z-index: 1000;
      display: none;
      align-items: flex-end;
      justify-content: center;
    }}
    .modal-overlay.open {{ display: flex; }}

    .modal-card {{
      background: white;
      border-radius: 16px 16px 0 0;
      width: 100%;
      max-width: 640px;
      height: 84vh;
      max-height: 84vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 -8px 28px rgba(0,0,0,0.2);
      overflow: hidden;
      animation: sheetUp 0.2s ease-out;
    }}
    @keyframes sheetUp {{
      from {{ transform: translateY(100%); }}
      to {{ transform: translateY(0); }}
    }}
    .modal-header {{
      background: #1e293b;
      color: white;
      padding: 0.75rem 1rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-shrink: 0;
    }}
    .modal-header h3 {{
      font-size: 0.95rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}
    .modal-close {{
      background: none;
      border: none;
      color: #cbd5e1;
      font-size: 1.4rem;
      cursor: pointer;
      line-height: 1;
      padding: 0.1rem 0.4rem;
    }}
    .modal-body {{
      padding: 0.85rem;
      overflow-y: auto;
      flex: 1;
      -webkit-overflow-scrolling: touch;
    }}

    /* Section Jump Grid */
    .sections-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(155px, 1fr));
      gap: 0.55rem;
    }}
    .sec-jump-card {{
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.55rem 0.7rem;
      cursor: pointer;
      background: #f8fafc;
      display: flex;
      flex-direction: column;
      gap: 0.15rem;
    }}
    .sec-jump-card:active {{
      background: #eff6ff;
      border-color: #93c5fd;
    }}
    .sec-jump-num {{
      font-family: 'Cinzel', serif;
      font-size: 0.82rem;
      font-weight: 800;
      color: #2563eb;
    }}
    .sec-jump-sub {{
      font-size: 0.7rem;
      color: var(--text-muted);
      line-height: 1.3;
    }}

    """ + generate_app_ui_css(is_mobile=True) + generate_daily_css() + """</style>
</head>
<body>

  <!-- SUPER COMPACT HEADER (1-LINE INTEGRATED BAR) -->
  <header>
    <div class="header-inner">
      <div class="header-left" id="btn-open-sections-top">
        <span id="current-sec-badge" class="sec-badge-pill">Sec.01</span>
        <span id="current-sec-label" class="sec-title-text">信条・人間関係</span>
      </div>
      <div class="header-right">
        <button id="btn-filter-star" class="btn-top-mini" title="要復習のみ表示">⭐ <span id="star-count">0</span></button>
        <button id="btn-quick-redsheet" class="btn-top-mini" title="赤シート（和訳・意味・解説を隠す）">🟥 赤シート</button>
        <button id="btn-current-sec-opus" class="btn-top-mini" style="color:#34d399;" title="セクション通し音声">▶ 通し</button>
      </div>
    </div>
  </header>

  <!-- THIN PROGRESS STRIP -->
  <div class="mobile-nav-strip">
    <div id="swipe-progress-fill" class="progress-bar-fill"></div>
  </div>

  <!-- MAIN SWIPE CONTAINER -->
  <main id="main-content">
""")

    # Render all 45 sections & 560 cards
    for sec in sections_data:
        sec_num = sec["num"]
        sec_subtitle = sec["subtitle"]
        has_opus = sec["has_opus"]
        active_sec_cls = " active-sec" if sec_num == 1 else ""

        html_out.append(f"""
    <!-- SECTION {sec_num:02d} -->
    <section class="section-container{active_sec_cls}" id="section-{sec_num:02d}" data-sec="{sec_num}" data-subtitle="{html.escape(sec_subtitle)}" data-opus="audio_sections/{sec['opus_file']}">
      <div class="section-banner">
        <h2>Section {sec_num:02d}</h2>
        {f'<button class="btn-section-opus" data-opus="audio_sections/{sec["opus_file"]}" data-sec="{sec_num}">▶ セクション通し再生 (OPUS)</button>' if has_opus else ''}
      </div>
      <div class="sentences-list">
""")

        for s in sec["sentences"]:
            sid = s["id"]
            cast_str = s["cast"]
            actor_cls = get_actor_class(cast_str)
            fr_text = s["fr"]
            jp_text = s["jp"]
            active_card_cls = " active-card" if sid == "001" else ""

            cloze_text = re.sub(r"\b([A-Za-zÀ-ÿ\-']+)\b", r'<span class="word-token">\1</span>', fr_text)

            html_out.append(f"""
        <!-- CARD No. {sid} -->
        <article class="duo-card{active_card_cls}" id="card-{sid}" data-id="{sid}" data-sec="{sec_num}">
          <!-- 1. TOP: French Sentence -->
          <div class="sentence-header">
            <div class="sentence-top-bar">
              <div class="sentence-badge-group">
                <div class="sentence-number">{sid}</div>
                <span class="cast-pill {actor_cls}">{cast_str}</span>
              </div>
              <div class="sentence-top-actions">
                <button class="btn-star" data-id="{sid}" title="要復習ブックマーク">☆</button>
                <button class="btn-play-single" data-mp3="audio/sentence_{sid}.mp3" data-id="{sid}" title="音声を再生">▶</button>
              </div>
            </div>
            <div class="french-sentence">{cloze_text}</div>
          </div>

          <!-- 2. MIDDLE: 2-Column Side-by-Side Vocabulary Table (見出し語左、日本語右) -->
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

            is_last_sentence_of_sec = (s == sec["sentences"][-1])
            quiz_banner_html = f'''
          <!-- SECTION {sec_num:02d} COMPLETION & QUICK QUIZ BANNER -->
          <div class="sec-quiz-banner">
            <div class="sec-quiz-title">🎉 Section {sec_num:02d} 読了！</div>
            <div class="sec-quiz-sub">このセクションの重要単語から5問の確認ミニクイズに挑戦してみよう</div>
            <button class="btn-start-quiz" data-quiz-sec="{sec_num}">🎯 5問クイズに挑戦！</button>
          </div>''' if is_last_sentence_of_sec else ''

            html_out.append(f"""
          </div>

          <!-- 3. BOTTOM: Separated Japanese Translation Box -->
          {f'''<div class="card-translation-box">
            <span class="translation-tag">和訳</span>
            <div class="japanese-translation">{jp_text}</div>
          </div>''' if jp_text else ''}
          {quiz_banner_html}
        </article>
""")

        html_out.append("""
      </div>
    </section>
""")

    # Append Everyday Vocabulary Themes (THEME 01 - 08, 336 words)
    html_out.append(generate_daily_sections_html(daily_themes, is_mobile=True))

    html_out.append(f"""
  </main>

  <!-- MODAL 1: SECTION DRAWER -->
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
          <div class="sec-jump-card" data-jump-sid="{first_sid}" data-jump="section-{sec['num']:02d}">
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

  <!-- MODAL 2: A-Z COMPREHENSIVE INDEX -->
  <div id="modal-index" class="modal-overlay">
    <div class="modal-card">
      <div class="modal-header">
        <h3>📖 A-Z 巻末総合索引 ({len(all_words_index):,}語)</h3>
        <button class="modal-close" data-close="modal-index">×</button>
      </div>
      <div class="modal-body">
        <div class="index-toolbar">
          <div class="index-search-row">
            <input type="text" id="az-search-input" class="az-search-input" placeholder="🔍 索引内クイック検索 (例: respect, 尊重)...">
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

  <!-- MODAL 3: SEARCH & STUDY TOOLS -->
  <div id="modal-tools" class="modal-overlay">
    <div class="modal-card">
      <div class="modal-header">
        <h3>🔍 例文検索 ＆ 暗記マスク設定</h3>
        <button class="modal-close" data-close="modal-tools">×</button>
      </div>
      <div class="modal-body">
        <div class="tools-section">
          <div class="tools-section-title">暗記サポート設定</div>
          <div class="tools-grid">
            <button id="tool-mask-redsheet" class="tool-btn">🟥 赤シート (和訳＋意味)</button>
            <button id="tool-mask-cloze" class="tool-btn">✏️ 仏文穴埋めテスト</button>
            <button id="tool-highlight-gender" class="tool-btn">🚻 名詞の性を色強調</button>
          </div>
        </div>

        <div class="tools-section">
          <div class="tools-section-title">🌿 日常語パート (生活必須単語集)</div>
          <div class="tools-grid">
            <button id="btn-open-daily-tools" class="tool-btn" style="border-color:#10b981; background:#ecfdf5; color:#065f46; font-weight:700;" onclick="closeAllModals(); activateDailyTheme('section-daily-01');">🌿 日常生活単語集（全8テーマ・336語）</button>
          </div>
        </div>

        <div class="tools-section">
          <div class="tools-section-title">全文・全単語クイック検索 (タップで例文へ移動)</div>
          <div class="search-box-wrap">
            <input type="text" id="global-search" class="search-input" placeholder="🔍 フランス語・日本語・見出し語で検索...">
            <span id="search-clear-btn" class="search-clear">×</span>
          </div>
          <div id="mobile-search-results" class="search-results-list"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- MODAL 4: SECTION QUICK QUIZ -->
  <div id="modal-quiz" class="modal-overlay">
    <div class="quiz-card">
      <div class="quiz-header">
        <h3 id="quiz-header-title">🎯 Section 01 確認クイズ</h3>
        <button class="modal-close" data-close="modal-quiz">×</button>
      </div>
      <div class="quiz-body" id="quiz-container">
        <!-- Interactive Quiz Content injected by JS -->
      </div>
    </div>
  </div>

  <!-- FIXED BOTTOM DOCK: 1-LINE AUDIO BAR + THUMB NAVIGATION -->
  <div class="bottom-fixed-stack">
    <div class="player-dock" id="player-dock">
      <div class="dock-now-playing">
        <div id="dock-indicator" class="dock-indicator"></div>
        <div id="dock-title" class="dock-info-title">No. 001 待機中</div>
        <div id="dock-sub" class="dock-info-sub"></div>
      </div>

      <div class="dock-settings">
        <select id="dock-repeat" class="dock-select" title="リピートモード">
          <option value="1" selected>1回</option>
          <option value="3">3回</option>
          <option value="loop">ループ</option>
          <option value="seq">連続</option>
        </select>
        <select id="dock-speed" class="dock-select" title="再生速度">
          <option value="0.75">0.75x</option>
          <option value="0.9">0.9x</option>
          <option value="1.0" selected>1.0x</option>
          <option value="1.1">1.1x</option>
          <option value="1.25">1.25x</option>
          <option value="1.5">1.5x</option>
        </select>
      </div>

      <div class="dock-controls">
        <button id="dock-prev-btn" class="dock-btn" title="前の文へ">⏮</button>
        <button id="dock-play-btn" class="dock-btn main-play" title="再生 / 一時停止">▶</button>
        <button id="dock-next-btn" class="dock-btn" title="次の文へ">⏭</button>
        <button id="btn-dock-close" class="btn-dock-close" title="閉じる">✕</button>
      </div>
    </div>

    <nav class="thumb-nav-bar">
      <button id="nav-prev-section" class="thumb-tab nav-arrow" title="前のセクションへ">
        <span class="thumb-icon">⏮</span>
        <span>前Sec</span>
      </button>
      <button id="btn-open-sections" class="thumb-tab">
        <span class="thumb-icon">📑</span>
        <span>目次</span>
      </button>
      <button id="btn-open-index" class="thumb-tab">
        <span class="thumb-icon">📖</span>
        <span>索引</span>
      </button>
      <button id="btn-open-tools" class="thumb-tab">
        <span class="thumb-icon">🔍</span>
        <span>検索・マスク</span>
      </button>
      <button id="nav-next-section" class="thumb-tab nav-arrow" title="次のセクションへ">
        <span class="thumb-icon">⏭</span>
        <span>次Sec</span>
      </button>
    </nav>
  </div>

  <!-- EMBEDDED AUDIO ELEMENT -->
  <audio id="audio-engine" preload="none"></audio>

  <!-- COMPACT JSON INDEX & QUIZ DATA -->
  <script>
    const INDEX_DATA = """)

    html_out.append(json_index_str)

    html_out.append(""";
    const SEC_QUIZ_DATA = """)

    html_out.append(json_sec_quiz_str)

    html_out.append(""";

    (function() {
      const audio = document.getElementById('audio-engine');
      const dockTitle = document.getElementById('dock-title');
      const dockIndicator = document.getElementById('dock-indicator');
      const dockPlayBtn = document.getElementById('dock-play-btn');
      const dockPrevBtn = document.getElementById('dock-prev-btn');
      const dockNextBtn = document.getElementById('dock-next-btn');
      const dockSpeed = document.getElementById('dock-speed');
      const dockRepeat = document.getElementById('dock-repeat');

      const allCards = Array.from(document.querySelectorAll('.duo-card'));
      const totalCards = allCards.length;
      const cardMap = new Map();
      allCards.forEach((c, idx) => cardMap.set(c.dataset.id, idx));

      let currentIndex = 0;
      let currentSentenceId = '001';
      let currentSectionNum = '1';
      let isPlaying = false;
      let repeatCountRemaining = 0;
      let currentMode = 'single';
      let starFilterActive = false;

      // Star Bookmarks
      let starredIds = new Set(JSON.parse(localStorage.getItem('duo_starred') || '[]'));
      const starCountEl = document.getElementById('star-count');

      function updateStarUI() {
        starCountEl.textContent = starredIds.size;
        document.querySelectorAll('.btn-star').forEach(btn => {
          const sid = btn.dataset.id;
          const card = document.getElementById(`card-${sid}`);
          if (starredIds.has(sid)) {
            btn.classList.add('starred');
            btn.textContent = '★';
            if (card) card.classList.add('is-starred');
          } else {
            btn.classList.remove('starred');
            btn.textContent = '☆';
            if (card) card.classList.remove('is-starred');
          }
        });
      }

      document.addEventListener('click', (e) => {
        const starBtn = e.target.closest('.btn-star');
        if (starBtn) {
          const sid = starBtn.dataset.id;
          if (starredIds.has(sid)) {
            starredIds.delete(sid);
          } else {
            starredIds.add(sid);
          }
          localStorage.setItem('duo_starred', JSON.stringify([...starredIds]));
          updateStarUI();
        }
      });

      // =========================================================================
      // SENTENCE NAVIGATION & HORIZONTAL SWIPE ENGINE
      // =========================================================================
      const swipeProgressFill = document.getElementById('swipe-progress-fill');
      const currentSecBadge = document.getElementById('current-sec-badge');
      const currentSecLabel = document.getElementById('current-sec-label');
      const btnCurrentSecOpus = document.getElementById('btn-current-sec-opus');

      function showSentenceByIndex(newIndex, slideDirection = 'next') {
        if (newIndex < 0) newIndex = 0;
        if (newIndex >= totalCards) newIndex = totalCards - 1;

        const prevCard = allCards[currentIndex];
        if (prevCard) {
          prevCard.classList.remove('active-card');
          const prevSec = prevCard.closest('.section-container');
          if (prevSec) prevSec.classList.remove('active-sec');
        }

        currentIndex = newIndex;
        const targetCard = allCards[currentIndex];
        currentSentenceId = targetCard.dataset.id;

        const targetSec = targetCard.closest('.section-container');
        if (targetSec) {
          targetSec.classList.add('active-sec');
          const secNum = targetSec.dataset.sec;
          const secSub = targetSec.dataset.subtitle || '';
          const secOpus = targetSec.dataset.opus || '';
          currentSectionNum = secNum;
          if (currentSecBadge) currentSecBadge.textContent = `Sec.${String(secNum).padStart(2, '0')}`;
          if (currentSecLabel) currentSecLabel.textContent = secSub;
          if (btnCurrentSecOpus) {
            btnCurrentSecOpus.dataset.opus = secOpus;
            btnCurrentSecOpus.dataset.sec = secNum;
          }
        }

        targetCard.classList.add('active-card');
        if (swipeProgressFill) swipeProgressFill.style.width = `${((currentIndex + 1) / totalCards) * 100}%`;
        if (!isPlaying) {
          dockTitle.textContent = `No. ${currentSentenceId} / ${totalCards}`;
        }
        localStorage.setItem('duo_mobile_last_sid', currentSentenceId);
        window.scrollTo({ top: 0, behavior: 'instant' });
      }

      function showSentenceById(sid, slideDirection = 'next') {
        const idx = cardMap.get(sid);
        if (idx !== undefined) {
          showSentenceByIndex(idx, slideDirection);
        }
      }

      function stepSentence(delta) {
        if (starFilterActive && starredIds.size > 0) {
          let i = currentIndex + delta;
          while (i >= 0 && i < totalCards) {
            if (starredIds.has(allCards[i].dataset.id)) {
              showSentenceByIndex(i, delta > 0 ? 'next' : 'prev');
              return;
            }
            i += delta;
          }
          return;
        }
        showSentenceByIndex(currentIndex + delta, delta > 0 ? 'next' : 'prev');
      }

      function stepSection(delta) {
        let curSec = parseInt(currentSectionNum, 10) || 1;
        let targetSec = curSec + delta;
        if (targetSec < 1) targetSec = 1;
        if (targetSec > 45) targetSec = 45;
        const secEl = document.getElementById(`section-${String(targetSec).padStart(2, '0')}`);
        if (secEl) {
          const firstCard = secEl.querySelector('.duo-card');
          if (firstCard && firstCard.dataset.id) {
            showSentenceById(firstCard.dataset.id, delta > 0 ? 'next' : 'prev');
          }
        }
      }

      const navPrevSec = document.getElementById('nav-prev-section');
      if (navPrevSec) navPrevSec.addEventListener('click', () => stepSection(-1));

      const navNextSec = document.getElementById('nav-next-section');
      if (navNextSec) navNextSec.addEventListener('click', () => stepSection(1));
      const topSecBtn = document.getElementById('btn-open-sections-top');
      if (topSecBtn) {
        topSecBtn.addEventListener('click', () => {
          closeAllModals();
          modalSections.classList.add('open');
        });
      }

      // Touch Swipe Listener on Main Content
      const mainEl = document.getElementById('main-content');
      let touchStartX = 0;
      let touchStartY = 0;

      mainEl.addEventListener('touchstart', (e) => {
        if (e.touches.length !== 1) return;
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
      }, { passive: true });

      mainEl.addEventListener('touchend', (e) => {
        if (e.changedTouches.length !== 1) return;
        const dx = e.changedTouches[0].clientX - touchStartX;
        const dy = e.changedTouches[0].clientY - touchStartY;
        if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.4) {
          if (dx < 0) {
            stepSentence(1);
          } else {
            stepSentence(-1);
          }
        }
      }, { passive: true });

      // Keyboard Left/Right support
      document.addEventListener('keydown', (e) => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;
        if (e.key === 'ArrowRight') stepSentence(1);
        if (e.key === 'ArrowLeft') stepSentence(-1);
      });

      // Star filter button
      const btnFilterStar = document.getElementById('btn-filter-star');
      btnFilterStar.addEventListener('click', () => {
        if (starredIds.size === 0) return;
        starFilterActive = !starFilterActive;
        btnFilterStar.classList.toggle('star-active', starFilterActive);
        if (starFilterActive && !starredIds.has(currentSentenceId)) {
          const firstStarred = [...starredIds].sort()[0];
          if (firstStarred) showSentenceById(firstStarred, 'next');
        }
      });

      // =========================================================================
      // STUDY TOOLS & INTEGRATED RED-SHEET MASK
      // =========================================================================
      const btnQuickRedSheet = document.getElementById('btn-quick-redsheet');
      const btnToolRedSheet = document.getElementById('tool-mask-redsheet');
      const btnToolMaskCloze = document.getElementById('tool-mask-cloze');
      const btnToolGender = document.getElementById('tool-highlight-gender');

      function toggleBodyMask(cls, btns) {
        const active = document.body.classList.toggle(cls);
        btns.forEach(b => {
          if (b) {
            b.classList.toggle('active', active);
            b.classList.toggle('star-active', active);
          }
        });
      }

      if (btnQuickRedSheet) {
        btnQuickRedSheet.addEventListener('click', () => toggleBodyMask('mask-redsheet', [btnQuickRedSheet, btnToolRedSheet]));
      }
      if (btnToolRedSheet) {
        btnToolRedSheet.addEventListener('click', () => toggleBodyMask('mask-redsheet', [btnQuickRedSheet, btnToolRedSheet]));
      }
      btnToolMaskCloze.addEventListener('click', () => toggleBodyMask('mask-cloze', [btnToolMaskCloze]));
      btnToolGender.addEventListener('click', () => toggleBodyMask('highlight-gender', [btnToolGender]));

      // =========================================================================
      // AUDIO ENGINE
      // =========================================================================
      function playSentence(sid, forceStart = true, mode = 'single') {
        showSentenceById(sid, 'next');
        currentMode = mode;
        const mp3Path = `audio/sentence_${sid}.mp3`;
        const repMode = dockRepeat.value;
        if (repMode === '3' && forceStart) {
          repeatCountRemaining = 2;
        } else if (forceStart) {
          repeatCountRemaining = 0;
        }
        dockTitle.textContent = `No. ${sid} 再生中`;
        audio.src = mp3Path;
        audio.playbackRate = parseFloat(dockSpeed.value);
        audio.play().catch(() => {});
      }

      audio.addEventListener('play', () => {
        isPlaying = true;
        document.body.classList.add('audio-open');
        dockPlayBtn.textContent = '⏸';
        dockIndicator.classList.add('live');
        document.querySelectorAll('.btn-play-single').forEach(b => {
          b.classList.toggle('playing', currentMode === 'single' && b.dataset.id === currentSentenceId);
        });
      });

      audio.addEventListener('pause', () => {
        isPlaying = false;
        dockPlayBtn.textContent = '▶';
        dockIndicator.classList.remove('live');
        document.querySelectorAll('.btn-play-single').forEach(b => b.classList.remove('playing'));
      });

      audio.addEventListener('ended', () => {
        if (currentMode === 'opus') {
          btnCurrentSecOpus.classList.remove('playing');
          btnCurrentSecOpus.textContent = '▶ 通し';
          return;
        }
        const repMode = dockRepeat.value;
        if (repMode === 'loop') {
          audio.currentTime = 0;
          audio.play();
        } else if (repMode === '3' && repeatCountRemaining > 0) {
          repeatCountRemaining--;
          audio.currentTime = 0;
          audio.play();
        } else if (repMode === 'seq' && currentMode === 'seq') {
          if (currentIndex + 1 < totalCards) {
            const nextSid = allCards[currentIndex + 1].dataset.id;
            playSentence(nextSid, true, 'seq');
          }
        }
      });

      document.addEventListener('click', (e) => {
        const btn = e.target.closest('.btn-play-single');
        if (btn) {
          const sid = btn.dataset.id;
          if (currentSentenceId === sid && isPlaying && currentMode === 'single') {
            audio.pause();
          } else {
            playSentence(sid, true, 'single');
          }
          return;
        }
        const opusBtn = e.target.closest('.btn-section-opus');
        if (opusBtn && btnCurrentSecOpus) {
          btnCurrentSecOpus.click();
        }
      });

      btnCurrentSecOpus.addEventListener('click', () => {
        const opusSrc = btnCurrentSecOpus.dataset.opus;
        const sec = btnCurrentSecOpus.dataset.sec;
        if (currentSectionNum === sec && isPlaying && currentMode === 'opus') {
          audio.pause();
          btnCurrentSecOpus.classList.remove('playing');
          btnCurrentSecOpus.textContent = '▶ 通し';
        } else {
          currentSectionNum = sec;
          currentMode = 'opus';
          dockTitle.textContent = `Sec.${String(sec).padStart(2, '0')} 通し再生中`;
          audio.src = opusSrc;
          audio.playbackRate = parseFloat(dockSpeed.value);
          audio.play().catch(() => {});
          btnCurrentSecOpus.classList.add('playing');
          btnCurrentSecOpus.textContent = '⏸ 停止';
        }
      });

      const btnDockClose = document.getElementById('btn-dock-close');
      if (btnDockClose) {
        btnDockClose.addEventListener('click', () => {
          audio.pause();
          document.body.classList.remove('audio-open');
        });
      }

      dockPlayBtn.addEventListener('click', () => {
        if (!audio.src) {
          const mode = dockRepeat.value === 'seq' ? 'seq' : 'single';
          playSentence(currentSentenceId, true, mode);
          return;
        }
        if (isPlaying) {
          audio.pause();
        } else {
          if (dockRepeat.value === 'seq') currentMode = 'seq';
          audio.play();
        }
      });

      dockPrevBtn.addEventListener('click', () => {
        stepSentence(-1);
        playSentence(currentSentenceId, true, currentMode);
      });

      dockNextBtn.addEventListener('click', () => {
        stepSentence(1);
        playSentence(currentSentenceId, true, currentMode);
      });

      dockRepeat.addEventListener('change', () => {
        if (currentMode !== 'opus') {
          currentMode = dockRepeat.value === 'seq' ? 'seq' : 'single';
        }
      });

      dockSpeed.addEventListener('change', () => {
        audio.playbackRate = parseFloat(dockSpeed.value);
      });

      // =========================================================================
      // MODALS (SECTIONS, INDEX, SEARCH/TOOLS, QUIZ, OPD)
      // =========================================================================
      const modalSections = document.getElementById('modal-sections');
      const modalIndex = document.getElementById('modal-index');
      const modalTools = document.getElementById('modal-tools');
      const modalQuiz = document.getElementById('modal-quiz');

      function closeAllModals() {
        modalSections.classList.remove('open');
        modalIndex.classList.remove('open');
        modalTools.classList.remove('open');
        if (modalQuiz) modalQuiz.classList.remove('open');
      }

      document.getElementById('btn-open-sections').addEventListener('click', () => {
        closeAllModals();
        modalSections.classList.add('open');
      });

      document.getElementById('btn-open-index').addEventListener('click', () => {
        closeAllModals();
        modalIndex.classList.add('open');
        if (!isIndexInitialized) initIndexView();
      });

      document.getElementById('btn-open-tools').addEventListener('click', () => {
        closeAllModals();
        modalTools.classList.add('open');
      });

      document.querySelectorAll('.modal-close, .modal-overlay').forEach(el => {
        el.addEventListener('click', (e) => {
          if (e.target === el || e.target.classList.contains('modal-close')) {
            closeAllModals();
          }
        });
      });

      // Jump from Section TOC or A-Z Index or Search
      document.addEventListener('click', (e) => {
        const secJump = e.target.closest('[data-jump-sid]');
        if (secJump) {
          closeAllModals();
          showSentenceById(secJump.dataset.jumpSid, 'next');
          return;
        }
        const dailyJump = e.target.closest('[data-jump-daily]');
        if (dailyJump) {
          closeAllModals();
          activateDailyTheme(dailyJump.dataset.jumpDaily);
          return;
        }

        const cardJump = e.target.closest('[data-jump]');
        if (cardJump) {
          const targetId = cardJump.dataset.jump;
          if (targetId.startsWith('card-daily-')) {
            const did = targetId.replace('card-daily-', '');
            closeAllModals();
            jumpToDailyWord(did);
            return;
          }
          if (targetId.startsWith('card-')) {
            const sid = targetId.replace('card-', '');
            closeAllModals();
            showSentenceById(sid, 'next');
            return;
          }
        }
      });

      // =========================================================================
      // ULTRA-FAST MONOCHROME A-Z INDEX (500 ITEMS + INFINITE SCROLL)
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

      azTypeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          azTypeBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          currentType = btn.dataset.type;
          updateIndexResults();
        });
      });

      let azSearchTimer = null;
      azSearchInput.addEventListener('input', () => {
        clearTimeout(azSearchTimer);
        azSearchTimer = setTimeout(() => {
          currentQuery = azSearchInput.value;
          updateIndexResults();
        }, 120);
      });

      // =========================================================================
      // FULL SENTENCE & VOCABULARY SEARCH IN TOOLS MODAL
      // =========================================================================
      const searchInput = document.getElementById('global-search');
      const searchClear = document.getElementById('search-clear-btn');
      const searchResultsContainer = document.getElementById('mobile-search-results');
      let globalSearchTimer = null;

      searchInput.addEventListener('input', () => {
        clearTimeout(globalSearchTimer);
        const q = searchInput.value.toLowerCase().trim();
        searchClear.style.display = q ? 'block' : 'none';

        globalSearchTimer = setTimeout(() => {
          if (!q) {
            searchResultsContainer.innerHTML = '';
            return;
          }
          const hits = [];
          for (let i = 0; i < totalCards; i++) {
            const card = allCards[i];
            const fr = (card.querySelector('.french-sentence') || {}).textContent || '';
            const jp = (card.querySelector('.japanese-translation') || {}).textContent || '';
            let matched = fr.toLowerCase().includes(q) || jp.toLowerCase().includes(q);
            if (!matched) {
              const rows = card.querySelectorAll('.word-row');
              for (let r = 0; r < rows.length; r++) {
                if ((rows[r].dataset.search || '').includes(q)) {
                  matched = true;
                  break;
                }
              }
            }
            if (matched) {
              hits.push({ sid: card.dataset.id, sec: card.dataset.sec, fr, jp });
              if (hits.length >= 60) break;
            }
          }

          if (hits.length === 0) {
            searchResultsContainer.innerHTML = '<div style="font-size:0.8rem; color:#64748b; padding:0.5rem;">一致する例文が見つかりませんでした。</div>';
          } else {
            searchResultsContainer.innerHTML = hits.map(h => `
              <div class="search-hit-item" data-jump="card-${h.sid}">
                <div class="search-hit-top">
                  <span>No. ${h.sid}</span>
                  <span>Section ${String(h.sec).padStart(2, '0')}</span>
                </div>
                <div class="search-hit-fr">${escapeHtml(h.fr)}</div>
                <div class="search-hit-jp">${escapeHtml(h.jp)}</div>
              </div>
            `).join('');
          }
        }, 120);
      });

      searchClear.addEventListener('click', () => {
        searchInput.value = '';
        searchInput.dispatchEvent(new Event('input'));
        searchInput.focus();
      });

      // =========================================================================
      // SECTION QUICK 5-QUESTION QUIZ ENGINE
      // =========================================================================
      const quizHeaderTitle = document.getElementById('quiz-header-title');
      const quizContainer = document.getElementById('quiz-container');

      let activeQuizQuestions = [];
      let activeQuizIndex = 0;
      let activeQuizScore = 0;
      let activeQuizSecNum = 1;

      function shuffleArray(arr) {
        const a = [...arr];
        for (let i = a.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [a[i], a[j]] = [a[j], a[i]];
        }
        return a;
      }

      function startSectionQuiz(secNum) {
        activeQuizSecNum = secNum;
        const pool = (typeof SEC_QUIZ_DATA !== 'undefined' && SEC_QUIZ_DATA[secNum]) || [];
        if (pool.length === 0) return;

        // Collect distractor meanings from other words
        const allMeanings = [];
        Object.values(SEC_QUIZ_DATA).forEach(list => {
          list.forEach(item => {
            if (item[2] && !allMeanings.includes(item[2])) allMeanings.push(item[2]);
          });
        });

        const selectedWords = shuffleArray(pool).slice(0, Math.min(5, pool.length));
        activeQuizQuestions = selectedWords.map(target => {
          const lemma = target[0];
          const pos = target[1];
          const correctMeaning = target[2];
          const sid = target[3];

          // Pick 3 distractors
          const distractors = shuffleArray(allMeanings.filter(m => m !== correctMeaning)).slice(0, 3);
          const choices = shuffleArray([correctMeaning, ...distractors]);

          return { lemma, pos, correctMeaning, sid, choices };
        });

        activeQuizIndex = 0;
        activeQuizScore = 0;
        quizHeaderTitle.textContent = `🎯 Section ${String(secNum).padStart(2, '0')} 確認クイズ (全5問)`;
        closeAllModals();
        modalQuiz.classList.add('open');
        renderQuizStep();
      }

      function renderQuizStep() {
        if (activeQuizIndex >= activeQuizQuestions.length) {
          renderQuizResult();
          return;
        }

        const q = activeQuizQuestions[activeQuizIndex];
        const stepNum = activeQuizIndex + 1;
        const totalQ = activeQuizQuestions.length;

        quizContainer.innerHTML = `
          <div class="quiz-progress-text">
            <span>第 ${stepNum} 問 / 全 ${totalQ} 問</span>
            <span>スコア: ${activeQuizScore} 点</span>
          </div>

          <div class="quiz-question-box">
            <div class="quiz-q-word">${escapeHtml(q.lemma)}</div>
            ${q.pos ? `<div class="quiz-q-pos">【${escapeHtml(q.pos)}】</div>` : ''}
          </div>

          <div class="quiz-choices" id="quiz-choices-wrap">
            ${q.choices.map((choice, idx) => `
              <button class="quiz-choice-btn" data-choice="${escapeHtml(choice)}">
                <span class="quiz-choice-num">${idx + 1}.</span>
                <span>${escapeHtml(choice)}</span>
              </button>
            `).join('')}
          </div>

          <div id="quiz-feedback-box" class="quiz-feedback"></div>
          <button id="btn-quiz-next" class="quiz-next-btn">次の問題へ ➔</button>
        `;

        const choicesWrap = document.getElementById('quiz-choices-wrap');
        const feedbackBox = document.getElementById('quiz-feedback-box');
        const nextBtn = document.getElementById('btn-quiz-next');
        let answered = false;

        choicesWrap.querySelectorAll('.quiz-choice-btn').forEach(btn => {
          btn.addEventListener('click', () => {
            if (answered) return;
            answered = true;
            const chosen = btn.dataset.choice;
            const isOk = (chosen === q.correctMeaning);

            if (isOk) {
              activeQuizScore++;
              btn.classList.add('correct');
              feedbackBox.className = 'quiz-feedback show ok';
              feedbackBox.innerHTML = `正解！🎉<br><span style="font-size:0.75rem; color:#166534;">例文 No.${q.sid} に登場した重要語句です。</span>`;
            } else {
              btn.classList.add('incorrect');
              // Highlight the correct one
              choicesWrap.querySelectorAll('.quiz-choice-btn').forEach(b => {
                if (b.dataset.choice === q.correctMeaning) b.classList.add('correct');
              });
              feedbackBox.className = 'quiz-feedback show ng';
              feedbackBox.innerHTML = `不正解… 正解: <strong>${escapeHtml(q.correctMeaning)}</strong><br><span style="font-size:0.75rem; color:#991b1b;">例文 No.${q.sid} を復習してみよう！</span>`;
            }

            nextBtn.classList.add('show');
            if (stepNum === totalQ) {
              nextBtn.textContent = '結果を見る 🏆';
            }
          });
        });

        nextBtn.addEventListener('click', () => {
          activeQuizIndex++;
          renderQuizStep();
        });
      }

      function renderQuizResult() {
        const total = activeQuizQuestions.length;
        const perfect = (activeQuizScore === total);
        let msg = 'よく頑張りました！間違えた単語をカードでチェックしよう。';
        if (perfect) msg = '全問正解！素晴らしい！このセクションは完璧です！🎉';
        else if (activeQuizScore >= 3) msg = '合格ライン突破！要復習の単語を☆マークしておこう。';

        quizContainer.innerHTML = `
          <div class="quiz-result-box">
            <div style="font-size:2.4rem;">${perfect ? '🏆' : (activeQuizScore >= 3 ? '👏' : '💪')}</div>
            <div class="quiz-result-score">${activeQuizScore} / ${total}</div>
            <div class="quiz-result-msg">${msg}</div>
            <div class="quiz-result-actions">
              <button id="btn-quiz-retry" class="quiz-result-btn">もう一度挑戦 🔄</button>
              <button id="btn-quiz-finish" class="quiz-result-btn primary">学習に戻る 📖</button>
            </div>
          </div>
        `;

        document.getElementById('btn-quiz-retry').addEventListener('click', () => {
          startSectionQuiz(activeQuizSecNum);
        });
        document.getElementById('btn-quiz-finish').addEventListener('click', () => {
          closeAllModals();
        });
      }

      // Delegate click for section quiz banner button
      document.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-quiz-sec]');
        if (btn) {
          const sec = parseInt(btn.dataset.quizSec, 10);
          if (sec) startSectionQuiz(sec);
        }
      });

      """ + generate_daily_js() + """
      // Restore last viewed sentence on load
      updateStarUI();
      const savedSid = localStorage.getItem('duo_mobile_last_sid');
      if (savedSid && cardMap.has(savedSid)) {
        showSentenceById(savedSid, 'next');
      } else {
        showSentenceByIndex(0, 'next');
      }
    })();
  </script>
</body>
</html>
""")

    full_html = "".join(html_out)
    with open(OUTPUT_MOBILE_HTML, "w", encoding="utf-8") as f:
        f.write(full_html)

    print("=" * 60)
    print("DUO Français Mobile Web App compiled successfully!")
    print(f"Output File     : {OUTPUT_MOBILE_HTML}")
    print(f"File Size       : {len(full_html) / 1024:.1f} KB ({len(full_html) / 1024 / 1024:.2f} MB)")
    print(f"Total Sentences : {total_sentences} sentences")
    print(f"Total Lemmas    : {total_lemmas} headwords")
    print(f"Total Index     : {len(all_words_index):,} vocabulary items")
    print("=" * 60)


if __name__ == "__main__":
    print("Parsing all 45 section markdown files for Mobile build...")
    sections_data, all_words_index, index_counts, total_sentences, total_lemmas = parse_all_sections()
    generate_mobile_html(sections_data, all_words_index, index_counts, total_sentences, total_lemmas)
