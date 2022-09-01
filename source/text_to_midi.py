from mido import MidiFile, MidiTrack, Message, MetaMessage
import os
import json

primary_notes = [49, 51, 38, 36, 42, 50]

def convert_to_midi(text, out_file):
    mid = MidiFile(type=1, ticks_per_beat=480)
    track0 = MidiTrack()
    track1 = MidiTrack()
    mid.tracks.append(track0)
    mid.tracks.append(track1)
    
    # metadata
    track0.append(MetaMessage('set_tempo', tempo=500000, time=0))
    track0.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    track0.append(MetaMessage('key_signature', key='C', time=0))
    track0.append(MetaMessage('end_of_track', time=1))
    
    track1.append(Message('program_change', channel=9, program=0, time=0))
    
    lines = [l for l in text.split('\n') if l]
    initial_note_played = False
    for j, line in enumerate(lines):
        #print(line)
        first_note_played = False
        for i, char in enumerate(line):
            if char == 'o':
                note_played = primary_notes[i]
                # add a midi event
                if not initial_note_played:
                    time = 0
                    initial_note_played = True
                    first_note_played = True
                elif not first_note_played:
                    time = 120
                    first_note_played = True
                else:
                    time = 0
                
                track1.append(Message('note_on', note=note_played, velocity=100, time=time))
        if not first_note_played:
            #print('not')
            track1.append(Message('note_on', note=51, velocity=0, time=120))
    
    track1.append(MetaMessage('end_of_track', time=1))
    #print(mid)
    mid.save(out_file)

def data_to_midi():
    with open('../gpt3_train.jsonl') as f:
        for line in f:
            j = json.loads(line)
            text = j["completion"]
            fname = '../data_midi/' + j["name"] + '.midi'
            convert_to_midi(text, fname)

if __name__ == '__main__':
    #text = "----o-\n------\n--o---\n------\n---oo-\n------\n--o---\n------\n--o-o-\n------\n--o---\n------\n---oo-\n------\n--o---\n------\n--o-o-\n------\n--o---\n------\n--ooo-\n------\n--o---\n------\nooo-o-\n------\n--o---\n------\n---oo-\n------\n------\n------\n--o-o-\n------\n--o---\n------\n---oo-\n------\n--o---\n------\n----o-\n------\n--o---\n------\n---oo-\n------\n--o---\n------\n----o-\n------\n--o---\n------\n--ooo-\n------\n--o---\n------\n----o-\n------\n--o---\n------\n---oo-\n------\n---o--\n---o--\nEND"
    #convert_to_midi(text, "test.mid")
    #data_to_midi()
    fnames = os.listdir('../data_text')
    for fname in fnames:
        with open('../data_text/'+fname) as f:
            text = f.read()
        convert_to_midi(text, '../data_text_midi/'+fname[:-4]+'.mid')