# https://github.com/plamere/spotipy

import os
from urllib import parse
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
from music_services.BaseService import BaseService


class Spotify(BaseService):

    def __init__(self):
        _cid = os.getenv("SPOTIPY_CLIENT_ID")
        _secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        _client_credentials_manager = SpotifyClientCredentials(client_id=_cid, client_secret=_secret)
        super().__init__(spotipy.Spotify(client_credentials_manager=_client_credentials_manager))

    def is_acceptable(self, url):
        parsed_url = parse.urlparse(url)
        is_spotify_service = parsed_url.netloc.__contains__("open.spotify")
        if is_spotify_service:
            self.url = url
            self.parsed_url = parsed_url
            return self
        return None

    def get_full_track_name(self):
        track = self.client.track(self.get_id())
        full_name = f"{track['artists'][0]['name']} - {track['name']}"
        print(full_name)
        # print(json.dumps(track, sort_keys=True, indent=4))
        return full_name

    def find_link(self, full_name):
        search = self.client.search(full_name, 1)
        link = None
        try:
            link = search["tracks"]["items"][0]["external_urls"]["spotify"]
            print(link)
        except Exception as e:
            print("link not found\n", e)
            print(json.dumps(search, sort_keys=True, indent=4))
        return link

    def get_id(self):
        track_id = self.parsed_url.path.replace("/track/", "")
        print(track_id)
        return track_id

# parse_track_id("https://open.spotify.com/track/5hAtL8xsBjKAaxkWJAit4L")
# find_link("Marselle - На букву М")
