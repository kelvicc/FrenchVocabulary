import os
import re

SECTIONS_DIR = "sections"
offset = 12

for sec in range(27, 31):
    fpath = os.path.join(SECTIONS_DIR, f"section_{sec}.md")
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    def shift_header(m):
        start_n = int(m.group(1)) + offset
        end_n = int(m.group(2)) + offset
        return f"(No. {start_n:03d} – No. {end_n:03d})"

    content = re.sub(r"\(No\.\s*(\d+)\s*[–-]\s*No\.\s*(\d+)\)", shift_header, content)

    def shift_no(m):
        n = int(m.group(1)) + offset
        return f"### No. {n:03d}"

    content = re.sub(r"###\s+No\.\s*(\d+)", shift_no, content)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Shifted section_{sec}.md by +{offset}")
