from abc import abstractmethod


class BaseService:
    def __init__(self, client):
        self.client = client
        self.url = None
        self.parsed_url = None

    @abstractmethod
    def is_acceptable(self, url):
        return NotImplemented

    @abstractmethod
    def get_full_track_name(self):
        return NotImplemented

    @abstractmethod
    def find_link(self, full_name):
        return NotImplemented

    @abstractmethod
    def get_id(self):
        return NotImplemented
