import os
import json
import csv

with open("../groove/info.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        fname = row["midi_filename"]
        fname = fname.split('/')[0][7:] + '_' + fname.split('/')[-1][:-4]
        split = row["split"]
        if split == "validation":
            split = "dev"
        os.system(f"cp ../data_midi/{fname}.mid ../data_midi/{split}/{fname}.mid")
        os.system(f"cp ../data_text/{fname}.txt ../data_text/{split}/{fname}.txt")
        os.system(f"cp ../data_text_midi/{fname}.mid ../data_text_midi/{split}/{fname}.mid")