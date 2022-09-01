import os
import json
import random
random.seed(29)

fnames = os.listdir("../data_text")

jobj_list = []
for fname in fnames:
    with open(os.path.join("../data_text", fname)) as f:
        strip = f.read()
    fname =  fname[:-4]
    drummer_id, genre, bpm, _, time_sig, track_id = fname.split('_')
    jobj = {"fname": fname,"drummer_id": drummer_id, "genre": genre, "bpm": bpm, "time_sig":time_sig, "track_id":track_id, "strip": strip}
    jobj_list.append(jobj)

random.shuffle(jobj_list)
#num_examples = len(jobj_list)

with open("../data_split/train.json", 'w') as f:
    json.dump(jobj_list[:10000],f, indent=4)

with open("../data_split/dev.json", 'w') as f:
    json.dump(jobj_list[10000:11000],f, indent=4)

with open("../data_split/test.json", 'w') as f:
    json.dump(jobj_list[11000:],f, indent=4)