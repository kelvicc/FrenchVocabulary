# -*- coding: utf-8 -*-
"""
DUO Français Section Audio Builder (Review Edition)
Builds section-by-section continuous review audio files replicating DUO 3.0 CD acoustics:
- Intro: 1.2s silence + Title call ("Section X") + 1.3s silence
- Inter-sentence interval: exactly 1.85s pause (golden ratio for shadowing & retention)
- Outro: 2.5s trailing silence
- Default output format: Opus (.opus at 48 kbps) for extreme compression with broadcast quality.
  Also supports AAC (.m4a) and MP3 (.mp3).
"""
import os
import re
import sys
import argparse
import subprocess
import asyncio
import edge_tts

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
SECTIONS_DIR = os.path.join(BASE_DIR, "sections")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
OUT_DIR = os.path.join(BASE_DIR, "audio_sections")
CALL_DIR = os.path.join(OUT_DIR, "_calls")

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(CALL_DIR, exist_ok=True)

# フランス語の数詞（1〜40）
FRENCH_NUMBERS = {
    1: "un", 2: "deux", 3: "trois", 4: "quatre", 5: "cinq",
    6: "six", 7: "sept", 8: "huit", 9: "neuf", 10: "dix",
    11: "onze", 12: "douze", 13: "treize", 14: "quatorze", 15: "quinze",
    16: "seize", 17: "dix-sept", 18: "dix-huit", 19: "dix-neuf", 20: "vingt",
    21: "vingt et un", 22: "vingt-deux", 23: "vingt-trois", 24: "vingt-quatre", 25: "vingt-cinq",
    26: "vingt-six", 27: "vingt-sept", 28: "vingt-huit", 29: "vingt-neuf", 30: "trente",
    31: "trente et un", 32: "trente-deux", 33: "trente-trois", 34: "trente-quatre", 35: "trente-cinq",
    36: "trente-six", 37: "trente-sept", 38: "trente-huit", 39: "trente-neuf", 40: "quarante"
}

CALL_VOICE = "fr-FR-DeniseNeural"

async def ensure_title_call(sec_num):
    """タイトルコール音声を生成・取得"""
    call_file = os.path.join(CALL_DIR, f"call_{sec_num:02d}.mp3")
    if not os.path.exists(call_file) or os.path.getsize(call_file) == 0:
        word = FRENCH_NUMBERS.get(sec_num, str(sec_num))
        text = f"Section {word}."
        comm = edge_tts.Communicate(text, CALL_VOICE, rate="-8%")
        await comm.save(call_file)
    return call_file

