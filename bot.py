import os
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

app = Flask(__name__)

API_KEY = "6674198155:AAHxHc333DZOL0Z5JHzZTHpAI3O0Zbex5x8"
bot = Bot(API_KEY)

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    if request.method == 'POST':
        update = Update.de_json(request.get_json(), bot)
        dispatcher.process_update(update)
    return 'ok'

def set_webhook():
    webhook_url = f"https://<your-domain>/webhook"
    bot.set_webhook(webhook_url)

def start(update, context):
    chat_id = update.message.chat_id
    user = update.message.from_user.username
    message = (
        "<b>Sk CHECKER\n"
        "• Usage: </b><code>/sk sk_live_xxx</code>\n"
        "<b>• Status: ON ✅</b>"
    )
    context.bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')

def check_sk(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    secret_key = text.split("/sk ")[1]
    
    context.bot.send_message(chat_id=chat_id, text="Checking...")

    # Start the checking process
    result = get_pk(secret_key)
    if 'pk_live' in result:
        pk = result
        users_data = get_users(secret_key)
        balance_data = get_balance(secret_key)
        response_message = (
            f"<b>→ Sk Checker\n"
            f"→ 🚺: ⚠️\n\n"
            f"• Key: </b><code>{users_data['SK']}</code>\n"
            f"<b>• Pk: </b><code>{pk}</code>\n"
            f"<b>• Currency: </b>{balance_data['currency']}\n"
            f"<b>• Available Balance: </b>{balance_data['available_amount']}\n"
            f"<b>→ Currency: </b>{balance_data['available_currency']}\n"
            f"<b>• Pending Balance: </b>{balance_data['pending_amount']}\n"
            f"→ Currency: {balance_data['pending_currency']}\n"
            f"• Response: Live Key ✅\n"
            f"• Country: {users_data['country']}\n"
            f"• Users Checked: {users_data['users']}\n"
            f"→Names: {users_data['lists']}\n\n"
            f"→ 🔗 Check out our channels:</b>\n"
            f"🔹 <a href='https://t.me/a_aaq'>FaresM</a>\n"
            f"🔹 <a href='https://t.me/a_aaq'>Group</a>\n"
            f"<b> Checked By: @{user} [Free]</b>"
        )
        context.bot.send_message(chat_id=chat_id, text=response_message, parse_mode='HTML')
    else:
        context.bot.send_message(chat_id=chat_id, text="Invalid Key.")

def get_pk(secret_key):
    url = 'https://api.stripe.com/v1/checkout/sessions'
    headers = {
        'Authorization': f'Bearer {secret_key}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'payment_method_types[]': 'card',
        'line_items[0][price_data][currency]': 'usd',
        'line_items[0][price_data][product_data][name]': 'T-shirt',
        'line_items[0][price_data][unit_amount]': 2000,
        'line_items[0][quantity]': 1,
        'mode': 'payment',
        'success_url': 'https://your-domain.com/success',
        'cancel_url': 'https://your-domain.com/cancel'
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        checkout_session = response.json()
        if 'url' in checkout_session:
            obfuscated_pk = checkout_session['url'].split("#")[1]
            decoded = base64.b64decode(obfuscated_pk)
            deobfed = "".join(chr(5 ^ ord(c)) for c in decoded)
            shuroap = json.loads(deobfed)
            return shuroap["apiKey"]
    return response.json()

def get_users(secret_key):
    url = 'https://api.stripe.com/v1/charges'
    headers = {
        'Authorization': f'Bearer {secret_key}'
    }
    params = {
        'limit': 15
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        charges = response.json()
        charge_count = len(charges['data'])
        descriptions = [charge['description'] for charge in charges['data'] if 'description' in charge]
        currency = charges['data'][0]['currency']
        country = charges['data'][0]['billing_details']['address']['country']
        return {
            "lists": "\n".join(descriptions),
            "SK": f"sk_live_{secret_key.split('_')[2][:5]}•fares•{secret_key.split('_')[2][-5:]}",
            "users": charge_count,
            "currency": currency,
            "country": country
        }
    return {}

def get_balance(secret_key):
    url = 'https://api.stripe.com/v1/balance'
    headers = {
        'Authorization': f'Bearer {secret_key}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        balance = response.json()
        return {
            "available_currency": balance['available'][0]['currency'],
            "available_amount": balance['available'][0]['amount'],
            "pending_currency": balance['pending'][0]['currency'],
            "pending_amount": balance['pending'][0]['amount']
        }
    return {}

dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex(r'^/sk '), check_sk))

if __name__ == '__main__':
    set_webhook()
    app.run(host='0.0.0.0', port=5000)
