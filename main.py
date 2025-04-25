
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
    app.run(host="0.0.0.0", port=10000)
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# Получаем токен из переменных окружения Render
TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=TOKEN)

# Flask-приложение
app = Flask(__name__)

# Telegram-приложение
application = Application.builder().token(TOKEN).build()

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот работает и готов отправлять сигналы!")

# Добавляем хендлер
application.add_handler(CommandHandler("start", start))

# Обработка Webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.process_update(update)
    return "ok", 200

# Проверка доступности
@app.route("/")
def home():
    return "Бот работает!"

# Один раз установить webhook (временный блок — можно удалить после установки)
with app.app_context():
    webhook_url = f"https://pocket-signal-bot.onrender.com/{TOKEN}"
    bot.set_webhook(url=webhook_url)
    print("Webhook установлен:", webhook_url)

# Запуск сервера
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
