from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import requests
import json
import logging

app = Flask(__name__)

API_KEY = "6674198155:AAHxHc333DZOL0Z5JHzZTHpAI3O0Zbex5x8"
bot = Bot(token=API_KEY)

dispatcher = Dispatcher(bot, None, use_context=True)

def start(update, context):
    update.message.reply_text('Welcome to the Stripe Key Checker bot!')

def check_sk(update, context):
    secret_key = context.args[0]
    try:
        headers = {
            "Authorization": f"Bearer {secret_key}"
        }
        balance_response = requests.get("https://api.stripe.com/v1/balance", headers=headers)
        balance_response.raise_for_status()

        checkout_data = {
            "payment_method_types[]": "card",
            "line_items[][price_data][currency]": "usd",
            "line_items[][price_data][product_data][name]": "T-shirt",
            "line_items[][price_data][unit_amount]": 2000,
            "line_items[][quantity]": 1,
            "mode": "payment",
            "success_url": "https://your-domain.com/success",
            "cancel_url": "https://your-domain.com/cancel"
        }

        checkout_response = requests.post("https://api.stripe.com/v1/checkout/sessions", headers=headers, data=checkout_data)
        checkout_response.raise_for_status()

        update.message.reply_text(f"The provided key is valid. PK Live: {checkout_response.json()['url']}")
    except requests.exceptions.HTTPError as e:
        update.message.reply_text(f"Error checking the key: {e.response.text}")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("sk", check_sk))

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

if __name__ == '__main__':
    app.run(port=8443)
