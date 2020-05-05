import os
import telebot
from flask import Flask, request

from config import token, heroku_webhook, welcome_message, HOST, PORT
import spotify
import ya_music

bot = telebot.TeleBot(token)
bot.stop_polling()

server = Flask(__name__)

sessionContext = {}


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.from_user.id, welcome_message)


@bot.message_handler(content_types=["text"])
def handle_intent(message):
    print(f"text handler {message}")
    process_command(message)


def process_command(message):
    music_url = message.text
    another_link = "cannot identify music provider or you send album(it's not supported now), only tracks"
    try:
        if ya_music.is_ya_music(music_url):
            full_name = ya_music.get_full_track_name(music_url)
            another_link = spotify.find_link(full_name)
        elif spotify.is_spotify(music_url):
            full_name = spotify.get_full_track_name(music_url)
            another_link = ya_music.find_link(full_name)
    except Exception as e:
        print(f"error was here {music_url}\nException is {e}")
    finally:
        bot.send_message(message.from_user.id, another_link)


@server.route("/bot", methods=["POST"])
def post_message():
    req = request.stream.read().decode("utf-8")
    print(f"post bot {req}")
    bot.process_new_updates([telebot.types.Update.de_json(req)])
    return "/bot", 200


@server.route("/bot", methods=["GET"])
def get_message():
    req = request.stream.read().decode("utf-8")
    print(f"get bot {req}")
    process_command(req)
    return "/bot", 200


@server.route("/")
def webhook_handler():
    bot.remove_webhook()
    bot.set_webhook(url=heroku_webhook)
    status_msg = f"i'm live. listening on {HOST}:{PORT}"
    return status_msg, 200


if os.getenv("PYTHON_ENV") == "development":
    bot.polling(none_stop=True)
else:
    bot.delete_webhook()
    bot.set_webhook(url=heroku_webhook)

server.run(host=HOST, port=PORT)
