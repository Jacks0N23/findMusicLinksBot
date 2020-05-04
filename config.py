import os

token = os.getenv('MUSIC_BOT_TOKEN')

heroku_webhook = "https://find-music-links.herokuapp.com/bot"

welcome_message = "Hello!\n" \
                  "I can help you to share music with your friends in their music apps.\n" \
                  "Enter link to spotify or yandex music and i'll send you link to another services "