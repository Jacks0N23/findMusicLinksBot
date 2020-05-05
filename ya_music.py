# https://pypi.org/project/yandex-music/
# https://github.com/MarshalX/yandex-music-api
import json
import logging
import os

from yandex_music.client import Client
from utils import list_to_dict
from urllib import parse

client = Client(os.getenv("YA_MUSIC_TOKEN"))
logging.getLogger("yandex_music").setLevel(100)


def parse_full_name(album_track_dict):
    album = client.albums_with_tracks(album_track_dict["album"])
    print(f"album is {album.title}")
    track = client.tracks(f'{album_track_dict["track"]}')
    # print(track)
    full_name = f"{track[0].artists[0].name} - {track[0].title}"
    print(full_name)
    return full_name


def parse_track_id(music_url):
    parsed_url = parse.urlparse(music_url)
    print(parsed_url)
    album_track_dict = list_to_dict(list(filter(None, parsed_url.path.rsplit("/"))))
    print(album_track_dict)
    return album_track_dict


def is_ya_music(url: str) -> bool:
    return parse.urlparse(url).netloc.__contains__("music.yandex.ru")


def get_full_track_name(sp_url):
    track_id = parse_track_id(sp_url)
    return parse_full_name(track_id)


def download_mp3(track):
    print(f"track is {track[0].title}")
    track[0].download(f"{track[0].title}.mp3")


def find_link(full_name):
    search = client.search(full_name, playlist_in_best=False)
    best_track_id = search.best.result.track_id.split(":")
    link = f"https://music.yandex.ru/album/{best_track_id[1]}/track/{best_track_id[0]}"
    print(json.dumps(search.to_dict(), indent=4))
    print(link)
    return link


# parse_track_id("https://music.yandex.ru/album/9004319/track/58980117")
# find_link("Marselle - На букву М")
