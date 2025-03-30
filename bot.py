from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application
import json

TOKEN = "7975587876:AAEPJnx7pt-qeqM41ijxg6dRU_wfzgEx1aA"

app = Flask(__name__)

application = Application.builder().token(TOKEN).build()
application.initialize()

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = Update.de_json(json.loads(json_str), application.bot)

    application.create_task(application.process_update(update))
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(port=5000)
