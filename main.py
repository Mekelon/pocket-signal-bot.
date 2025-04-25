
import telebot
from flask import Flask, request

# Прямо вставленные данные (небезопасно, только для тестов!)
TOKEN = "7803509296:AAHBXhCp7jgbmrIh7KJvvpk0qe0-7Kjn8DI"
OWNER_ID = 962322661

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=["start"])
def start_message(message):
    if message.chat.id == OWNER_ID:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("Получить сигнал")
        bot.send_message(message.chat.id, "Добро пожаловать! Нажми кнопку, чтобы получить сигнал.", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Доступ ограничен. Только для владельца.")

@bot.message_handler(func=lambda m: m.text == "Получить сигнал")
def signal(m):
    if m.chat.id == OWNER_ID:
        bot.send_message(m.chat.id, "Сигнал: ВВЕРХ на 3 минуты (тестовый сигнал)")
    else:
        bot.send_message(m.chat.id, "У тебя нет доступа.")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode("utf-8"))])
    return "ok", 200

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
