import json

with open('../data_split/train.json') as f, open('../gpt3_train.jsonl','w') as fw:
    jobj = json.load(f)
    for j in jobj:
        fw.write(json.dumps({'prompt': '', 'completion': j['strip']}) + '\n')