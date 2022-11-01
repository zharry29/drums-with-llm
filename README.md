# AI Drum Generation: Language Models Learn to Drum

This repository contains resources pertaining to the ongoing project of drum generation with NLP techniques, led by Li Zhang at the University of Pennsylvania. Currently, the assets here reflect our efforts until 10/31/2022.

## Background
Music generation with AI has made steady progress over the last few years. As a [drummer](https://space.bilibili.com/483770554) (drumset player) and AI researcher myself, I can't help but find out the progress with drum generation, and get disappointed at how little attention is directed towards it. In popular music, drums play a paradoxial role. More than 90% of the pop songs you hear on the charts have drums in them - drums are that important - while more than 90% of these drum beats are simply stock loops - drums are that unimportant. In the less mainstream genres I listen to and play, such as rock, metal, jazz, funk, and fusion, the composition and the performance of drums are no less involved and fascinating than any other instrument like the piano. 

Now that you understand the predicament about drums in modern music: there simply aren't too many interesting and well-formatted drum compositions out there, at least not enough to train a machine learning model that performs as well as for other instruments, such as piano. While the drummer in me laments, the NLP researcher in me kindles a flame of hope: indeed, the drumming world has little data, but so do other fields and domains in NLP, which have been coping decently with pre-trained large language models and their miraculous ability of transfer learning! What if such language training can transfer to drums? What if drum notations are not so different from English, from the persepective of machine learning models? I'm sure that Benny Greb, one of the greatest drummer of all time and author of one of the most famous drumming text book called "[The Language of Drumming](https://hudsonmusic.com/product/the-language-of-drumming-book-video/)," would appreciate this idea. 

The details of our work so far can be found in our paper to be published. Here, I'll show you how I trained one of the state-of-the-art language models, GPT3, to be a decent drummer. 

## Generate Drums
The best data source for nontrivial drumming I can find is the [Groove MIDI Dataset](https://magenta.tensorflow.org/datasets/groove) containing MIDI files of drum grooves, recorded by professional drummers playing solo on an electronic drum kit. For non-drummers, a _groove_ is basically what makes you dance when you hear some music (quoting Sarah Thawer, one of the greatest drummers). The drum grooves in this dataset is especially suitable because they are humanly (none of the drum machine looper shenanigans), diverse (spanning many genres, with the sad exception of metal), and sound good. 

```
wget https://storage.googleapis.com/magentadata/datasets/groove/groove-v1.0.0-midionly.zip
mkdir groove
unzip groove-v1.0.0-midionly.zip -d groove
```

To process the data as described in the paper:
```
cd source
python midi_to_text.py
python split_data.py
python text_to_data.py
```
Now, `/data_midi` contains all the original MIDI files by the split. `/data_text` and `/data_text_midi` contain the textual drumroll representation of each MIDI file *after the simplification process* described in the paper. We can now use `gpt3_train.jsonl` to finetune a GPT3 to generate drum grooves given 2 measures. 
```
export OPENAI_API_KEY="YOUR_API_KEY"
openai api fine_tunes.create -t ../gpt3_train.jsonl -m davinci|curie|babbage|ada
```
Once finetuning has finished, you should edit `evaluate.py` to provide your `openai.api_key_path` in line 6 and the ID of your trained model in line 7. Then run
```
python evaluate.py
```
Now, `/output_text_MODEL` and `/output_midi_MODEL` contain the textual drumroll representation of each MIDI file generated by the finetuned model in the dev and test set. You can examine and listen to the generation by loading the output MIDI files into a DAW or a notation software.

To perform analyses in the paper, run
```
python anaylsis.py
```

## Citation
If you find our work useful, please cite
```
@inproceedings{zhang2023drums,
  title={Large Language Models Learn to Drum},
  author={Zhang, Li and Callison-Burch, Chris},
  booktitle={The AAAI-23 Workshop on Creative AI Across Modalities},
  year={2023}
}
```