import os
import logging
import asyncio
from quart import Quart, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = "7975587876:AAEPJnx7pt-qeqM41ijxg6dRU_wfzgEx1aA"
WEBHOOK_URL = "https://telegram-popxev-bot.onrender.com"

app = Quart(__name__)
bot = Bot(token=TOKEN)

BANNED_WORDS = [
    "كس", "كسمك", "كسك", "بوسة", "نيك", "نك", "حواك", "حوي", "نحويك", "نيكك", "زك", "زكك",
    "قحب", "قحبة", "شرذيذ", "مضاجعة", "جماع", "ممارسة", "اغتصاب", "عاهرة", "دعارة", "مؤخرة",
    "صدر", "ثدي", "فرج", "استمناء", "احتلام", "لواط", "سحاق", "شاذ", "شاذة", "زنا", "إباحية",
    "سكسي", "sexy", "sex", "porn", "pussy", "dick", "ass", "boobs", "cock", "bitch", "slut"
]

BANNED_LINKS = ["xxx", "x", "xn", "porn", "www", "http", ".com", ".net", ".org", ".xyz"]

application = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text("مرحبا! أنا بوت Popxev Games.")

async def handle_message(update: Update, context):
    text = update.message.text.lower()
    if any(word in text for word in BANNED_WORDS) or any(link in text for link in BANNED_LINKS):
        await update.message.delete()
        return
    await update.message.reply_text("تم استلام رسالتك!")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(await request.json(), bot)
    await application.process_update(update)
    return "OK", 200

async def set_webhook():
    await bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

if __name__ == "__main__":
    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=5000)
