# -*- coding: utf-8 -*-
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTIONS_DIR = os.path.join(BASE_DIR, 'sections')

# All lemmas currently in Sec 1-22
all_lemmas = set()
for i in range(1, 23):
    f = f'section_{i:02d}.md'
    txt = open(os.path.join(SECTIONS_DIR, f), encoding='utf-8').read()
    lemmas = re.findall(r'-\s+\*\*\d+\s*\|\s*([^*]+?)\*\*', txt)
    for l in lemmas:
        all_lemmas.add(l.strip().replace('...', '').lower())

proposals = [
    ('section_03.md', '0083', 'prêter', 'prêter de l\'argent'),
    ('section_03.md', '0116', 'maladroit(e)', 'une politique maladroite'),
    ('section_03.md', '0128', 'urbain(e)', 'la délinquance urbaine'),
    ('section_04.md', '0145', 'isolé(e)', 'un village isolé'),
    ('section_04.md', '0153', 'la substance', 'une substance radioactive'),
    ('section_04.md', '0182', 'engager', 'engager des poursuites'),
    ('section_05.md', '0236', 'la phase', 'la phase initiale'),
    ('section_06.md', '0283', 'par hasard', 'croiser par hasard'),
    ('section_07.md', '0328', 'convaincre', 'convaincre qn de (+ inf.)'),
    ('section_07.md', '0330', 'soutenir', 'soutenir un projet'),
    ('section_09.md', '0395', 'délicat(e)', 'un tissu délicat'),
    ('section_09.md', '0414', 'un appareil', 'un appareil ménager'),
    ('section_10.md', '0451', 'surveiller', 'surveiller les enfants'),
    ('section_10.md', '0472', 'flâner', 'flâner sur le rivage'),
    ('section_12.md', '0550', 'la phase', 'une phase cruciale'),
    ('section_13.md', '0567', 'ignorer', 'ignorer qn'),
    ('section_13.md', '0583', 'immense', 'une immense propriété'),
    ('section_14.md', '0614', 'respecter', 'respecter un délai'),
    ('section_15.md', '0646', 's\'intéresser à', 's\'intéresser'), # let's check!
    ('section_15.md', '0649', 'pratique', 'des compétences pratiques'),
    ('section_15.md', '0660', 'le tissu', 'le tissu musculaire'),
    ('section_16.md', '0703', 'finir par (+ inf.)', 'réussir'),
    ('section_18.md', '0759', 'avouer', 'devoir avouer'),
    ('section_18.md', '0766', 'pas du tout', 'non, pas du tout'),
    ('section_20.md', '0868', 'soutenir', 'soutenir que'),
    ('section_20.md', '0878', 'une expérience', 'une expérience scientifique'),
    ('section_20.md', '0891', 'préserver', 'préserver la planète'),
    ('section_20.md', '0893', 'en danger', 'une planète en danger'),
    ('section_20.md', '0910', 'vulnérable', 'une espèce vulnérable'),
    ('section_21.md', '0961', 'indispensable', 'être indispensable pour'),
    ('section_21.md', '0998', 'épais(se)', 'un brouillard épais'),
    ('section_22.md', '1013', 'un appareil', 'les appareils électroménagers'),
    ('section_22.md', '1066', 'un outil', 'un outil commode')
]

for sec, num, curr, prop in proposals:
    clean_p = prop.lower().strip()
    status = 'COLLISION!' if clean_p in all_lemmas else 'OK (unique)'
    print(f'{sec} #{num}: "{curr}" -> "{prop}" : {status}')
