from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import re

TOKEN = "7975587876:AAEPJnx7pt-qeqM41ijxg6dRU_wfzgEx1aA"

banned_words = ["شرموط", "شرموطة", "قحبة", "زاملة", "زامل", "قحب", "نك", "نيك", "نيكمك", "نكمك", "زبي", "زب"]

banned_links = [
    "www", "إعلان", "porn", "xxx", "x", ".com", "hetai"
]

custom_replies = {
    "مرحبا": "أهلًا وسهلًا بك! 😊",
    "كيف حالك؟": "أنا بخير، وأنت؟",
    "ما اسمك؟": "أنا بوت Popxev Games! 🤖"
}

async def start(update: Update, context: CallbackContext):
    message = f"""مرحبًا {update.effective_user.first_name}!

🔗 قنواتنا الرسمية:
1️⃣ يوتيوب: [Popxev Games](https://youtube.com/@popxevgames-v)
2️⃣ إنستجرام: [Popxev Games](https://www.instagram.com/popxev_games)
3️⃣ فيسبوك: [Popxev Games](https://www.facebook.com/share/1Dsxdcv7yN/)
5️⃣ ديسكورد: [انضم إلينا](https://discord.gg/hK33DD74QN)
    """
    await update.message.reply_text(message)

async def help_command(update: Update, context: CallbackContext):
    help_text = """🔹 أوامر البوت:
/start - بدء البوت
/help - عرض الأوامر
/contact - للتواصل معنا
/discord - للانضمام إلى سيرفر ديسكورد"""
    await update.message.reply_text(help_text)

async def contact(update: Update, context: CallbackContext):
    contact_text = """💬 للتواصل معنا، يمكنك زيارة قنواتنا الرسمية:
1️⃣ يوتيوب: [Popxev Games](https://youtube.com/@popxevgames-v)
2️⃣ إنستجرام: [Popxev Games](https://www.instagram.com/popxev_games)
3️⃣ فيسبوك: [Popxev Games](https://www.facebook.com/share/1Dsxdcv7yN/)
5️⃣ ديسكورد: [انضم إلينا](https://discord.gg/hK33DD74QN)
    """
    await update.message.reply_text(contact_text)

async def discord(update: Update, context: CallbackContext):
    await update.message.reply_text("🎮 انضم إلى سيرفر ديسكورد: https://discord.gg/hK33DD74QN")

async def handle_messages(update: Update, context: CallbackContext):
    text = update.message.text

    for word in banned_words:
        if word in text:
            await update.message.delete()
            await update.message.reply_text("تم حذف الرسالة لأنها تحتوي على كلمات غير لائقة.")
            return

    for link in banned_links:
        if re.search(link, text):
            await update.message.delete()
            await update.message.reply_text("تم حذف الرسالة لأنها تحتوي على رابط غير مرغوب فيه.")
            return

    reply = custom_replies.get(text, "يمكنك استعمال /help لمعرفة أكثر")
    await update.message.reply_text(reply)

async def webhook(request):
    update = Update.de_json(request.json, application.bot)
    await application.process_update(update)

def main():
    global application
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("contact", contact))
    application.add_handler(CommandHandler("discord", discord))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    application.bot.set_webhook("https://telegram-popxev-bot.onrender.com/webhook")
    print("✅ Webhook تم تعيينه بنجاح...")

if __name__ == "__main__":
    main()
