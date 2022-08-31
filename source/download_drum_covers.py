from youtubesearchpython import VideosSearch
import pickle
import json
import os
from pytube import YouTube
from tqdm import tqdm

def get_urls(query):
    urls = set()
    search = VideosSearch(query)
    while(len(urls) < 10000):
        print(len(urls))
        video_ids = []
        new_urls = []
        for result in search.result()['result']:
            video_ids.append(result['id'])
            new_urls.append(result['link'])
        urls.update(new_urls)
        search.next()

    pickle.dump(list(urls), open('urls.p','wb'))
    #return urls


def downloadYouTube(videourl, path, fn):
    yt = YouTube(videourl)
    yt = yt.streams.filter(only_audio=True).first()
    yt.download(path, filename=fn)

    output_path = '../drum_covers/'
    for url in tqdm(urls):
        downloadYouTube(url, output_path, fn = url[-11:] + '.mp3')

query = 'drum cover'
get_urls(query)

