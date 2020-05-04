# https://github.com/plamere/spotipy

import os
from urllib import parse
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials

cid = os.getenv('SPOTIPY_CLIENT_ID')
secret = os.getenv('SPOTIPY_CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def parse_full_name(track_id):
    track = sp.track(track_id)
    full_name = f"{track['artists'][0]['name']} - {track['name']}"
    print(full_name)
    print(json.dumps(track, sort_keys=True, indent=4))
    return full_name


def parse_track_id(sp_url):
    assert isinstance(sp_url, str)
    parsed_url = parse.urlparse(sp_url)
    if is_spotify(sp_url):
        assert isinstance(parsed_url.path, str)
        track_id = parsed_url.path.replace("/track/", "")
        print(track_id)
        return track_id

    else:
        print("it's not spotify")
        return None


def get_full_track_name(sp_url):
    track_id = parse_track_id(sp_url)
    return parse_full_name(track_id)


def is_spotify(sp_url):
    return parse.urlparse(sp_url).netloc.__contains__("spotify")


def find_link(full_name):
    search = sp.search(full_name, 1)
    link = search['tracks']['items'][0]['external_urls']['spotify']
    print(json.dumps(search, sort_keys=True, indent=4))
    print(link)
    return link

# parse_track_id("https://open.spotify.com/track/5hAtL8xsBjKAaxkWJAit4L")
# find_link("Marselle - На букву М")
