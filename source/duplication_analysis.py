import os
import matplotlib.pyplot as plt

def plot_histogram(total_occurences, fname):
    print(total_occurences)
    plt.hist(total_occurences)
    plt.xlabel('Occurences in training')
    plt.ylabel('Count')
    #plt.title('Histogram of IQ')
    #plt.xlim(0, 12)
    #plt.ylim(0, 300)
    plt.grid(True)
    #plt.show()
    plt.savefig(f"../diagrams/duplication/{fname}.png")

fpath = f"../data_text/test"
fnames = os.listdir(fpath)
unimeasure_occurence = {}
for fname in fnames:
    with open(os.path.join(fpath, fname)) as f:
        lines = f.readlines()
        measures = [''.join(lines[i:i+16]) for i in range(0,len(lines),16)]
        for measure in measures:
            if measure in unimeasure_occurence:
                unimeasure_occurence[measure] += 1
            else:
                unimeasure_occurence[measure] = 1

#print(unimeasure_occurence)
all_occurences = []
for model in ["human", "davinci", "ada"]:
    if model == "human":
        fpath = f"../data_text/test"
    else:
        fpath = f"../output_text_{model}/test"
    fnames = os.listdir(fpath)
    total_occurences = []
    for fname in fnames:
        #print(fname)
        #raise SystemExit()
        with open(os.path.join(fpath, fname)) as f:
            lines = f.readlines()
            measures = [''.join(lines[i:i+16]) for i in range(0,len(lines),16) if ''.join(lines[i:i+16]).replace('-', '').replace('\n', '')]
            #if not measures.replace('-', '').replace('\n', ''):
            #    continue
            for measure in measures:
                occurences = unimeasure_occurence.get(measure, 0)
                total_occurences.append(occurences)
    #print(total_occurences)
    #plot_histogram(total_occurences, model)
    all_occurences.append(total_occurences)

plt.figure(figsize=(6, 2))
plt.hist(all_occurences, label=["human", "davinci", "ada"])
plt.xlabel('Occurences in training')
plt.ylabel('Count')
plt.yticks([0, 100, 200, 300, 400])
#plt.title('Histogram of IQ')
#plt.xlim(0, 12)
#plt.ylim(0, 300)
#plt.grid(True)
#plt.show()
plt.legend(loc='best')
plt.savefig(f"../diagrams/duplication/duplication.png")