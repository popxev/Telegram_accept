from telegram import Update from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext from flask import Flask, request, jsonify import asyncio import logging import os

TOKEN = "7975587876:AAEPJnx7pt-qeqM41ijxg6dRU_wfzgEx1aA" WEBHOOK_URL = "https://telegram-popxev-bot.onrender.com/webhook"

app = Flask(name) logging.basicConfig(level=logging.INFO)

banned_words = ["شرموط", "شرموطة", "قحبة", "زاملة", "زامل", "قحب", "نك", "نيك", "نيكمك", "نكمك", "زبي", "زب"] banned_links = ["www", "إعلان", "porn", "xxx", "x", ".com", "hetai"]

custom_replies = { "مرحبا": "أهلًا وسهلًا بك!", "كيف حالك؟": "أنا بخير، وأنت؟", "ما اسمك؟": "أنا بوت Popxev Games!" }

application = Application.builder().token(TOKEN).build() application.initialize()

async def start(update: Update, context: CallbackContext): message = f"""مرحبًا {update.effective_user.first_name}! قنواتنا الرسمية: يوتيوب: https://youtube.com/@popxevgames-v1w?si=QulhnL1ZbhMU3mDK إنستجرام: https://www.instagram.com/popxev_games?igsh=anNwdzR5dXFwc2E4 فيسبوك: https://www.facebook.com/share/1Dsxdcv7yN/ ديسكورد: https://discord.gg/tuRy8Qf7 """ await update.message.reply_text(message)

async def handle_messages(update: Update, context: CallbackContext): text = update.message.text.lower()

for word in banned_words:
    if word in text:
        await update.message.delete()
        await update.message.reply_text("تم حذف الرسالة لأنها تحتوي على كلمات غير لائقة.")
        return

for link in banned_links:
    if link in text:
        await update.message.delete()
        await update.message.reply_text("تم حذف الرسالة لأنها تحتوي على رابط غير مرغوب فيه.")
        return

reply = custom_replies.get(text, "يمكنك استعمال /help لمعرفة أكثر")
await update.message.reply_text(reply)

@app.route("/webhook", methods=["POST"]) def webhook(): try: update = Update.de_json(request.get_json(), application.bot) asyncio.run(application.process_update(update)) return jsonify({"status": "ok"}), 200 except Exception as e: logging.error(f"خطأ في webhook: {str(e)}") return jsonify({"error": str(e)}), 500

def main(): application.add_handler(CommandHandler("start", start)) application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages)) application.run_webhook( listen="0.0.0.0", port=int(os.environ.get("PORT", 5000)), webhook_url=WEBHOOK_URL )

if name == "main": main()

