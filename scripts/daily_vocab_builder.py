# -*- coding: utf-8 -*-
"""
daily_vocab_builder.py
Generates HTML, CSS, Index entries, and TOC cards for the Everyday Vocabulary Part (336 words, 8 themes).
Designed to be integrated cleanly and seamlessly into build_mobile_app.py and build_web_app.py.
"""
import os, sys, re, unicodedata, html
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
from parse_daily_vocab import load_daily_vocab_data, get_initial_letter, get_clean_lemma

def escape_html(text):
    return html.escape(str(text)) if text else ""

def get_daily_index_entries(themes):
    """
    Returns a list of index items formatted for compact_index_data:
    [word, type, pos, meaning, sid, letter]
    """
    entries = []
    for t in themes:
        for g in t["groups"]:
            for w in g["words"]:
                lemma = get_clean_lemma(w["french"])
                initial = get_initial_letter(lemma)
                entries.append([
                    lemma,
                    "日常",
                    w["gender"],
                    w["meaning"],
                    f"daily-{w['did']}",
                    initial
                ])
                # If there are aliases like "le frigo / le réfrigérateur"
                variants = [v.strip() for v in w["french"].split("/")]
                if len(variants) > 1:
                    for v in variants[1:]:
                        v_lemma = get_clean_lemma(v)
                        v_initial = get_initial_letter(v_lemma)
                        entries.append([
                            v_lemma,
                            "日常",
                            w["gender"],
                            f"{w['meaning']} (={variants[0]})",
                            f"daily-{w['did']}",
                            v_initial
                        ])
    return entries

