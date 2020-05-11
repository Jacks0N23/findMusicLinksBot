from music_services.apple_music import AppleMusic
from music_services.spotify import Spotify
from music_services.ya_music import YaMusic
from music_services.youtube_music import Youtube


class ServiceFactory:
    def __init__(self):
        self.all_services = {}

    def get(self, key):
        return self.all_services.get(key)

    def create(self, key, builder):
        self.all_services[key] = builder

    def list_services(self):
        return list(self.all_services.values())

    def list_services_without(self, service_to_remove):
        services = self.list_services()
        services.remove(service_to_remove)
        return services


factory = ServiceFactory()
factory.create('YA_MUSIC', YaMusic())
factory.create('SPOTIFY', Spotify())
factory.create('YOUTUBE', Youtube())
factory.create('APPLE_MUSIC', AppleMusic())


def build_links(url):
    parsed_url_service = [service.is_acceptable(url) for service in factory.list_services()]
    base_service = list(filter(None, parsed_url_service))[0]
    name = base_service.get_full_track_name()
    other_services = factory.list_services_without(base_service)
    return get_links(name, other_services)


def get_links(name, other_services):
    __links = []
    for service in other_services:
        link = service.find_link(name)
        if link:
            __links.append(link)
    return __links
