from music_services.service import build_links


def process_command(message):
    music_url = message
    links = []

    try:
        links = build_links(music_url)
    except Exception as e:
        print(f"error was here {music_url}\nException is {e}")
    finally:
        print(links)
        # if len(links):
        #     bot.send_message(message.from_user.id, "\n".join(links))
        # else:
        #     bot.send_message(message.from_user.id, default_messages["unknown_link"])


process_command("https://open.spotify.com/track/11gXs1fmRhR5Q6PxD3Lhr4?si=KlYewqvwR4qrkHRU7O_DRg")
