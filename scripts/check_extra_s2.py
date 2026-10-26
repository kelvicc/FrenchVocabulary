# -*- coding: utf-8 -*-
from run_full_audit import parse_french_section

# Section 02 French items:
s2 = parse_french_section(2)
print("=== Section 02 French Items ===")
for it in s2:
    print(f"FR No.{it['num']}: {it['ja']}")
    print(f"   French: {it['fr']}")

# Notice:
# No. 013: 寓話からの引用 (Official No. 14)
# No. 014: 現代文学 (Official No. 15)
# No. 015: 2つの動詞混同 (Official No. 16)
# No. 016: 発音合ってる (Official No. 17)
# No. 017: 語彙増やすアドバイス (Official No. 18)
# No. 018: 市役所で展示 (Official No. 19)
# No. 019: 少し詰めて (Official No. 20)
# No. 020: 要するに、この実用的な著作は心を奪われるほど面白く、実に読む価値がある。 -> EXTRA (独自文)
# No. 021: 知的好奇心に突き動かされ、彼は毎日自らの知識を深めようと努めている。 -> EXTRA (独自文)
# No. 022: 打ち解けるために、彼は同僚の女性の自然なエレガンスを褒めた。 -> EXTRA (独自文)
# No. 023: 一目見た最初の出会いから、彼の温かい眼差しは私に完全な信頼感を抱かせた。 -> EXTRA (独自文)
# No. 024: 彼のこと、お人好しだと思う？どちらかと言えば経験不足ね。 -> EXTRA (独自文)
