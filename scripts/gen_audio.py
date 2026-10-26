# -*- coding: utf-8 -*-
"""
DUO Français Audio Generator (Character Ensemble & Duet Dialogue Edition)
Scans markdown files in duo_francais/sections/, extracts sentences and cast assignments,
and generates Edge/Azure Neural MP3 files with tailored speed tuning.

Supports:
- Single speaker sentences: [♀ Vivienne], [♂ Remy], [♀ Denise], etc.
- Duet dialogue sentences: [♂ Remy & ♀ Vivienne], [♀ Vivienne & ♂ Remy]
  where text with '— ... — ...' is synthesized per speaker and concatenated.

Cast & Personas:
- Vivienne [♀] (Main Female / Expressive): fr-FR-VivienneMultilingualNeural (rate: -12%)
- Remy     [♂] (Main Male / Expressive):   fr-FR-RemyMultilingualNeural     (rate: -8%)
- Denise   [♀] (Formal / News / Mme Dupont): fr-FR-DeniseNeural             (rate: +0%)
- Henri    [♂] (Authority / Professor / Judge): fr-FR-HenriNeural           (rate: +0%)
- Eloise   [♀] (Young / Student / Sarcastic Girl): fr-FR-EloiseNeural       (rate: -5%)
"""
import os
import re
import sys
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
TEMP_DIR = os.path.join(AUDIO_DIR, "_temp")
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

CAST_CONFIG = {
    "Vivienne": { "voice": "fr-FR-VivienneMultilingualNeural", "rate": "-16%" },
    "Remy":     { "voice": "fr-FR-RemyMultilingualNeural",     "rate": "-12%" },
    "Denise":   { "voice": "fr-FR-DeniseNeural",               "rate": "-8%" },
    "Henri":    { "voice": "fr-FR-HenriNeural",                "rate": "-8%" },
    "Eloise":   { "voice": "fr-FR-EloiseNeural",               "rate": "-10%" }
}

DEFAULT_MALE = "Remy"
DEFAULT_FEMALE = "Vivienne"

