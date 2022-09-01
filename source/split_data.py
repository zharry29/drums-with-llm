import os
import json
import csv



fnames = os.listdir("../data_text")

jobj_list = []
appeared_strip = set()
for fname in fnames:
    with open(os.path.join("../data_text", fname)) as f:
        strip = f.read()
    if strip in appeared_strip:
        continue
    fname =  fname[:-4]
    drummer_id, genre, bpm, _, time_sig, track_id = fname.split('_')
    jobj = {"fname": fname,"drummer_id": drummer_id, "genre": genre, "bpm": bpm, "time_sig":time_sig, "track_id":track_id, "strip": strip}
    jobj_list.append(jobj)
    appeared_strip.add(strip)

random.shuffle(jobj_list)
num_examples = len(jobj_list)

with open("../data_split/train.json", 'w') as f:
    json.dump(jobj_list[:int(num_examples*.8)],f, indent=4)

with open("../data_split/dev.json", 'w') as f:
    json.dump(jobj_list[int(num_examples*.8):int(num_examples*.9)],f, indent=4)

with open("../data_split/test.json", 'w') as f:
    json.dump(jobj_list[int(num_examples*.8):],f, indent=4)