def get_section_info():
    """全セクションファイルからセクション番号と含まれる文番号を抽出"""
    sec_files = sorted([f for f in os.listdir(SECTIONS_DIR) if f.startswith("section_") and f.endswith(".md")])
    sections = []
    for fname in sec_files:
        m = re.search(r"section_(\d+)", fname)
        if not m:
            continue
        sec_num = int(m.group(1))
        fpath = os.path.join(SECTIONS_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        sids = [int(s) for s in re.findall(r"###\s+No\.\s*(\d+)", content)]
        sections.append({
            "num": sec_num,
            "filename": fname,
            "sentence_ids": sorted(sids)
        })
    return sorted(sections, key=lambda x: x["num"])

def build_section(sec_info, call_path, output_format="opus", force=False):
    """
    ffmpeg を用いてセクション統合音声を構築
    構成:
    - 冒頭無音: 1.2s
    - タイトルコール: call_path
    - コール後無音: 1.3s
    - 各文（sentence_XXX.mp3）間に 1.85s 無音
    - 末尾無音: 2.5s
    """
    sec_num = sec_info["num"]
    sids = sec_info["sentence_ids"]
    ext = output_format.lower()
    target_filename = f"section_{sec_num:02d}.{ext}"
    target_path = os.path.join(OUT_DIR, target_filename)

    if not force and os.path.exists(target_path) and os.path.getsize(target_path) > 10000:
        print(f"[Section {sec_num:02d}] Already exists, skipping ({target_filename})")
        return True

    # 必要な文音声ファイルの存在チェック
    missing = []
    sentence_files = []
    for sid in sids:
        sp = os.path.join(AUDIO_DIR, f"sentence_{sid:03d}.mp3")
        if not os.path.exists(sp):
            missing.append(sid)
        else:
            sentence_files.append(sp)

    if missing:
        print(f"❌ [Section {sec_num:02d}] Missing sentence audio: {missing}")
        return False

    print(f"🔨 Building Section {sec_num:02d} ({len(sentence_files)} sentences) -> {target_filename}...")

    # ffmpeg コマンド構築
    # 入力ストリームリスト
    cmd = ['ffmpeg', '-y']
    filter_inputs = []
    stream_idx = 0

    # 1. 冒頭無音 0.8s (コールの前置余白と合わさり約1.2s)
    cmd.extend(['-f', 'lavfi', '-t', '0.80', '-i', 'anullsrc=r=24000:cl=mono'])
    filter_inputs.append(f"[{stream_idx}:a]")
    stream_idx += 1

    # 2. タイトルコール
    cmd.extend(['-i', call_path])
    filter_inputs.append(f"[{stream_idx}:a]")
    stream_idx += 1

    # 3. コール後無音 0.8s (コールの後置余白と合わさり約1.3s)
    cmd.extend(['-f', 'lavfi', '-t', '0.80', '-i', 'anullsrc=r=24000:cl=mono'])
    filter_inputs.append(f"[{stream_idx}:a]")
    stream_idx += 1

    # 4. 各文音声 + 例文間 1.10s ポーズ (各文末尾余白と合わさり実測1.85〜1.90s)
    for i, sf in enumerate(sentence_files):
        if i > 0:
            cmd.extend(['-f', 'lavfi', '-t', '1.10', '-i', 'anullsrc=r=24000:cl=mono'])
            filter_inputs.append(f"[{stream_idx}:a]")
            stream_idx += 1
        cmd.extend(['-i', sf])
        filter_inputs.append(f"[{stream_idx}:a]")
        stream_idx += 1

    # 5. 末尾余白 2.0s (最終文余白と合わさり実測2.5s)
    cmd.extend(['-f', 'lavfi', '-t', '2.00', '-i', 'anullsrc=r=24000:cl=mono'])
    filter_inputs.append(f"[{stream_idx}:a]")
    stream_idx += 1

    # concat + loudnorm フィルタ (EBU R128準拠: 本家DUO実測値 -19.0 LUFS に最適化)
    filter_str = "".join(filter_inputs) + f"concat=n={len(filter_inputs)}:v=0:a=1[cat];[cat]loudnorm=I=-19:TP=-1.5:LRA=7[out]"
    cmd.extend(['-filter_complex', filter_str, '-map', '[out]'])

    # コーデック設定
    if ext == "opus":
        cmd.extend(['-c:a', 'libopus', '-b:a', '48k', '-vbr', 'on', '-application', 'voip'])
    elif ext == "m4a":
        cmd.extend(['-c:a', 'aac', '-b:a', '64k', '-ar', '24000', '-ac', '1'])
    elif ext == "mp3":
        cmd.extend(['-c:a', 'libmp3lame', '-b:a', '48k', '-ar', '24000', '-ac', '1'])
    else:
        raise ValueError(f"Unsupported format: {ext}")

    cmd.append(target_path)

    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if res.returncode != 0:
        print(f"❌ ffmpeg failed for Section {sec_num:02d}: {res.stderr.decode('utf-8', errors='ignore')[:300]}")
        return False

    size_kb = os.path.getsize(target_path) / 1024.0
    print(f"✅ [Section {sec_num:02d}] Generated successfully ({size_kb:.1f} KB)")
    return True

async def main():
    parser = argparse.ArgumentParser(description="DUO Français Section Review Audio Builder")
    parser.add_argument("sections", nargs="*", type=int, help="Target section numbers (e.g. 1 2 5). All if omitted.")
    parser.add_argument("--format", default="opus", choices=["opus", "m4a", "mp3"], help="Output audio format (default: opus)")
    parser.add_argument("--force", "-f", action="store_true", help="Force overwrite existing section audio")
    args = parser.parse_args()

    sections = get_section_info()
    if args.sections:
        sections = [s for s in sections if s["num"] in args.sections]

    print("=" * 65)
    print(f"DUO Français Section Audio Builder (Format: {args.format.upper()})")
    print(f"Target: {len(sections)} sections")
    print("=" * 65)

    # 1. タイトルコールの生成・確認
    for s in sections:
        await ensure_title_call(s["num"])

    # 2. 各セクションの結合
    success_count = 0
    for s in sections:
        ok = build_section(s, os.path.join(CALL_DIR, f"call_{s['num']:02d}.mp3"), output_format=args.format, force=args.force)
        if ok:
            success_count += 1

    print("=" * 65)
    print(f"Completed: {success_count}/{len(sections)} sections ready in {OUT_DIR}")
    print("=" * 65)

if __name__ == "__main__":
    asyncio.run(main())
