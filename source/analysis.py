import matplotlib.pyplot as plt
import os

def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def repetition_variation(lines):
    # A good groove is based on repetition and variation of a core idea as a measure
    measures = ['\n'.join(lines[i:i+16]) for i in range(0,len(lines),16)]
    # First, we need to define a "distance" between two measures
    def distance(m1, m2):
        # Both m1 and m2 are 16 lines (16 16-th notes)
        m1 = m1.replace('\n', '')
        m2 = m2.replace('\n', '')
        return levenshtein_distance(m1,m2)
    # Then, we find the most frequently occuring measure
    most_common_measure = max(set(measures), key=measures.count)
    # Then, we calculate edit distance of every M to this M
    distances = [distance(m, most_common_measure) for m in measures]
    print(distances)
    return distances

def plot_distances(gold_distances, pred_distances, fname):
    plt.plot(range(len(gold_distances)), gold_distances, '-o', label='gold')
    plt.plot(range(len(pred_distances)), pred_distances, '-o', label='pred')
    plt.title(fname)
    plt.xlabel("Measure")
    plt.ylabel("Distance from most common")
    plt.legend(loc='best')
    plt.ylim([0, 50])
    #plt.show()
    plt.savefig(f"../output_figs/{fname}.png")
    plt.clf()

fnames = os.listdir("../data_text/dev")
for fname in fnames:
    fname = fname.split('.')[0]
    with open(f"../data_text/dev/{fname}.txt") as fg, open(f"../output_text/dev/{fname}.txt") as fp:
        gold_lines = fg.readlines()
        pred_lines = fp.readlines()

    gold_distances = repetition_variation(gold_lines)
    pred_distances = repetition_variation(pred_lines)
    plot_distances(gold_distances, pred_distances, fname)
    #break