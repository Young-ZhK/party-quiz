
import json

with open('data/第四套-第六套.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('第四套-第六套.json中的内容:')
print(list(data.keys()))
print(f'第四套: {len(data.get("set4", []))}题')
print(f'第五套: {len(data.get("set5", []))}题')
print(f'第六套: {len(data.get("set6", []))}题')
