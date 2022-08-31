import json
import os

score_path = "../e-gmd-v1.0.0/text_v1"
fnames = os.listdir(score_path)

with open('../gpt3_train.jsonl', 'w') as fw:
    for fname in fnames:
        json_line = {"prompt":"", "completion":"", "name":""}
        with open(os.path.join(score_path, fname)) as fr:
            score = fr.read()
            json_line["completion"] = score# + "END"
            json_line["name"] = fname[:-4]
        fw.write(json.dumps(json_line))
        fw.write('\n')
    