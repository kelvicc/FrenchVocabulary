# -*- coding: utf-8 -*-
import json

with open('C:/Users/noid/.gemini/antigravity/brain/6d38666a-f963-44ca-ad84-c6459bfa6e8e/.system_generated/logs/transcript.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        if data.get('source') == 'USER_EXPLICIT':
            content = data.get('content', '')
            if 'transcript' in content.lower() or 'original' in content.lower() or '本家' in content:
                print(f"Step {data.get('step_index')}: {content[:200]}")
