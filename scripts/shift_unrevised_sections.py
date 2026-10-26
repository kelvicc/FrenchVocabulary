import os
import re

SECTIONS_DIR = "sections"

# Section 21 から Section 30 までの文番号を +8 シフト
offset = 8

for sec in range(21, 31):
    fpath = os.path.join(SECTIONS_DIR, f"section_{sec}.md")
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # タイトル行の (No. XXX – No. YYY) を置換
    def shift_header(m):
        start_n = int(m.group(1)) + offset
        end_n = int(m.group(2)) + offset
        return f"(No. {start_n} – No. {end_n})"

    content = re.sub(r"\(No\.\s*(\d+)\s*[–-]\s*No\.\s*(\d+)\)", shift_header, content)

    # 各文の見出し ### No. XXX を置換
    def shift_no(m):
        n = int(m.group(1)) + offset
        return f"### No. {n:03d}"

    content = re.sub(r"###\s+No\.\s*(\d+)", shift_no, content)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Shifted section_{sec}.md by +{offset}")