def generate_daily_css():
    """Returns CSS styles for the Everyday Vocabulary Part."""
    return """
    /* =========================================================================
       EVERYDAY VOCABULARY PART (CONTIGUOUS SECTIONS & EMERALD PALETTE)
       ========================================================================= */
    .daily-theme-container {
      margin-bottom: 2.5rem;
      scroll-margin-top: 100px;
    }
    .daily-theme-header-card {
      background: linear-gradient(135deg, #064e3b 0%, #047857 55%, #059669 100%);
      color: #ffffff;
      border-radius: 14px;
      padding: 16px 18px;
      margin-bottom: 14px;
      box-shadow: 0 4px 14px rgba(5, 150, 105, 0.22);
      border: 1px solid rgba(167, 243, 208, 0.25);
    }
    .daily-badge-theme {
      background: #a7f3d0;
      color: #064e3b;
      font-size: 10px;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 4px;
      letter-spacing: 0.6px;
      display: inline-block;
    }
    .daily-back-btn {
      background: rgba(255, 255, 255, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.45);
      color: #ffffff;
      padding: 3px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      transition: background 0.15s, transform 0.1s;
    }
    .daily-back-btn:hover {
      background: rgba(255, 255, 255, 0.35);
      transform: translateY(-1px);
    }
    .daily-theme-title {
      font-size: 18px;
      font-weight: 800;
      margin: 4px 0 2px;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .daily-theme-sub {
      font-size: 12px;
      color: #d1fae5;
    }
    .daily-theme-stats {
      display: flex;
      gap: 12px;
      margin-top: 8px;
      font-size: 11px;
      font-weight: 600;
      color: #a7f3d0;
    }

    /* Sub-group Card */
    .daily-group-box {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      margin-bottom: 14px;
      overflow: hidden;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .daily-group-header {
      background: #f1f5f9;
      padding: 8px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #e2e8f0;
    }
    .daily-group-badge {
      background: #0f766e;
      color: #ffffff;
      font-size: 11px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;
    }
    .daily-group-count {
      font-size: 11px;
      color: #64748b;
      font-weight: 600;
    }

    /* Word Rows */
    .daily-word-row {
      padding: 9px 12px;
      border-bottom: 1px solid #f1f5f9;
      display: flex;
      align-items: flex-start;
      gap: 8px;
      transition: background-color 0.15s ease;
      scroll-margin-top: 140px;
    }
    .daily-word-row:last-child { border-bottom: none; }
    .daily-word-row:hover { background-color: #f8fafc; }
    .daily-word-row.is-checked { opacity: 0.45; background-color: #f8fafc; }
    .daily-word-row.flash-highlight {
      animation: dailyRowFlash 2.5s ease;
    }
    @keyframes dailyRowFlash {
      0% { background-color: #a7f3d0; box-shadow: inset 0 0 0 2px #059669; }
      50% { background-color: #d1fae5; }
      100% { background-color: transparent; }
    }

    .daily-word-check {
      width: 16px;
      height: 16px;
      cursor: pointer;
      accent-color: #059669;
      flex-shrink: 0;
      margin-top: 3px;
    }
    .daily-tag-gender {
      font-size: 10px;
      font-weight: 700;
      padding: 1px 5px;
      border-radius: 3px;
      flex-shrink: 0;
      margin-top: 2px;
    }
    .daily-tag-gender.masc { background: #dbeafe; color: #1d4ed8; }
    .daily-tag-gender.fem { background: #fce7f3; color: #db2777; }

    .daily-word-content {
      flex: 1;
      min-width: 0;
    }
    .daily-top-line {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 8px;
      width: 100%;
    }
    .daily-french {
      font-size: 15px;
      font-weight: 700;
      color: #0f172a;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .daily-btn-audio {
      background: none;
      border: none;
      cursor: pointer;
      font-size: 13px;
      padding: 0 3px;
      opacity: 0.6;
      line-height: 1;
      transition: opacity 0.15s, transform 0.1s;
    }
    .daily-btn-audio:hover { opacity: 1; transform: scale(1.15); }

    .daily-meaning {
      font-size: 14px;
      font-weight: 600;
      color: #334155;
      text-align: right;
    }

    .daily-sub-note {
      font-size: 11px;
      color: #0284c7;
      margin-top: 2px;
      padding-left: 2px;
    }
    .daily-sub-phrase {
      font-size: 11px;
      color: #475569;
      margin-top: 2px;
      padding-left: 2px;
    }
    .daily-sub-phrase b { color: #1e293b; }

    /* Red Sheet masking for daily words */
    body.red-sheet-active .daily-meaning .red-text,
    .mask-redsheet .daily-meaning .red-text {
      background-color: #ef4444 !important;
      color: #ef4444 !important;
      border-radius: 3px;
      user-select: none;
    }

    /* Check Banner */
    .daily-check-banner {
      background: #ecfdf5;
      border-top: 1px dashed #6ee7b7;
      padding: 8px 12px;
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 11px;
    }
    .daily-check-badge {
      background: #059669;
      color: #fff;
      font-size: 9px;
      font-weight: 800;
      padding: 1px 5px;
      border-radius: 3px;
    }
    .daily-check-q { color: #065f46; flex: 1; font-weight: 600; }
    .daily-check-btn {
      background: #d1fae5;
      border: 1px solid #a7f3d0;
      color: #065f46;
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      cursor: pointer;
    }

    /* TOC Daily Section Block */
    .daily-toc-divider {
      grid-column: 1 / -1;
      margin-top: 1.5rem;
      margin-bottom: 0.5rem;
      padding: 10px 14px;
      background: #ecfdf5;
      border: 1px solid #a7f3d0;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .daily-toc-divider-title {
      font-size: 13px;
      font-weight: 800;
      color: #065f46;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .daily-jump-card {
      border-left: 4px solid #059669 !important;
      background: #ffffff;
    }
    .daily-jump-card:hover {
      border-color: #059669 !important;
      background: #f0fdf4 !important;
    }
    .daily-jump-badge {
      font-size: 10px;
      font-weight: 800;
      color: #059669;
      letter-spacing: 0.5px;
    }

    /* Index tag for daily vocabulary */
    .index-tag-type.tag-daily {
      background: #059669 !important;
      color: #ffffff !important;
      font-weight: 700;
      border-radius: 3px;
      padding: 1px 5px;
    }
    """

