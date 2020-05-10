import json
import os
from urllib import parse

import applemusicpy

key_id = os.getenv("APPLE_KEY_ID")
team_id = os.getenv("APPLE_TEAM_ID")
secret_key = os.getenv("APPLE_SECRET_KEY")

am = applemusicpy.AppleMusic(secret_key=secret_key, key_id=key_id, team_id=team_id)

# TODO need to ask somehow region aka storefront from user, coz marselle didn't available in us or ca
storefront = "ru"


def find_link(full_name):
    results = am.search(full_name, storefront=storefront, types=["songs"], limit=1)
    print(json.dumps(results["results"]["songs"], indent=4))
    link = results["results"]["songs"]["data"][0]["attributes"]["url"]
    print(link)
    return link


def parse_full_name(track_id):
    track = am.song(track_id, storefront=storefront)
    track_info = track["data"][0]["attributes"]
    full_name = f"{track_info['artistName']} — {track_info['name']}"
    print(full_name)
    print(json.dumps(track_info, indent=4, ensure_ascii=False))
    return full_name


def parse_track_id(am_url):
    assert isinstance(am_url, str)
    parsed_url = parse.urlparse(am_url)
    if is_apple_music(am_url):
        track_id = parse.parse_qs(parsed_url.query)["i"][0]
        print(track_id)
        return track_id

    else:
        print("it's not apple music")
        return None


def get_full_track_name(am_url):
    track_id = parse_track_id(am_url)
    return parse_full_name(track_id)


def is_apple_music(am_url):
    return parse.urlparse(am_url).netloc.__contains__("music.apple.com")


# find_link("Marselle - На букву М")
# parse_full_name("1483756855")
# parse_track_id("https://music.apple.com/ru/album/%D0%BD%D0%B0-%D0%B1%D1%83%D0%BA%D0%B2%D1%83-%D0%BC/1483756838?i=1483756855")
# get_full_track_name("https://music.apple.com/ru/album/%D0%BD%D0%B0-%D0%B1%D1%83%D0%BA%D0%B2%D1%83-%D0%BC/1483756838?i=1483756855")
