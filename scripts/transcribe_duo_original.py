import os
import subprocess
import glob

whisper_exe = r"c:\Users\noid\Documents\antigravity\kind-fermi\tools\whisper.cpp\Release\whisper-cli.exe"
model_bin = r"c:\Users\noid\Documents\antigravity\kind-fermi\tools\whisper.cpp\models\ggml-base.en.bin"
audio_dir = r"Duo3.0 original\DUO audio"
out_dir = r"Duo3.0 original\transcripts"
os.makedirs(out_dir, exist_ok=True)

files = sorted(glob.glob(os.path.join(audio_dir, "*.mp3")))
print(f"Found {len(files)} audio files to transcribe.")

for f in files:
    base = os.path.splitext(os.path.basename(f))[0]
    out_txt = os.path.join(out_dir, f"{base}.txt")
    if os.path.exists(out_txt):
        print(f"Skipping {base} (already exists)")
        continue
    print(f"Transcribing {base}...")
    cmd = [whisper_exe, "-m", model_bin, "-f", f, "-nt"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    lines = res.stdout.strip()
    with open(out_txt, "w", encoding="utf-8") as fp:
        fp.write(lines)
    print(f"Saved: {out_txt}")

print("All sections transcribed successfully!")
