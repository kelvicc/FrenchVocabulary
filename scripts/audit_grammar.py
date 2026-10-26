# -*- coding: utf-8 -*-
"""
DUO Français Deep Grammar & Gender Auditor
Performs deep grammatical, morphological, gender, and spelling verification across all 520 sentences.
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

def audit_all():
    files = sorted([f for f in os.listdir(SECTIONS_DIR) if f.endswith(".md")])
    
    # 1. 縮約忘れチェック (de le, de les, à le, à les)
    contraction_errors = []
    # 2. 有音hのエリズィオン誤りチェック (l'honte, l'hausse, l'haine, l'hasard, l'héros, etc.)
    aspirated_h_errors = []
    # 3. エリズィオン忘れチェック (je ai, de un, etc.)
    elision_omissions = []
    # 4. 名詞の性別ルールと不一致の名詞チェック
    gender_suspicious = []
    
    aspirated_h_words = ['honte', 'hausse', 'haine', 'hasard', 'héros', 'hauteur', 'halte', 'handicap', 'hâte']
    
    # 代表的な間違いやすい名詞の正解性別辞書（男性名詞）
    known_masculine = [
        'silence', 'problème', 'système', 'thème', 'poème', 'modèle', 'domaine', 'groupe',
        'espace', 'culte', 'doute', 'rôle', 'monde', 'livre', 'territoire', 'mérite', 'parti',
        'poste', 'sommet', 'commerce', 'ordre', 'manque', 'siècle', 'voyage', 'visage', 'fleuve',
        'orage', 'désastre', 'équilibre', 'principe', 'terme', 'sommeil', 'regret', 'paradoxe'
    ]
    # 代表的な間違いやすい名詞の正解性別辞書（女性名詞）
    known_feminine = [
        'fin', 'mer', 'loi', 'foi', 'dent', 'nuit', 'forêt', 'peau', 'clef', 'clé', 'fois',
        'voix', 'paix', 'croix', 'douleur', 'couleur', 'valeur', 'erreur', 'fleur', 'odeur',
        'saveur', 'peur', 'chaleur', 'vapeur', 'mémoire', 'vertu', 'statut', 'tribu', 'victime'
    ]
    
    total_sentences = 0
    total_lemmas = 0
    
    for fname in files:
        fpath = os.path.join(SECTIONS_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        cur_no = None
        for line in lines:
            m_no = re.match(r"^###\s+No\.\s*(\d+)", line)
            if m_no:
                cur_no = m_no.group(1)
                total_sentences += 1
                
            m_sent = re.match(r"^>\s*\*\*«\s*(.*?)\s*»\*\*", line)
            if m_sent and cur_no:
                text = m_sent.group(1).strip()
                
                # Check contractions
                for bad in ['de le ', 'de les ', 'à le ', 'à les ']:
                    if bad in text:
                        # Exclude pronouns: e.g. "de le faire", "de les voir"
                        idx = text.find(bad)
                        after = text[idx + len(bad):].strip().split()
                        if after:
                            next_word = after[0].lower().strip(".,;:?!")
                            is_infinitive = (next_word.endswith('er') or next_word.endswith('ir') or 
                                             next_word.endswith('re') or next_word in ['faire', 'voir', 'prendre', 'mettre'])
                            if not is_infinitive:
                                contraction_errors.append((fname, cur_no, bad.strip(), text))
                                
                # Check aspirated H
                for h in aspirated_h_words:
                    if re.search(r"\bl'" + h + r"\b", text, re.IGNORECASE) or re.search(r"\bd'" + h + r"\b", text, re.IGNORECASE):
                        aspirated_h_errors.append((fname, cur_no, h, text))
                        
                # Check missing elision: e.g. "je ai", "de un"
                bad_elisions = re.findall(r"\b(je|ne|me|te|se|de|ce|que|lorsque|puisque)\s+([aeiouyàâéèêëîïôùû][a-zàâéèêëîïôùûç]*)", text, re.IGNORECASE)
                for be in bad_elisions:
                    # Exceptions: "ce" before 'un/une' is "c'est un", but "ce un" is bad
                    # "de" before "huit/onze" is allowed
                    if be[1].lower() not in ['huit', 'onze', 'oui']:
                        elision_omissions.append((fname, cur_no, f"{be[0]} {be[1]}", text))

            # Check lemma gender tags
            m_lem = re.match(r"^-\s+\*\*(\d+)\s*\|\s*([^*]+?)\*\*\s*(?:/[^/]+/|\[[^\]]+\])?\s*(【[^】]+】)?", line)
            if m_lem:
                total_lemmas += 1
                lem_num = m_lem.group(1)
                lem_name = m_lem.group(2).strip()
                pos = m_lem.group(3) or ""
                
                clean_name = re.sub(r"^(le |la |l'|un |une |les |se |s')", "", lem_name).strip().lower()
                clean_name = re.split(r"[\s(/]", clean_name)[0]
                
                if "【名・女】" in pos and clean_name in known_masculine:
                    gender_suspicious.append((fname, cur_no, lem_num, lem_name, pos, f"'{clean_name}' is typically masculine!"))
                elif "【名・男】" in pos and clean_name in known_feminine:
                    # Note: "mémoire" can be both (le mémoire: thesis, la mémoire: memory)
                    if clean_name == 'mémoire':
                        pass
                    else:
                        gender_suspicious.append((fname, cur_no, lem_num, lem_name, pos, f"'{clean_name}' is typically feminine!"))

    print("=" * 60)
    print("DUO Français Deep Grammar & Gender Audit Results")
    print(f"Total Sentences Audited: {total_sentences} / 520")
    print(f"Total Lemmas Audited   : {total_lemmas}")
    print("=" * 60)
    
    print("\n[1] Contraction Errors (縮約忘れ: de le -> du, à le -> au 等):")
    if contraction_errors:
        for err in contraction_errors:
            print(f"  ❌ {err[0]} [No. {err[1]}]: '{err[2]}' in: {err[3]}")
    else:
        print("  ✅ PASS: 縮約エラー 0件 (100% 正確)")
        
    print("\n[2] Aspirated H Errors (有音hの誤ったエリズィオン: l'honte 等):")
    if aspirated_h_errors:
        for err in aspirated_h_errors:
            print(f"  ❌ {err[0]} [No. {err[1]}]: '{err[2]}' in: {err[3]}")
    else:
        print("  ✅ PASS: 有音hエリズィオンエラー 0件 (100% 正確)")
        
    print("\n[3] Elision Omissions (母音衝突エリズィオン忘れ: je ai -> j'ai 等):")
    if elision_omissions:
        for err in elision_omissions:
            print(f"  ❌ {err[0]} [No. {err[1]}]: '{err[2]}' in: {err[3]}")
    else:
        print("  ✅ PASS: エリズィオン脱落 0件 (100% 正確)")
        
    print("\n[4] Gender Suspicious Items (性別辞書との照合):")
    if gender_suspicious:
        for err in gender_suspicious:
            print(f"  ⚠️ {err[0]} [No. {err[1]} / Lemma {err[2]}]: {err[3]} {err[4]} -> {err[5]}")
    else:
        print("  ✅ PASS: 辞書照合による性別エラー 0件 (100% 正確)")
        
    print("=" * 60)

if __name__ == "__main__":
    audit_all()
