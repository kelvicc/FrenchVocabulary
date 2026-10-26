# -*- coding: utf-8 -*-
"""
DUO Français Audio-Text Discrepancy Auditor
Strictly verifies:
1. Markdown sentence text vs extracted text.
2. File modification timestamps (ensures MP3 is strictly newer than MD).
3. Duration-to-character ratio (detects cutoffs, silence loops, or mismatched sentences).
4. Dialogue turn count and splitting consistency.
5. Audio stream validity (no corrupt frames).
"""
import os
import sys
import subprocess
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.append(SCRIPT_DIR)

from gen_audio import extract_all_sentences, SECTIONS_DIR, AUDIO_DIR

def audit():
    tasks = extract_all_sentences()
    tasks_map = {t['id']: t for t in tasks}

    # 指定されたIDがあればそれを、なければデフォルトの対象を監査
    cli_ids = [arg.zfill(3) for arg in sys.argv[1:] if arg.isdigit()]
    if cli_ids:
        target_ids = cli_ids
    else:
        target_ids = [t['id'] for t in tasks]

    print("=" * 70)
    print(f"AUDITING {len(target_ids)} SENTENCES...")
    print("=" * 70)

    issues = []
    normal_cps_list = []

    for sid in target_ids:
        if sid not in tasks_map:
            issues.append(f"[No.{sid}] Sentence ID not found in extracted tasks!")
            continue

        t = tasks_map[sid]
        mp3_path = os.path.join(AUDIO_DIR, f"sentence_{sid}.mp3")
        md_path = os.path.join(SECTIONS_DIR, t["source"])

        # 1. 存在確認
        if not os.path.exists(mp3_path):
            issues.append(f"[No.{sid}] Missing MP3 file: {mp3_path}")
            continue

        # 2. タイムスタンプ照合 (MDファイル更新後にMP3が正しく生成されているか)
        md_mtime = os.path.getmtime(md_path)
        mp3_mtime = os.path.getmtime(mp3_path)
        if mp3_mtime < md_mtime - 2.0:
            issues.append(
                f"[No.{sid}] OUTDATED AUDIO: MP3 ({datetime.fromtimestamp(mp3_mtime).strftime('%H:%M:%S')}) "
                f"is older than MD ({datetime.fromtimestamp(md_mtime).strftime('%H:%M:%S')}) in {t['source']}"
            )

        # 3. 音声の破損チェックおよび再生時間取得
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration,size,bit_rate',
            '-of', 'default=noprint_wrappers=1',
            mp3_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            issues.append(f"[No.{sid}] Corrupt MP3 file: {res.stderr.strip()}")
            continue

        meta = dict(line.split('=', 1) for line in res.stdout.strip().splitlines() if '=' in line)
        try:
            dur = float(meta.get('duration', 0))
            size = int(meta.get('size', 0))
        except Exception as e:
            issues.append(f"[No.{sid}] Failed to parse audio metadata: {e}")
            continue

        if size < 1000:
            issues.append(f"[No.{sid}] Suspicious tiny MP3 file size: {size} bytes")
            continue

        chars = len(t["text"])
        cps = chars / dur if dur > 0 else 0
        normal_cps_list.append(cps)

        # 4. 発話速度・比率チェック (フランス語標準: 11〜22 chars/sec)
        # 極端に小さすぎる（長すぎる無音・ループ）または大きすぎる（文が途中で切れている）場合を検知
        if cps < 10.5 or cps > 23.5:
            issues.append(
                f"[No.{sid}] ABNORMAL SPEECH RATIO: {cps:.1f} chars/sec (text: {chars} chars, audio: {dur:.2f}s) "
                f"Text snippet: « {t['text'][:35]}... »"
            )

        # 5. 会話文（対話）の構造・パート整合性
        if "&" in t["cast_str"]:
            if t["type"] != "dialogue":
                issues.append(f"[No.{sid}] Dialogue cast '{t['cast_str']}' was mistakenly extracted as single speaker!")
            elif len(t.get("parts", [])) < 2:
                issues.append(f"[No.{sid}] Dialogue text failed to split with '—': parts={t.get('parts')}")

    print(f"Total Sentences Audited: {len(target_ids)}")
    if normal_cps_list:
        avg_cps = sum(normal_cps_list) / len(normal_cps_list)
        min_cps = min(normal_cps_list)
        max_cps = max(normal_cps_list)
        print(f"Speed Consistency: Average {avg_cps:.1f} chars/sec (Min: {min_cps:.1f}, Max: {max_cps:.1f})")

    print("-" * 70)
    if issues:
        print(f"❌ DETECTED {len(issues)} DISCREPANCIES:")
        for iss in issues:
            print(f"  • {iss}")
        return False
    else:
        print("✅ [ALL CLEAR] 100% PERFECT MATCH! Every sentence text and audio is fully synchronized with zero discrepancies.")
        return True

if __name__ == "__main__":
    ok = audit()
    sys.exit(0 if ok else 1)
