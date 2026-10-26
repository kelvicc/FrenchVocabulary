import re

with open('sections/section_12.md', 'r', encoding='utf-8') as f:
    content = f.read()

def repl(match):
    old_num = int(match.group(1))
    new_num = old_num - 13
    return f"- **{new_num:04d} |"

new_content = re.sub(r'- \*\*(\d{4}) \|', repl, content)

with open('sections/section_12.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated section_12.md numbers from 0545..0576 to 0532..0563.")
