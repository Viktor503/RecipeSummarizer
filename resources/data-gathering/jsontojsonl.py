import json
f = open('resources/data-gathering/data.json', 'r',encoding='utf-8')
f2 = open('resources/data-gathering/data2.jsonl', 'w',encoding='utf-8')
data = json.load(f)
all = []
for i in data:
    new = {
        "message": [
            {
                "role": "user",
                "content": i['text_input']
            },
            {
                "role": "model",
                "content": i['output']
            }
        ]
        }
    all.append(new)
json.dump(all, f2, indent=4)