def generate_daily_sections_html(themes, is_mobile=False):
    """
    Generates HTML section containers for all daily themes.
    """
    html_buffer = []
    for t in themes:
        num = t["num"]
        total_w = sum(len(g["words"]) for g in t["groups"])
        sec_id = f"section-daily-{num:02d}"
        data_sec = f"D{num}"
        subtitle = t["title_ja"]
        title_fr = t["title_fr"]

        html_buffer.append(f"""
    <!-- DAILY VOCABULARY THEME {num:02d} -->
    <section class="section-container daily-theme-container" id="{sec_id}" data-sec="{data_sec}" data-subtitle="{subtitle}" data-daily-num="{num}">
      <div class="daily-theme-header-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
          <span class="daily-badge-theme">日常語 THEME {num:02d}</span>
          <button class="daily-back-btn" onclick="if (typeof showSentenceById === 'function') {{ showSentenceById(currentSentenceId || '001', 'next'); }} else {{ const el = document.getElementById('section-01'); if (el) el.scrollIntoView({{behavior:'smooth'}}); }}">← DUO本編に戻る</button>
        </div>
        <h2 class="daily-theme-title">🌿 {subtitle}</h2>
        <div class="daily-theme-sub">{title_fr}</div>
        <div class="daily-theme-stats">
          <span>全 {total_w} 語</span>
          <span>•</span>
          <span>{len(t['groups'])} グループ構成</span>
          <span>•</span>
          <span class="theme-mastery-stat" data-theme-stat="{num}">習得: 0 / {total_w}</span>
        </div>
      </div>
""")

        for g in t["groups"]:
            code = g["code"]
            g_title = g["title_ja"]
            g_fr = g["title_fr"]
            w_list = g["words"]

            html_buffer.append(f"""
      <article class="daily-group-box" id="daily-group-{code}">
        <div class="daily-group-header">
          <div style="display:flex; align-items:center; gap:6px;">
            <span class="daily-group-badge">{code}. {escape_html(g_title)}</span>
            <span class="daily-group-count">{len(w_list)} 語</span>
          </div>
          <button class="daily-btn-audio" style="font-size:11px; padding:2px 6px; background:#fff; border:1px solid #cbd5e1; border-radius:4px; font-weight:600;" onclick="playDailyGroupAudio('{code}')">🔊 連続再生</button>
        </div>
""")

            for w in w_list:
                did = w["did"]
                fr = escape_html(w["french"])
                gender = w["gender"]
                gender_cls = "fem" if "女" in gender else "masc"
                meaning = escape_html(w["meaning"])
                clean_fr_speak = w["french"].split("/")[0].strip()

                phrase_html = ""
                if w.get("phrase_fr"):
                    phrase_fr = escape_html(w["phrase_fr"])
                    phrase_ja = escape_html(w["phrase_ja"])
                    phrase_html = f'<div class="daily-sub-phrase">▶ <b>{phrase_fr}</b> ({phrase_ja})</div>'

                note_html = ""
                if w.get("note"):
                    note_html = f'<div class="daily-sub-note">★ {escape_html(w["note"])}</div>'

                html_buffer.append(f"""
        <div class="daily-word-row" id="daily-word-{did}" data-did="{did}">
          <input type="checkbox" class="daily-word-check" onchange="onDailyCheckChange(this)">
          <span class="daily-tag-gender {gender_cls}">{gender}</span>
          <div class="daily-word-content">
            <div class="daily-top-line">
              <span class="daily-french">
                {fr}
                <button class="daily-btn-audio" title="発音を聞く" data-speak="{escape_html(clean_fr_speak)}" onclick="playDailyWord(this.dataset.speak)">🔊</button>
              </span>
              <span class="daily-meaning"><span class="red-text">{meaning}</span></span>
            </div>
            {phrase_html}
            {note_html}
          </div>
        </div>
""")

            if g.get("check"):
                chk = g["check"]
                q = escape_html(chk["q"])
                ans = escape_html(chk["ans"])
                expl = escape_html(chk["expl"])
                alert_text = escape_html(f"正解: {ans} ({expl})")
                html_buffer.append(f"""
        <div class="daily-check-banner">
          <span class="daily-check-badge">Check!</span>
          <span class="daily-check-q">{q}</span>
          <button class="daily-check-btn" data-expl="{alert_text}" onclick="alert(this.dataset.expl)">解答</button>
        </div>
""")

            html_buffer.append("""      </article>\n""")

        html_buffer.append("""    </section>\n""")

    return "".join(html_buffer)

def generate_daily_toc_html(themes):
    """Generates the Table of Contents block for Daily Vocabulary in modal-sections."""
    html_buffer = ["""
          <!-- DAILY VOCABULARY TOC DIVIDER & GRID -->
          <div class="daily-toc-divider">
            <span class="daily-toc-divider-title">🌿 日常語・生活必須単語集（全8テーマ・336語）</span>
            <span style="font-size:11px; font-weight:700; color:#065f46;">本編未登場の生活単語を完全網羅</span>
          </div>
"""]
    for t in themes:
        num = t["num"]
        total_w = sum(len(g["words"]) for g in t["groups"])
        sub_desc = "・".join(g["title_ja"].split("・")[0] for g in t["groups"][:3])
        sec_id = f"section-daily-{num:02d}"

        html_buffer.append(f"""
          <div class="sec-jump-card daily-jump-card" data-jump-daily="{sec_id}">
            <div class="daily-jump-badge">THEME {num:02d}</div>
            <div class="sec-jump-num" style="color:#065f46;">{t['title_ja']} ({total_w}語)</div>
            <div class="sec-jump-sub">{sub_desc}</div>
          </div>
""")
    return "".join(html_buffer)

