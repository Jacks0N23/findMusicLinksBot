import json
import os
import applemusicpy
from urllib.parse import urlparse, parse_qs
from music_services.BaseService import BaseService


class AppleMusic(BaseService):
    # TODO need to ask somehow region aka storefront from user, coz marselle didn't available in us or ca
    storefront = "ru"

    def __init__(self):
        key_id = os.getenv("APPLE_KEY_ID")
        team_id = os.getenv("APPLE_TEAM_ID")
        secret_key = os.getenv("APPLE_SECRET_KEY")
        super().__init__(applemusicpy.AppleMusic(secret_key=secret_key, key_id=key_id, team_id=team_id))

    def is_acceptable(self, url):
        self.url = url
        self.parsed_url = urlparse(url)
        if self.is_apple_music():
            return self
        return None

    def get_full_track_name(self):
        track = self.client.song(self.get_id(), storefront=self.storefront)
        track_info = track["data"][0]["attributes"]
        # print(json.dumps(track_info, indent=4, ensure_ascii=False))
        full_name = f"{track_info['artistName']} — {track_info['name']}"
        print(full_name)
        return full_name

    def get_id(self):
        track_id = parse_qs(self.parsed_url.query)["i"][0]
        print(track_id)
        return track_id

    def find_link(self, full_name):
        results = self.client.search(full_name, storefront=self.storefront, types=["songs"], limit=1)
        link = None
        try:
            link = results["results"]["songs"]["data"][0]["attributes"]["url"]
            print(link)
        except Exception as e:
            print("AppleMusic: link not found", e)
            print(json.dumps(results["results"], indent=4))
        return link

    def is_apple_music(self):
        return "music.apple.com" in self.parsed_url.netloc

# service = AppleMusic()
# service.find_link("Masego — Girls That Dance")
# service.find_link("Masego & Medasin — Girls That Dance")

# service.is_acceptable("https://music.apple.com/ru/album/girls-that-dance/1099376295?i=1099376359")
# service.get_full_track_name()