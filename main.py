import os
import telebot
from flask import Flask, request

from config import token, heroku_webhook, default_messages, HOST, PORT
from service import ServiceBuilder

bot = telebot.TeleBot(token)
bot.stop_polling()

server = Flask(__name__)

sessionContext = {}


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.from_user.id, default_messages["welcome"])


@bot.message_handler(content_types=["text"])
def handle_intent(message):
    print(f"text handler {message}")
    process_command(message)


def process_command(message):
    music_url = message.text
    unknown_link = default_messages["unknown_link"]
    links = []

    try:
        links = ServiceBuilder(music_url).build_links()
    except Exception as e:
        print(f"error was here {music_url}\nException is {e}")
    finally:
        if len(links):
            bot.send_message(message.from_user.id, "\n".join(links))
        else:
            bot.send_message(message.from_user.id, unknown_link)


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
