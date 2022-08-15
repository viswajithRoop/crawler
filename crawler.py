import argparse
import logging

import requests
from bs4 import BeautifulSoup

logger = None

def parse_args():
    parser = argparse.ArgumentParser(description = "web crawler")
    parser.add_argument("-d", "--debug", help = "Enable debug logging", action = "store_true")
    return parser.parse_args()

def configure_logging(level = logging.INFO):
    global logger
    logger = logging.getLogger("crawler")
    logger.setLevel(level)
    screen_handler = logging.StreamHandler()
    screen_handler.setLevel(level)
    formatter = logging.Formatter("[%(levelname)s] : %(filename)s(%(lineno)d) : %(message)s")
    screen_handler.setFormatter(formatter)
    logger.addHandler(screen_handler)

def get_artists(base):
    resp = requests.get(base)
    soup = BeautifulSoup(resp.content, "lxml")
    track_list = soup.find("table", attrs = {"class" : "tracklist"})
    track_link = track_list.find_all('a')
    for link in track_link:
        if link.find('img') not in link:
            print(link.text)

def get_songs(artist):
    resp = requests.get(artist)
    soup = BeautifulSoup(resp.content, "lxml")
    song_list = soup.find("table", attrs = {"class" : "tracklist"})
    songs = song_list.find_all('a')
    for song in songs:
        print(song.text)

def get_lyrics(song):
    resp = requests.get(song)
    soup = BeautifulSoup(resp.content, "lxml")
    lyrics = soup.find("p", attrs = {"id" : "songLyricsDiv"})
    print(lyrics.text)

def main():
    get_artists('https://www.songlyrics.com/top-artists-lyrics.html')
    get_songs('https://www.songlyrics.com/eminem-lyrics/')
    get_lyrics('https://www.songlyrics.com/eminem/survival-lyrics/')

if __name__=="__main__":
    main()