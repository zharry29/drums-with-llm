import matplotlib.pyplot as plt
import os
import random
random.seed(29)
from statistics import mean
from sklearn.cluster import KMeans
import numpy as np

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
    measures = measures[:16]
    # First, we need to define a "distance" between two measures
    # Then, we use a sliding window to find the minimum distance to a neighbor
    stabilities = [min([levenshtein_distance(measures[i],measures[i-1]),levenshtein_distance(measures[i],measures[i+1])]) for i in range(1, len(measures)-1)]
    return stabilities

def plot_stabilities(gold_stabilities, davinci_stabilities, curie_stabilities, random_stabilities, repeat_stabilities, fname):
    plt.plot(range(2,len(gold_stabilities)+2), gold_stabilities, '-o', label='human')
    plt.plot(range(2,len(random_stabilities)+2), random_stabilities, '-1', label='random')
    plt.plot(range(2,len(repeat_stabilities)+2), repeat_stabilities, '-2', label='repeat')
    plt.plot(range(2,len(davinci_stabilities)+2), davinci_stabilities, '-v', label='davinci')
    plt.plot(range(2,len(curie_stabilities)+2), curie_stabilities, '-^', label='curie')
    plt.title(fname)
    plt.xlabel("Measure")
    plt.ylabel("Stability")
    #plt.legend(loc='best')
    plt.ylim([0, 50])
    #plt.show()
    plt.savefig(f"../output_figs/{fname}.png")
    plt.clf()

def average_distance_to_cluster_center(stabilities):
    stabilities = np.array(stabilities)
    kmeans = KMeans(n_clusters=2, random_state=0).fit(stabilities.reshape(-1, 1))
    return np.mean(np.abs(stabilities - kmeans.cluster_centers_[kmeans.labels_][:,0]))


fnames = os.listdir("../data_text/dev")
gold_all_stabilities = []
random_all_stabilities = []
repeat_all_stabilities = []
davinci_all_stabilities = []
curie_all_stabilities = []
for fname in fnames:
    fname = fname.split('.')[0]
    with open(f"../data_text/dev/{fname}.txt") as fg, open(f"../output_text/dev/{fname}.txt") as fd, open(f"../output_text_curie/dev/{fname}.txt") as fc:
        gold_lines = fg.readlines()
        davinci_lines = fd.readlines()
        curie_lines = fc.readlines()

    gold_stabilities = repetition_variation(gold_lines)
    davinci_stabilities = repetition_variation(davinci_lines)
    curie_stabilities = repetition_variation(curie_lines)
    random_stabilities = repetition_variation([''.join([random.choice(['-','o']) for j in range(6)]) + '\n' for i in range(256)])
    repeat_stabilities = repetition_variation(gold_lines[:16] + gold_lines[16:32]*15)
    
    gold_all_stabilities.append(average_distance_to_cluster_center(gold_stabilities))
    random_all_stabilities.append(average_distance_to_cluster_center(random_stabilities))
    #repeat_all_stabilities += average_distance_to_cluster_center(repeat_stabilities)
    davinci_all_stabilities.append(average_distance_to_cluster_center(davinci_stabilities))
    curie_all_stabilities.append(average_distance_to_cluster_center(curie_stabilities))

    #gold_all_stabilities += gold_stabilities
    #random_all_stabilities += random_stabilities
    #repeat_all_stabilities +=repeat_stabilities
    #davinci_all_stabilities += davinci_stabilities
    #curie_all_stabilities += curie_stabilities

    #plot_stabilities(gold_stabilities, davinci_stabilities, curie_stabilities, random_stabilities, repeat_stabilities, fname)
    #break



print(mean(gold_all_stabilities))
print(mean(random_all_stabilities))
#print(mean(repeat_all_stabilities))
print(mean(davinci_all_stabilities))
print(mean(curie_all_stabilities))