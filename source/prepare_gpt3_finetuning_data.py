import json
import os

with open('../gpt3_train.jsonl','w') as fw:
    for fname in os.listdir('../data_text/train'):
        with open('../data_text/train/' + fname) as f:
            fw.write(json.dumps({'prompt': '', 'completion': f.read()}) + '\n')