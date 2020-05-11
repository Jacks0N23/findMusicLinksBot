# https://pypi.org/project/yandex-music/
# https://github.com/MarshalX/yandex-music-api
import json
import logging
import os
from yandex_music.client import Client as YaClient
from music_services.BaseService import BaseService
from utils import list_to_dict
from urllib import parse


class YaMusic(BaseService):
    logging.getLogger("yandex_music").setLevel(100)

    def __init__(self):
        super().__init__(YaClient(os.getenv("YA_MUSIC_TOKEN")))

    # TODO redo like in youtube
    def is_acceptable(self, url):
        parsed_url = parse.urlparse(url)
        is_ya_music_service = parsed_url.netloc.__contains__("music.yandex")
        if is_ya_music_service:
            self.url = url
            self.parsed_url = parsed_url
            return self
        return None

    def find_link(self, full_name):
        search = self.client.search(full_name, playlist_in_best=False)
        link = None
        try:
            best_track_id = search.best.result.track_id.split(":")
            link = f"https://music.yandex.ru/album/{best_track_id[1]}/track/{best_track_id[0]}"
            print(link)
        except Exception as e:
            print("YaMusic: link not found", e)
            # print(json.dumps(search.to_dict(), indent=4))  # the exception is too long so by default is commented
        return link

    def get_full_track_name(self):
        album_track_dict = self.get_id()
        album = self.client.albums_with_tracks(album_track_dict["album"])
        print(f"album is {album.title}")
        track = self.client.tracks(f'{album_track_dict["track"]}')
        # print(track)
        full_name = f"{track[0].artists[0].name} - {track[0].title}"
        print(full_name)
        return full_name

    def get_id(self):
        album_track_dict = list_to_dict(
            list(filter(None, self.parsed_url.path.rsplit("/")))
        )
        print(album_track_dict)
        return album_track_dict

# get_id("https://music.yandex.ru/album/9004319/track/58980117")
# find_link("Marselle - На букву М")