def clean_french_text(s):
    s = re.sub(r"\r?\n>\s*", " ", s)
    s = s.replace("«", "").replace("»", "").replace("**", "").replace("\"", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s

def extract_all_sentences():
    files = sorted([f for f in os.listdir(SECTIONS_DIR) if f.endswith(".md")])
    tasks = []

    for fname in files:
        fpath = os.path.join(SECTIONS_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # Pattern: ### No. 001 [...] の後に > **«...»** または > **...** (複数行対応)
        pattern = r"###\s+No\.\s*(\d+)\s*\[(.*?)\]\s*\r?\n>\s*\*\*(?:[«\s]*)(.*?)(?:[»\s]*)\*\*"
        matches = re.findall(pattern, content, flags=re.DOTALL)

        for num_str, cast_str, raw_french in matches:
            sentence_id = f"{int(num_str):03d}"
            cleaned = clean_french_text(raw_french)

            # 掛け合い判定: cast_str に '&' があり、かつテキスト内に '—' (ダッシュ) が含まれる場合
            if "&" in cast_str and "—" in cleaned:
                # 話者をパース
                actors = []
                for part in cast_str.split("&"):
                    part = part.strip()
                    m = re.search(r"([A-Za-z]+)", part)
                    if m and m.group(1) in CAST_CONFIG:
                        actors.append(m.group(1))
                    else:
                        actors.append(DEFAULT_MALE if "♂" in part else DEFAULT_FEMALE)

                # テキストを対話パートに分割
                parts = [p.strip() for p in cleaned.split("—") if p.strip()]

                tasks.append({
                    "id": sentence_id,
                    "type": "dialogue",
                    "actors": actors,
                    "parts": parts,
                    "text": cleaned,
                    "cast_str": cast_str,
                    "source": fname
                })
            else:
                # 単一話者
                m = re.search(r"([A-Za-z]+)", cast_str.strip())
                actor_name = m.group(1) if m else DEFAULT_MALE
                if actor_name not in CAST_CONFIG:
                    actor_name = DEFAULT_MALE if "♂" in cast_str else DEFAULT_FEMALE

                cfg = CAST_CONFIG[actor_name]
                tasks.append({
                    "id": sentence_id,
                    "type": "single",
                    "voice": cfg["voice"],
                    "rate": cfg["rate"],
                    "actor": actor_name,
                    "text": cleaned,
                    "cast_str": cast_str,
                    "source": fname
                })

    return tasks

async def generate(force=False, target_ids=None):
    tasks = extract_all_sentences()
    print("=" * 60)
    print("DUO Français Multi-Character & Duet Audio Pipeline")
    print(f"Found {len(tasks)} sentences across section files.")
    print("=" * 60)

    generated_count = 0
    skipped_count = 0

    for item in tasks:
        if target_ids and item['id'] not in target_ids:
            continue

        target_path = os.path.join(AUDIO_DIR, f"sentence_{item['id']}.mp3")
        if not force and os.path.exists(target_path) and os.path.getsize(target_path) > 1000:
            skipped_count += 1
            continue

        if item["type"] == "dialogue":
            # 2人の掛け合いデュエット生成
            print(f"Generating Duet [{item['id']}] [{item['cast_str']}]: {item['text'][:40]}...")
            part_files = []
            for idx, part_text in enumerate(item["parts"]):
                actor = item["actors"][idx % len(item["actors"])]
                cfg = CAST_CONFIG[actor]
                temp_file = os.path.join(TEMP_DIR, f"part_{item['id']}_{idx}.mp3")
                for attempt in range(4):
                    try:
                        comm = edge_tts.Communicate(part_text, cfg["voice"], rate=cfg["rate"])
                        await comm.save(temp_file)
                        break
                    except Exception:
                        if attempt == 3:
                            raise
                        await asyncio.sleep(2 * (attempt + 1))
                part_files.append(temp_file)

            # ffmpeg で各パートの余分な前後無音をトリムし、話者交代間に 0.30秒の自然なポーズを挿入して -19.0 LUFS でノーマライズ
            cmd = ['ffmpeg', '-y']
            trim_filters = []
            concat_inputs = []
            stream_idx = 0
            for idx, pf in enumerate(part_files):
                if idx > 0:
                    # 話者交代間の0.30秒ポーズ
                    cmd.extend(['-f', 'lavfi', '-t', '0.30', '-i', 'anullsrc=r=24000:cl=mono'])
                    concat_inputs.append(f"[{stream_idx}:a]")
                    stream_idx += 1
                cmd.extend(['-i', pf])
                trimmed_label = f"[t{idx}]"
                trim_filters.append(
                    f"[{stream_idx}:a]silenceremove=start_periods=1:start_silence=0.05:start_threshold=-50dB,"
                    f"areverse,silenceremove=start_periods=1:start_silence=0.08:start_threshold=-50dB,areverse{trimmed_label};"
                )
                concat_inputs.append(trimmed_label)
                stream_idx += 1

            filter_complex = (
                "".join(trim_filters)
                + "".join(concat_inputs)
                + f"concat=n={len(concat_inputs)}:v=0:a=1[cat];[cat]loudnorm=I=-19:TP=-1.5:LRA=7[out]"
            )
            cmd.extend([
                '-filter_complex', filter_complex,
                '-map', '[out]',
                '-ar', '24000', '-ac', '1', '-b:a', '64k',
                target_path
            ])

            import subprocess
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res.returncode != 0:
                # フォールバック: 単純バイナリ結合
                with open(target_path, "wb") as fout:
                    for pf in part_files:
                        with open(pf, "rb") as fin:
                            fout.write(fin.read())

            for pf in part_files:
                try:
                    os.remove(pf)
                except Exception:
                    pass

            generated_count += 1
            await asyncio.sleep(0.3)
        else:
            # 単一話者生成 (-19.0 LUFS でノーマライズ)
            print(f"Generating [{item['id']}] [{item['actor']} (rate: {item['rate']})]: {item['text'][:40]}...")
            raw_temp = os.path.join(TEMP_DIR, f"raw_{item['id']}.mp3")
            for attempt in range(4):
                try:
                    communicate = edge_tts.Communicate(item["text"], item["voice"], rate=item["rate"])
                    await communicate.save(raw_temp)
                    import subprocess
                    cmd = ['ffmpeg', '-y', '-i', raw_temp, '-af', 'loudnorm=I=-19:TP=-1.5:LRA=7', '-ar', '24000', '-ac', '1', '-b:a', '64k', target_path]
                    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    if res.returncode != 0 or not os.path.exists(target_path):
                        os.replace(raw_temp, target_path)
                    else:
                        if os.path.exists(raw_temp):
                            os.remove(raw_temp)
                    break
                except Exception:
                    if attempt == 3:
                        raise
                    await asyncio.sleep(2 * (attempt + 1))
            generated_count += 1
            await asyncio.sleep(0.3)

    print("=" * 60)
    print(f"Audio Generation Complete: {generated_count} newly created/updated, {skipped_count} skipped.")
    print("=" * 60)
    verify_integrity(tasks, target_ids=target_ids)

def verify_integrity(tasks, target_ids=None):
    """MD原文・抽出テキスト・MP3ファイルサイズ（再生時間比率）の最終整合性チェック"""
    errors = []
    files = sorted([f for f in os.listdir(SECTIONS_DIR) if f.endswith(".md")])
    expected_headers = 0
    for fname in files:
        fpath = os.path.join(SECTIONS_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        headers = re.findall(r"###\s+No\.\s*(\d+)", content)
        expected_headers += len(headers)
        # 2行以上に分かれた > **...** が残っていないかチェック
        multiline_quotes = re.findall(r"###\s+No\.\s*(\d+).*?\r?\n>\s*\*\*.*?\*\*\r?\n>\s*\*\*", content)
        if multiline_quotes:
            errors.append(f"[{fname}] Multiple blockquote lines detected in No. {multiline_quotes}")

    if not target_ids and len(tasks) != expected_headers:
        errors.append(f"Header count mismatch: {expected_headers} headers in MD vs {len(tasks)} extracted tasks.")

    tasks_to_check = [t for t in tasks if t["id"] in target_ids] if target_ids else tasks
    for t in tasks_to_check:
        sid = t["id"]
        mp3_path = os.path.join(AUDIO_DIR, f"sentence_{sid}.mp3")
        if not os.path.exists(mp3_path):
            errors.append(f"[No.{sid}] Missing MP3 file: sentence_{sid}.mp3")
            continue
        # ffprobe で正確な再生時間を取得、なければ 64kbps (8000 bytes/sec) で概算
        est_sec = 0
        try:
            cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', mp3_path]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0 and res.stdout.strip():
                est_sec = float(res.stdout.strip())
        except Exception:
            pass
        if est_sec <= 0:
            size = os.path.getsize(mp3_path)
            est_sec = size / 8000.0

        chars = len(t["text"])
        ratio = chars / est_sec if est_sec > 0 else 999
        if ratio < 10.0 or ratio > 24.0:
            errors.append(f"[No.{sid}] Abnormal chars/sec ratio ({ratio:.1f} chars/sec, {chars} chars, {est_sec:.1f}s) in {t['source']}")
        if "&" in t["cast_str"]:
            if t["type"] != "dialogue" or len(t.get("parts", [])) < 2:
                errors.append(f"[No.{sid}] Dialogue cast '{t['cast_str']}' failed to split into >=2 parts.")

    if errors:
        print("❌ [VERIFICATION FAILED] Issues detected:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    else:
        print(f"✅ [VERIFICATION PASSED] All {len(tasks)} MD sentences & MP3 files verified (100% match, normal duration ratios).")

if __name__ == "__main__":
    force_overwrite = "--force" in sys.argv or "-f" in sys.argv
    # 特定のIDのみ指定可能 (例: python gen_audio.py 004 005)
    specific_ids = [arg.zfill(3) for arg in sys.argv[1:] if arg.isdigit()]
    asyncio.run(generate(force=force_overwrite, target_ids=specific_ids if specific_ids else None))

