import os

HOST = "0.0.0.0"
PORT = os.environ.get("PORT", 8443)

token = os.getenv("MUSIC_BOT_TOKEN")

heroku_webhook = "https://find-music-links.herokuapp.com/bot"

default_messages = {
    "welcome": """Hello!
    I can help you share music with your friends using various streaming platforms 🎶.
    Send me a link to Spotify or Yandex Music or Youtube Music or Apple Music and I'll send you links to other platforms that have the same song available 💯
    """,
    "unknown_link": """I don't understand this. I'm support only links to tracks. Please, send me another link 🎶
    """,
}
