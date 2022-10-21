import json
import os

for split in ["train", "dev", "test"]:
    score_path = f"../data_text/{split}"
    fnames = os.listdir(score_path)

    with open(f'../gpt3_{split}.jsonl', 'w') as fw:
        for fname in fnames:
            json_line = {"prompt":"", "completion":"", "name":""}
            with open(os.path.join(score_path, fname)) as fr:
                score = fr.readlines()
                json_line["prompt"] = ''.join(score[:32])
                json_line["completion"] = ''.join(score[32:]) + 'END'
                json_line["name"] = fname[:-4]
            fw.write(json.dumps(json_line))
            fw.write('\n')
        