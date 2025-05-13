from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters
import os

TOKEN = '8066144176:AAGDSb9GtVzGLtDE20a4GW8QX2xTO0isAAc'  # замените на свой токен от BotFather
bot = Bot(token=TOKEN)

app = Flask(__name__)

def reduce_to_single_digit(number):
    while number > 9:
        number = sum(int(d) for d in str(number))
    return number

def generate_response(n):
    messages = {
        1: "🔢 Ваше число — 1. Лидер. Сила воли, независимость, индивидуальность.",
        2: "🔢 Ваше число — 2. Дипломат. Гармония, чувствительность, партнёрство.",
        3: "🔢 Ваше число — 3. Творец. Радость, креативность, самовыражение.",
        4: "🔢 Ваше число — 4. Практик. Надёжность, стабильность, труд.",
        5: "🔢 Ваше число — 5. Искатель. Свобода, перемены, приключения.",
        6: "🔢 Ваше число — 6. Хранитель. Любовь, семья, забота.",
        7: "🔢 Ваше число — 7. Мудрец. Интуиция, анализ, духовность.",
        8: "🔢 Ваше число — 8. Стратег. Сила, власть, достижение целей.",
        9: "🔢 Ваше число — 9. Гуманист. Сострадание, мудрость, служение.",
    }
    return messages.get(n, "Ошибка в вычислении числа.")

def handle_message(update: Update, context):
    text = update.message.text
    digits = [int(ch) for ch in text if ch.isdigit()]
    if not digits:
        update.message.reply_text("Пожалуйста, введите дату в формате: 13 04 1995")
        return
    total = sum(digits)
    result = reduce_to_single_digit(total)
    update.message.reply_text(generate_response(result))

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

if __name__ == '__main__':
    app.run(port=8443)
