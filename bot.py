import os
import logging
import asyncio
import json
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from flask import Flask, request

TOKEN = "7975587876:AAEPJnx7pt-qeqM41ijxg6dRU_wfzgEx1aA"
bot = Bot(token=TOKEN)

BANNED_WORDS = ["كس", "كسمك", "بوسة", "نيك", "قحب", "إباحية", "sex", "porn"]
BANNED_LINKS = ["xxx", "porn", "http", ".com", ".net"]

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

@app.route('/')
def home():
    return "Bot is running!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update_data = json.loads(json_str)  # تحويل النص إلى JSON
    update = Update.de_json(update_data, bot)
    asyncio.run(application.process_update(update))
    return 'ok'

async def set_webhook():
    webhook_url = f'https://telegram-accept.onrender.com/{TOKEN}'
    await bot.set_webhook(url=webhook_url)

async def start(update: Update, context):
    await update.message.reply_text("مرحبا! أنا بوت Popxev Games. استخدم /help للمساعدة.")

async def help(update: Update, context):
    await update.message.reply_text("كيفية استخدام البوت: \n- لا تستخدم كلمات أو روابط ممنوعة. \n- استخدم /contact للتواصل.")

async def contact(update: Update, context):
    await update.message.reply_text(
        "للتواصل معنا: \n"
        "فيسبوك: [Popxev Games](https://www.facebook.com/share/1Dsxdcv7yN/) \n"
        "إنستجرام: [Popxev Games](https://www.instagram.com/popxev_games?igsh=anNwdzR5dXFwc2E4) \n"
        "تيليجرام: [جروب Popxev](https://t.me/Popxevgamesgroup) \n"
        "ديسكورد: [Popxev Games Discord](https://discord.gg/tuRy8Qf7) \n"
    )

async def handle_message(update: Update, context):
    text = update.message.text.lower()
    if any(word in text for word in BANNED_WORDS) or any(link in text for link in BANNED_LINKS):
        await update.message.delete()
        return
    await update.message.reply_text("إذا كنت بحاجة إلى مساعدة، استخدم /help.")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help))
application.add_handler(CommandHandler("contact", contact))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    asyncio.run(set_webhook())
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
