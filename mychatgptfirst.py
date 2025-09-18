import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# ==== Получаем ключи из переменных окружения ====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ==== Инициализация OpenAI ====
client = OpenAI(api_key=OPENAI_API_KEY)

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот с ChatGPT. Напиши мне что-нибудь.")

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # или gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "Ты помощник в Telegram."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        bot_reply = f"Ошибка при запросе к OpenAI: {e}"

    await update.message.reply_text(bot_reply)

# Основная функция
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
