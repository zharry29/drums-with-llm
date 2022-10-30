import json
import os

def is_enough_length(score):
    return len(score) > 128

def strip_empty_measure(score):
    stripped = False
    def is_first_measure_empty(score):
        first_qtr_note = score[:4]
        # If first quarter note is empty, then empty
        if ''.join(first_qtr_note).replace('\n','') == '------'*4:
            return True
        else:
            return False
    while is_first_measure_empty(score):
        score = score[16:]
        stripped = True
    return score, stripped

def add_separator(score):
    j = 0
    for i in range(16, len(score)+1, 16):
        score = score[:i+j] + ['SEP\n'] + score[i+j:]
        j += 1
    return score

for split in ["train", "dev", "test"]:
    score_path = f"../data_text/{split}"
    fnames = os.listdir(score_path)

    with open(f'../gpt3_{split}.jsonl', 'w') as fw:
        for fname in fnames:
            json_line = {"prompt":"", "completion":"", "name":""}
            with open(os.path.join(score_path, fname)) as fr:
                score = fr.readlines()
                score, stripped = strip_empty_measure(score)
                if stripped:
                    print(f"Stripped {fname}")
                if not is_enough_length(score):
                    print(f"Ignored short {fname}")
                    continue
                json_line["prompt"] = ''.join(add_separator(score[:32]))
                json_line["completion"] = ''.join(add_separator(score[32:])).strip('SEP\n') + '\nEND'
                json_line["name"] = fname[:-4]
            fw.write(json.dumps(json_line))
            fw.write('\n')
        