import os
import logging
import asyncio
import json
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from flask import Flask, request, jsonify

TOKEN = "7975587876:AAEPJnx7pt-qeqM41ijxg6dRU_wfzgEx1aA"
bot = Bot(token=TOKEN)

BANNED_WORDS = [
    "كس", "كسمك", "كسك", "بوسة", "نيك", "نك", "حواك", "حوي", "نحويك", "نيكك", "زك", "زكك",
    "قحب", "قحبة", "شرذيذ", "مضاجعة", "جماع", "ممارسة", "اغتصاب", "عاهرة", "دعارة", "مؤخرة",
    "صدر", "ثدي", "فرج", "استمناء", "احتلام", "لواط", "سحاق", "شاذ", "شاذة", "زنا", "إباحية",
    "سكسي", "sexy", "sex", "porn", "pussy", "dick", "ass", "boobs", "cock", "bitch", "slut"
]

BANNED_LINKS = ["xxx", "x", "xn", "porn", "www", "http", ".com", ".net", ".org", ".xyz"]

app = Flask(__name__)

async def create_application():
    application = Application.builder().token(TOKEN).build()
    await application.initialize()
    return application

async def set_webhook():
    webhook_url = f'https://telegram-accept.onrender.com/{TOKEN}'
    await bot.set_webhook(url=webhook_url)

async def start(update: Update, context):
    await update.message.reply_text("مرحبا! أنا بوت Popxev Games. إذا كنت بحاجة للمساعدة، استخدم /help.")

async def help(update: Update, context):
    await update.message.reply_text("كيفية استخدام البوت: \n- لا تستخدم كلمات أو روابط ممنوعة. \n- إذا كنت بحاجة للتواصل، استخدم /contact.")

async def contact(update: Update, context):
    await update.message.reply_text(
        "للتواصل معنا: \n\n"
        "فيسبوك: [Popxev Games](https://www.facebook.com/share/1Dsxdcv7yN/) \n"
        "إنستجرام: [Popxev Games](https://www.instagram.com/popxev_games?igsh=anNwdzR5dXFwc2E4) \n"
        "تيليجرام: [بوت Popxev](https://t.me/Popxevgamesgroup) \n"
        "جروب تيليجرام: [Popxev Games Group](https://t.me/Popxevgamesgroup) \n"
        "ديسكورد: [Popxev Games Discord](https://discord.gg/tuRy8Qf7) \n"
    )

async def handle_message(update: Update, context):
    text = update.message.text.lower()
    if any(word in text for word in BANNED_WORDS) or any(link in text for link in BANNED_LINKS):
        await update.message.delete()
        return
    await update.message.reply_text("إذا كنت بحاجة إلى مساعدة، يمكنك استخدام الأمر /help.")

@app.route(f'/{TOKEN}', methods=['POST'])
async def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = Update.de_json(json.loads(json_str), bot)
    asyncio.create_task(application.process_update(update))
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    application = asyncio.run(create_application())

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("contact", contact))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    asyncio.run(set_webhook())
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