def generate_daily_js():
    """Generates JS logic for speech, sequential audio, checks, and jumps."""
    return """
    // =========================================================================
    // DAILY VOCABULARY ENGINE (336 WORDS CONTIGUOUS JUMPS & AUDIO)
    // =========================================================================
    function playDailyWord(text) {
      if (!window.speechSynthesis) return;
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text);
      u.lang = 'fr-FR';
      u.rate = 0.95;
      window.speechSynthesis.speak(u);
    }

    async function playDailyGroupAudio(code) {
      const groupEl = document.getElementById('daily-group-' + code);
      if (!groupEl) return;
      const rows = groupEl.querySelectorAll('.daily-word-row');
      for (const row of rows) {
        const fr = row.querySelector('.daily-french').innerText.split('/')[0].trim();
        playDailyWord(fr);
        row.classList.add('flash-highlight');
        await new Promise(r => setTimeout(r, 1500));
        row.classList.remove('flash-highlight');
      }
    }

    // Persist daily checkboxes in localStorage
    function getDailyMasterySet() {
      try {
        const raw = localStorage.getItem('duo_daily_mastery');
        return raw ? new Set(JSON.parse(raw)) : new Set();
      } catch(e) { return new Set(); }
    }
    function saveDailyMasterySet(setObj) {
      try {
        localStorage.setItem('duo_daily_mastery', JSON.stringify(Array.from(setObj)));
      } catch(e) {}
    }

    function initDailyMasteryUI() {
      const setObj = getDailyMasterySet();
      document.querySelectorAll('.daily-word-row').forEach(row => {
        const did = row.dataset.did;
        if (setObj.has(did)) {
          const cb = row.querySelector('.daily-word-check');
          if (cb) cb.checked = true;
          row.classList.add('is-checked');
        }
      });
      updateDailyStats();
    }

    function onDailyCheckChange(cb) {
      const row = cb.closest('.daily-word-row');
      const did = row.dataset.did;
      const setObj = getDailyMasterySet();
      if (cb.checked) {
        setObj.add(did);
        row.classList.add('is-checked');
      } else {
        setObj.delete(did);
        row.classList.remove('is-checked');
      }
      saveDailyMasterySet(setObj);
      updateDailyStats();
    }

    function updateDailyStats() {
      const setObj = getDailyMasterySet();
      document.querySelectorAll('.daily-theme-container').forEach(sec => {
        const total = sec.querySelectorAll('.daily-word-row').length;
        const checked = sec.querySelectorAll('.daily-word-check:checked').length;
        const statEl = sec.querySelector('.theme-mastery-stat');
        if (statEl) {
          statEl.textContent = `習得: ${checked} / ${total}`;
        }
      });
    }

    function jumpToDailyWord(did) {
      const row = document.getElementById('daily-word-' + did);
      if (!row) return;
      const sec = row.closest('.section-container');
      if (sec) {
        document.querySelectorAll('.section-container').forEach(s => s.classList.remove('active-sec'));
        sec.classList.add('active-sec');
        const badge = document.getElementById('current-sec-badge');
        if (badge) {
          badge.textContent = `日常語 D${sec.dataset.dailyNum || ''}`;
        }
      }
      setTimeout(() => {
        row.scrollIntoView({ behavior: 'smooth', block: 'center' });
        row.classList.add('flash-highlight');
        setTimeout(() => row.classList.remove('flash-highlight'), 2600);
      }, 100);
    }

    function activateDailyTheme(targetSecId) {
      const sec = document.getElementById(targetSecId);
      if (!sec) return;
      document.querySelectorAll('.section-container').forEach(s => s.classList.remove('active-sec'));
      sec.classList.add('active-sec');
      const badge = document.getElementById('current-sec-badge');
      if (badge) {
        badge.textContent = `日常語 D${sec.dataset.dailyNum || ''}`;
      }
      sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initDailyMasteryUI);
    } else {
      initDailyMasteryUI();
    }
    """
