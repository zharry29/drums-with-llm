from mido import MidiFile
from mido import tempo2bpm
import os

def quantize(ticks_per_beat, ticks):
    range0 = [int(ticks_per_beat / 4) - int(ticks_per_beat / 8), int(ticks_per_beat / 4) + int(ticks_per_beat / 8)]
    ranges = [range(0, int(ticks_per_beat / 8))] + [range(range0[0] + k*int(ticks_per_beat / 4), range0[1] + k*int(ticks_per_beat / 4)) for k in range((MAX_BEATS)*4-1)]
    #print(ranges)
    #raise SystemExit()
    for i, r in enumerate(ranges):
        if ticks in r:
            return i
    #raise ValueError('Tick out of bounds.')
    return -1

def merge_articulations(note_to_seq):
    # snare
    for i, _ in enumerate(note_to_seq[38]):
        if note_to_seq[40][i] == 'o':
            #note_to_seq[38][i] = 'r'
            note_to_seq[38][i] = 'o'
        elif note_to_seq[37][i] == 'o':
            #note_to_seq[38][i] = 's'
            note_to_seq[38][i] = 'o'
    # ride
    for i, _ in enumerate(note_to_seq[51]):
        if note_to_seq[53][i] == 'o':
            #note_to_seq[51][i] = 'b'
            note_to_seq[51][i] = 'o'
        if note_to_seq[59][i] == 'o':
            note_to_seq[51][i] = 'o'
    # crash
    for i, _ in enumerate(note_to_seq[49]):
        if note_to_seq[57][i] == 'o':
            note_to_seq[49][i] = 'o'
    # hihat
    for i, _ in enumerate(note_to_seq[42]):
        #if note_to_seq[42][i] == 'o':
        #    note_to_seq[42][i] = 'x'
        #note_to_seq[42][i] = 'o'
        if note_to_seq[46][i] == 'o':
            note_to_seq[42][i] = 'o'
    # toms
    for i, _ in enumerate(note_to_seq[50]):
        if note_to_seq[48][i] == 'o':
            note_to_seq[50][i] = 'o'
        if note_to_seq[47][i] == 'o':
            note_to_seq[50][i] = 'o'
        if note_to_seq[45][i] == 'o':
            note_to_seq[50][i] = 'o'
        if note_to_seq[43][i] == 'o':
            note_to_seq[50][i] = 'o'

note_to_drum = {
    49: "CC",
    57: "CC2",
    51: "RC",
    59: "RC2",
    55: "SC",
    42: "HH",
    38: "SD",
    36: "KD",
    44: "FH",
    50: "T1",
    48: "T2",
    47: "T3",
    45: "T4",
    43: "FT",
    40: "RS",
    37: "SS",
    52: "CH",
    53: "RB", 
    46: "OH",
    54: "TB",
    56: "CB",
    22: "??",
    26: "??",
    39: "??",
    58: "??",
}

primary_notes = [49, 51, 42, 38, 36, 50]
#secondary_notes = [40, 37, 53, 46, 22, 26, 39, 58, 59, 57]

#midi_dir = '../e-gmd-v1.0.0/midi'
midi_dir = '../data_midi'
midi_fnames = os.listdir(midi_dir)
#text_dir = '../e-gmd-v1.0.0/text_v1'
text_dir = '../data_text'

file_count = 0
for midi_fname in midi_fnames:
    if file_count % 1000 == 0:
        print(file_count)
    file_count += 1
    #print(os.path.join(midi_dir, midi_fname))
    mid = MidiFile(os.path.join(midi_dir, midi_fname), clip=True)
    #print(mid)
    #raise SystemExit()
    tempo = 0
    time_signature = [0,0]
    for m in list(mid.tracks[0]):
        try:
            #tempo = tempo2bpm(m.tempo)
            time_signature = [m.numerator, m.denominator]
        except AttributeError:
            #print(m)
            continue
    
    #raise SystemExit()
    if time_signature[1] != 4:
        print("Skipped non x/4")
        continue

    #print(mid.ticks_per_beat)
    max_ticks = 0
    cumulative_time = 0

    for m in list(mid.tracks[1]):
        max_ticks += m.time

    #MAX_BEATS = int(max_ticks / mid.ticks_per_beat)
    MAX_BEATS = 4 * time_signature[0] # 4 measures * beats per measure
    MAX_16THS = (MAX_BEATS)*4 # max beats * 4 16ths per beat
    #print(MAX_16THS)

    note_to_seq = {k:['-']*(MAX_16THS) for k in note_to_drum.keys()}

    for m in list(mid.tracks[1]):
        cumulative_time += m.time
        if m.type == "note_on" and m.velocity > 0:
            #print(note_to_drum[m.note], end=' ')
            #print(m.velocity, end=' ')
            #print(m.time)
            #print(cumulative_time, end=' ')
            num_16th = quantize(mid.ticks_per_beat, cumulative_time)
            #print(num_16th)
            if num_16th == -1:
                break
            else:
                note_to_seq[m.note][num_16th] = 'o'
    else:
        continue

    #print(note_to_seq)

    merge_articulations(note_to_seq)

    with open(os.path.join(text_dir, midi_fname[:-5]+'.txt'), 'w') as fw:
        notes = list(note_to_seq.keys())
        notes = [x for x in notes if x in primary_notes]
        #for note in notes:
        #    fw.write(note_to_drum[note] + ' ')
        #fw.write('\n')
        #counter = 0
        for i in range(len(note_to_seq[notes[0]])):
            #if counter % time_signature[0] == 0:
            #    fw.write('=================\n')
            #counter += 1
            for note in notes:
                fw.write(note_to_seq[note][i] + '')
            fw.write('\n')
        
        
        """
        for k,seq in note_to_seq.items():
            #if k not in secondary_notes:
            if k in primary_notes:
                fw.write(note_to_drum[k])
                fw.write(' ')
                counter = 0
                for s in seq:
                    if counter % time_signature[0] == 0:
                        fw.write('|')
                    fw.write(s)
                    counter += 1
                fw.write('\n')
        """