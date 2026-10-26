import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\noid\.gemini\antigravity\brain\6d38666a-f963-44ca-ad84-c6459bfa6e8e\.system_generated\logs\transcript.jsonl', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(4340, 4355):
    data = json.loads(lines[i])
    print(f"Step {i} ({data.get('source')} - {data.get('type')}):")
    if data.get('tool_calls'):
        for tc in data['tool_calls']:
            print(f"  Tool: {tc['name']} -> {tc.get('args', {})}")
    if data.get('content'):
        print(f"  Content: {data['content'][:150]}...")
