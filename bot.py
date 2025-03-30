import os import logging from flask import Flask, request from telegram import Bot, Update from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext import threading

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(name) bot = Bot(token=TOKEN) dispatcher = Dispatcher(bot, None, workers=4, use_context=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def start(update: Update, context: CallbackContext): update.message.reply_text("مرحبا! أنا بوت.")

def handle_message(update: Update, context: CallbackContext): update.message.reply_text("لقد قلت: " + update.message.text)

dispatcher.add_handler(CommandHandler("start", start)) dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

@app.route(f"/{TOKEN}", methods=["POST"]) def webhook(): update = Update.de_json(request.get_json(force=True), bot) dispatcher.process_update(update) return "OK"

def set_webhook(): bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

if name == "main": set_webhook() app.run(host="0.0.0.0", port=5000)

