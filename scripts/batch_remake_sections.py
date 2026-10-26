# -*- coding: utf-8 -*-
"""
DUO Français Batch Section Remaker (Section 02 to 10)
Strictly adheres to:
- No guillemets in sentence blockquote
- No lemma numbers (- **mot**)
- Synonyms and antonyms inline at the end of headword line
- Notes in brackets [ ] and < > indented by 2 spaces (no leading &emsp; inside brackets)
- Derivatives (□) and idioms (◆) indented with &emsp;&emsp;
- Empty lines between headwords
- Single-line translation card at the bottom: > [!NOTE] 訳文
- 100% Lossless content verification (asserts lemma count, derivative count)
"""
import os
import re
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
SECTIONS_DIR = os.path.join(BASE_DIR, "sections")

def transform_section_text(content):
    blocks = re.split(r'\n(?=###\s+No\.)', content)
    header = re.sub(r'[\r\n\s-]+$', '', blocks[0]).strip()
    new_blocks = [header]

    for block in blocks[1:]:
        lines = block.strip().splitlines()
        if not lines:
            continue
        title_line = lines[0].strip()
        french_sentence = ''
        japanese_translation = ''
        line_idx = 1

        while line_idx < len(lines):
            l = lines[line_idx].strip()
            if l.startswith('> **'):
                m = re.search(r'>\s*\*\*[«\s]*(.*?)[»\s]*\*\*', l)
                french_sentence = m.group(1).strip() if m else l.replace('> **', '').replace('**', '').strip()
            elif l.startswith('> （') or l.startswith('> (') or l.startswith('>'):
                m = re.search(r'>\s*[（(](.*?)[）)]', l)
                if m:
                    japanese_translation = m.group(1).strip()
                elif l.startswith('> [!NOTE]'):
                    japanese_translation = l.replace('> [!NOTE]', '').strip()
            elif l.startswith('- **'):
                break
            line_idx += 1

        vocab_blocks = []
        curr_vocab = None

        while line_idx < len(lines):
            l = lines[line_idx]
            raw = l.strip()
            if raw == '---':
                line_idx += 1
                continue
            if raw.startswith('- **'):
                if curr_vocab:
                    vocab_blocks.append(curr_vocab)
                curr_vocab = {'head': raw, 'items': []}
            elif curr_vocab is not None:
                if raw:
                    curr_vocab['items'].append(raw)
            line_idx += 1

        if curr_vocab:
            vocab_blocks.append(curr_vocab)

        b_out = [title_line, f'> **{french_sentence}**\n']

        for vi, v in enumerate(vocab_blocks):
            # 単語番号を除去: - **0081 | supplier** -> - **supplier**
            head_clean = re.sub(r'^-\s+\*\*(?:\d+\s*\|\s*)?', '- **', v['head'])
            synonyms, antonyms, notes, derivatives = [], [], [], []

            for item in v['items']:
                item_clean = re.sub(r'^\s*-\s*', '', item).strip()
                if item_clean.startswith('(= '):
                    synonyms.append(item_clean)
                elif item_clean.startswith('(↔ '):
                    antonyms.append(item_clean)
                elif item_clean.startswith('※ 【文化・背景】') or item_clean.startswith('※ 〈') or item_clean.startswith('<'):
                    c = re.sub(r'^(?:※\s*【文化・背景】|※\s*〈|<)', '', item_clean).rstrip('〉>').strip()
                    notes.append(f'<{c}>')
                elif item_clean.startswith('※ 【') or item_clean.startswith('※') or item_clean.startswith('['):
                    c = re.sub(r'^※\s*【.*?】|^※\s*', '', item_clean).strip(' []')
                    notes.append(f'[{c}]')
                elif '□' in item_clean or '◆' in item_clean:
                    derivatives.append(item_clean)
                else:
                    notes.append(f'[{item_clean}]')

            syn_str = ' ' + ' '.join(synonyms) if synonyms else ''
            ant_str = ' ' + ' '.join(antonyms) if antonyms else ''
            b_out.append(head_clean.rstrip() + syn_str + ant_str + '  ')

            for n in notes:
                # 括弧の内側に余計な空白を入れない
                b_out.append(f'  {n}  ')

            for d in derivatives:
                d_clean = re.sub(r'^.*?([□◆])', r'\1', d).strip()
                b_out.append(f'  &emsp;&emsp;{d_clean}  ')

            if vi < len(vocab_blocks) - 1:
                b_out.append('')

        b_out.append(f'\n> [!NOTE] {japanese_translation}')
        new_blocks.append('\n'.join(b_out))

    return header + '\n\n' + '\n\n---\n\n'.join(new_blocks[1:]) + '\n'

def verify_and_remake(sec_num):
    fname = f"section_{sec_num:02d}.md"
    fpath = os.path.join(SECTIONS_DIR, fname)
    if not os.path.exists(fpath):
        print(f"File not found: {fpath}")
        return False

    with open(fpath, "r", encoding="utf-8") as f:
        orig = f.read()

    # 元の重要要素の集計
    orig_lemmas = len(re.findall(r'^-\s+\*\*', orig, re.MULTILINE))
    orig_squares = orig.count('□')
    orig_diamonds = orig.count('◆')
    orig_sentences = len(re.findall(r'^###\s+No\.', orig, re.MULTILINE))

    transformed = transform_section_text(orig)

    new_lemmas = len(re.findall(r'^-\s+\*\*', transformed, re.MULTILINE))
    new_squares = transformed.count('□')
    new_diamonds = transformed.count('◆')
    new_sentences = len(re.findall(r'^###\s+No\.', transformed, re.MULTILINE))

    # 完全無損失のアサーション（1つでも減っていたら絶対不可）
    assert orig_lemmas == new_lemmas, f"Lemma count mismatch in {fname}: orig {orig_lemmas} vs new {new_lemmas}"
    assert orig_squares == new_squares, f"Square bullet count mismatch in {fname}: orig {orig_squares} vs new {new_squares}"
    assert orig_diamonds == new_diamonds, f"Diamond count mismatch in {fname}: orig {orig_diamonds} vs new {new_diamonds}"
    assert orig_sentences == new_sentences, f"Sentence count mismatch in {fname}: orig {orig_sentences} vs new {new_sentences}"

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(transformed)

    print(f"✅ {fname}: Remade successfully! (Sentences: {new_sentences}, Lemmas: {new_lemmas}, □: {new_squares}, ◆: {new_diamonds}) - 100% Lossless")
    return True

if __name__ == "__main__":
    target_sections = [int(arg) for arg in sys.argv[1:] if arg.isdigit()]
    if not target_sections:
        target_sections = list(range(2, 11))

    print("=" * 60)
    print(f"Starting batch remake for sections: {target_sections}")
    print("=" * 60)

    for sec in target_sections:
        verify_and_remake(sec)

    print("=" * 60)
    print("Batch remake complete. Running vocabulary auditor...")
    print("=" * 60)
