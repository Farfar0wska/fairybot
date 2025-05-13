import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters

TOKEN = '8066144176:AAGDSb9GtVzGLtDE20a4GW8QX2xTO0isAAc' 

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("❌ Telegram TOKEN is not set in environment variables")

bot = Bot(token=TOKEN)
app = Flask(__name__)

def reduce_to_single_digit(number):
    while number > 9:
        number = sum(int(d) for d in str(number))
    return number

def generate_response(n):
    messages = {
        1: "🔢 Ваше число — 1. Лидер. Сила воли, независимость.",
        2: "🔢 Ваше число — 2. Дипломат. Гармония, партнёрство.",
        3: "🔢 Ваше число — 3. Творец. Радость, креативность.",
        4: "🔢 Ваше число — 4. Практик. Надёжность, стабильность.",
        5: "🔢 Ваше число — 5. Искатель. Свобода, перемены.",
        6: "🔢 Ваше число — 6. Хранитель. Любовь, семья.",
        7: "🔢 Ваше число — 7. Мудрец. Интуиция, анализ.",
        8: "🔢 Ваше число — 8. Стратег. Сила, власть.",
        9: "🔢 Ваше число — 9. Гуманист. Сострадание, мудрость.",
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



