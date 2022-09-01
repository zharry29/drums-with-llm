import os

fnames = os.listdir("./data_midi")

for fname in fnames:
    genre = fname.split('_')[1]