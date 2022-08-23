import argparse
import logging
import os


import requests
from bs4 import BeautifulSoup

logger = None

def parse_args():
    parser = argparse.ArgumentParser(description = "web crawler")
    parser.add_argument("-d", "--debug", help = "Enable debug logging", action = "store_true")
    parser.add_argument("-c", "--crawl", help = "Enable crawl and write the file", action = "store_true")
    return parser.parse_args()

def configure_logging(level = logging.DEBUG):
    global logger
    logger = logging.getLogger("crawler")
    logger.setLevel(level)
    screen_handler = logging.StreamHandler()
    screen_handler.setLevel(level)
    formatter = logging.Formatter("[%(levelname)s] : %(filename)s(%(lineno)d) : %(message)s")
    screen_handler.setFormatter(formatter)
    logger.addHandler(screen_handler)

def get_artists(base):
    artists = {}
    resp = requests.get(base)
    soup = BeautifulSoup(resp.content, "lxml")
    track_list = soup.find("table", attrs = {"class" : "tracklist"})
    track_link = track_list.find_all('h3')
    for link in track_link[0:5]:
        artists[link.text] = link.a['href']
    return artists

def get_songs(artist):
    songs = {}
    resp = requests.get(artist)
    soup = BeautifulSoup(resp.content, "lxml")
    song_list = soup.find("table", attrs = {"class" : "tracklist"})
    songs_links = song_list.find_all('a')
    for song in songs_links[:3]:
        songs[song.text] = song['href']
    return songs

def get_lyrics(song):
    resp = requests.get(song)
    soup = BeautifulSoup(resp.content, "lxml")
    lyrics = soup.find("p", attrs = {"id" : "songLyricsDiv"})
    return lyrics.text


def crawl(download_dir):
    logger.info("crawling started..")
    for artist_name, artist_link in get_artists('https://www.songlyrics.com/top-artists-lyrics.html').items():
        logger.debug("Artist : %s", artist_name)
        artist_dir = os.path.join(download_dir, artist_name)
        os.makedirs(artist_dir, exist_ok = True)
        for song_name, song_link in get_songs(artist_link).items():
            song = song_name.replace("/"," ")
            file = open(f"{artist_dir}/{song}.txt", 'w')
            file.write(get_lyrics(song_link))
            file.close
    logger.info("crawling completed")
            
def main():

    args = parse_args()
    if args.debug:
        configure_logging()
    else:
        configure_logging(logging.INFO)
    if args.crawl:
        crawl("artists")

    
if __name__== "__main__":
    main()