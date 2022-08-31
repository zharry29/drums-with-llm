import moviepy.editor as mp
import os

for fname in os.listdir('../youtube/videos'):
    clip = mp.VideoFileClip('../youtube/videos/' + fname)
    clip.audio.write_audiofile('../youtube/audios/' + fname.split('.')[0] + '.mp3')