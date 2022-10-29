import os
from collections import Counter

for split in ["train", "dev", "test"]:
    styles = []
    for fname in os.listdir(f"../data_text/{split}"):
        style = fname.split('_')[2].split('-')[0]
        styles.append(style)
    print(Counter(styles))