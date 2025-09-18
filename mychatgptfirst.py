import os
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
client = OpenAI(api_key="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")
# 🔑 Вставь свои ключи
TELEGRAM_TOKEN = "8311368695:AAHkVdoT_0sPiP2Xa44-QKGCN3BZ3HmrYNA"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

# Функция старта
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой AI-репетитор. Напиши что-нибудь на английском 😊")

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Новый запрос к ChatGPT
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # или gpt-4 если есть доступ
        messages=[{"role": "user", "content": user_message}]
    )

    bot_reply = response.choices[0].message.content
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
