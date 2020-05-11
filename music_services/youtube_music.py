import json
import os
from urllib.parse import parse_qs, urlparse
from googleapiclient.discovery import build
from music_services.BaseService import BaseService


class Youtube(BaseService):

    def __init__(self):
        super().__init__(build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY")))

    def is_acceptable(self, url):
        self.url = url
        self.parsed_url = urlparse(url)
        if self.is_youtube():
            return self
        return None

    def get_full_track_name(self):
        video_id = self.get_id()

        results = (
            self.client.videos()
                .list(part="snippet", id=video_id)
                .execute()
                .get("items", [])
        )

        # get the first result (should be the only one anyway)
        found_video = list(filter(lambda x: x["id"] == video_id, results))
        if len(found_video):
            video = found_video[0]
            return video["snippet"]["title"]

        return None

    def find_link(self, full_name):
        search_result = (
            self.client.search()
                .list(q=full_name, maxResults=1, part="snippet")
                .execute()
                .get("items", [])
        )
        video_results = list(filter(lambda x: x["id"]["kind"] == "youtube#video", search_result))

        link = None

        try:
            link = f"https://www.youtube.com/watch?v={video_results[0]['id']['videoId']}"
        except Exception as e:
            print("YoutubeMusic: link not found", e)
            print(json.dumps(video_results, indent=4))
        return link

    def get_id(self):
        if self.__is_full_url():
            params = parse_qs(self.parsed_url.query)
            return params["v"][0]
        elif self.__is_short_url():
            return self.parsed_url.path.replace("/", "")

    def is_youtube(self):
        return self.__is_short_url() or self.__is_full_url()

    def __is_full_url(self):
        return "youtube.com" in self.parsed_url.netloc

    def __is_short_url(self):
        return "youtu.be" in self.parsed_url.netloc
