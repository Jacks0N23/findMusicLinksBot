import os

HOST = "0.0.0.0"
PORT = os.environ.get("PORT", 8443)

token = os.getenv("MUSIC_BOT_TOKEN")

heroku_webhook = "https://find-music-links.herokuapp.com/bot"

welcome_message = (
    "Hello!\n"
    "I can help you share music with your friends using various streaming platforms 🎶.\n"
    "Send me a link to Spotify or Yandex Music and I'll send you links to other platforms that have the same song available."
)
