import json
import logging
import os
from utils import list_to_dict
from urllib import parse
from abc import abstractmethod
from urllib.parse import parse_qs, urlparse

import spotipy
from yandex_music.client import Client as YaClient
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logging.getLogger("yandex_music").setLevel(100)


class ServiceBuilder:
    def __init__(self, url):
        self.url = url
        self.__parsed_url = urlparse(url)
        self.service = None

    def build_links(self):
        name = ""
        links = []
        if ServiceFactory.__is_spotify(self.__parsed_url):
            self.service = Spotify(self.url)
            name = self.service.get_full_track_name()
            links = [YaMusic.find_link(name), Youtube.find_link(name)]
        elif ServiceFactory.__is_yandex_music(self.__parsed_url):
            self.service = YaMusic(self.url)
            name = self.service.get_full_track_name()
            links = [Spotify.find_link(name), Youtube.find_link(name)]
        elif ServiceFactory.__is_youtube(self.__parsed_url):
            self.service = Youtube(self.url)
            name = self.service.get_full_track_name()
            links = [YaMusic.find_link(name), Spotify.find_link(name)]
        else:
            raise Exception(f"Unknown service: {self.url}")

        return links

    @staticmethod
    def __is_spotify(parsed_url):
        return "open.spotify.com" in parsed_url.netloc

    @staticmethod
    def __is_yandex_music(parsed_url):
        return "music.yandex.ru" in parsed_url.netloc

    @staticmethod
    def __is_youtube(parsed_url):
        return __is_short_youtube_url(parsed_url) or __is_full_youtube_url(parsed_url)

    @staticmethod
    def __is_full_youtube_url(parsed_url):
        return "youtube.com" in parsed_url.netloc

    @staticmethod
    def __is_short_youtube_url(parsed_url):
        return "youtu.be" in parsed_url.netloc


class Service:
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(self.url)

    @abstractmethod
    def get_full_track_name(self):
        return NotImplemented

    @staticmethod
    @abstractmethod
    def find_link(full_name):
        return NotImplemented

    @abstractmethod
    def get_id(self):
        return NotImplemented


class YaMusic(Service):
    client = YaClient(os.getenv("YA_MUSIC_TOKEN"))

    def __init__(self, url):
        super().__init__(url)

    def find_link(full_name):
        search = YaMusic.client.search(full_name, playlist_in_best=False)
        best_track_id = search.best.result.track_id.split(":")
        link = (
            f"https://music.yandex.ru/album/{best_track_id[1]}/track/{best_track_id[0]}"
        )
        # print(json.dumps(search.to_dict(), indent=4))
        # print(link)
        return link

    def get_full_track_name(self):
        album_track_dict = self.get_id()
        album = YaMusic.client.albums_with_tracks(album_track_dict["album"])
        print(f"album is {album.title}")
        track = YaMusic.client.tracks(f'{album_track_dict["track"]}')
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


class Youtube(Service):
    youtube = build(
        os.getenv("YOUTUBE_API_SERVICE_NAME"),
        os.getenv("YOUTUBE_API_VERSION"),
        developerKey=os.getenv("YOUTUBE_API_KEY"),
    )

    def __init__(self, url):
        super().__init__(url)

    def get_full_track_name(self):
        video_id = self.get_id()

        results = (
            Youtube.youtube.videos()
            .list(part="snippet", id=video_id)
            .execute()
            .get("items", [])
        )

        # get the first result (should be the only one anyway)
        found_video = list(filter(lambda x: x["id"] == video_id, results))
        if len(found_video):
            video = found_video[0]
            artist, name = video["snippet"]["title"].split("-")
            return f"{artist.strip()} - {name.strip()}"

        return None

    def find_link(full_name):
        search_result = (
            Youtube.youtube.search()
            .list(q=full_name, maxResults=1, part="snippet")
            .execute()
            .get("items", [])
        )

        video_results = list(
            filter(lambda x: x["id"]["kind"] == "youtube#video", search_result)
        )

        if len(video_results):
            return (
                f"https://www.youtube.com/watch?v={video_results[0]['id']['videoId']}"
            )

        return None

    def get_id(self):
        if ServiceFactory.__is_full_url():
            params = parse_qs(self.parsed_url.query)
            return params["v"][0]
        elif ServiceFactory.__is_short_url():
            return self.parsed_url.path.replace("/", "")


class Spotify(Service):
    cid = os.getenv("SPOTIPY_CLIENT_ID")
    secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    client_credentials_manager = SpotifyClientCredentials(
        client_id=cid, client_secret=secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def __init__(self, url):
        super().__init__(url)

    def get_full_track_name(self):
        track = Spotify.sp.track(self.get_id())
        full_name = f"{track['artists'][0]['name']} - {track['name']}"
        print(full_name)
        print(json.dumps(track, sort_keys=True, indent=4))
        return full_name

    def find_link(full_name):
        search = Spotify.sp.search(full_name, 1)
        link = search["tracks"]["items"][0]["external_urls"]["spotify"]
        # print(json.dumps(search, sort_keys=True, indent=4))
        print(link)
        return link

    def get_id(self):
        track_id = self.parsed_url.path.replace("/track/", "")
        return track_id


class AppleMusic(Service):
    def find_link(self):
        return NotImplemented
