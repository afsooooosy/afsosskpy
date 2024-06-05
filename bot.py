import os
import json
import base64
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

app = Flask(__name__)
API_KEY = os.getenv("API_KEY", "7389066468:AAHG5UyOxxHyO5oJ3h4S9_q9asorcPCxx04")
bot = Bot(token=API_KEY)

def set_webhook():
    webhook_url = f"https://afsosskpy.onrender.com{os.getenv('RENDER_EXTERNAL_URL')}/webhook"
    bot.set_webhook(webhook_url)

def start(update, context):
    chat_id = update.message.chat_id
    caption = (
        "<b>Sk CHECKER\n"
        "• Usage: </b><code>/sk sk_live_xxx</code>\n"
        "<b>• Status: ON ✅</b>"
    )
    bot.send_photo(chat_id, photo=f"https://t.me/{update.message.from_user.username}", caption=caption, parse_mode="HTML")

def check_sk(update, context):
    chat_id = update.message.chat_id
    secret_key = context.args[0]
    bot.send_message(chat_id, "CHICK", parse_mode="HTML")

    steps = 10
    time_icons = ['🕛', '🕧', '🕐', '🕜', '🕑', '🕝', '🕒', '🕞', '🕓', '🕟', '🕔', '🕠', '🕕', '🕡', '🕖', '🕢', '🕗', '🕣', '🕘', '🕤', '🕙', '🕥', '🕚', '🕦']
    
    for i in range(steps + 1):
        progress = "⭕" * i + "⚪️" * (steps - i)
        time_icon = time_icons[i % len(time_icons)]
        message = f"{time_icon} Processing... [{progress}] {i * 10}%\n\n🔗 Check out our channels:\n🔹 <a href=\"https://t.me/a_aaq\">FaresM</a>\n🔹 <a href=\"https://t.me/a_aaq\">Group</a>"
        bot.send_message(chat_id, message, parse_mode="HTML")

    pk_result = get_pk(secret_key)
    if 'Error' in pk_result:
        msg = f"<b>→ Sk Checker\n→ Result: Dead\n• Key: </b><code>{secret_key}</code>\n→ Checked By: @{update.message.from_user.username} [Free]"
        bot.send_message(chat_id, msg, parse_mode="HTML")
    else:
        pk = pk_result
        gusr = json.loads(get_users(secret_key))
        gcur = json.loads(get_cur(secret_key))
        skk = gusr["SK"]
        limit = gusr["users"]
        country = gusr["country"]
        currency = gusr["currency"]
        lista = gusr["Lists"]
        cura = gcur["cura"]
        ama = gcur["ama"]
        curp = gcur["curp"]
        amp = gcur["amp"]
        msg = (
            f"<b>→ Sk Checker\n→ 🚺: ⚠️\n\n• Key: </b><code>{skk}</code>\n"
            f"<b>• Pk: </b><code>{pk}</code>\n"
            f"<b>• Currency: </b>{currency}\n"
            f"<b>• Available Balance: </b>{ama}\n"
            f"<b>→ Currency: </b>{cura}\n"
            f"<b>• Pending Balance: {amp}\n→ Currency: {curp}\n"
            f"• Response: Live Key ✅\n"
            f"• Country: {country}\n"
            f"• Users Checked: {limit}\n"
            f"→ Names: {lista}\n\n"
            f"→ 🔗 Check out our channels:</b>\n🔹 <a href=\"https://t.me/a_aaq\">FaresM</a>\n🔹 <a href=\"https://t.me/a_aaq\">Group</a>\n"
            f"<b> Checked By: @{update.message.from_user.username} [Free]</b>"
        )
        bot.send_message(chat_id, msg, parse_mode="HTML")

def get_pk(secret_key):
    try:
        response = requests.post(
            'https://api.stripe.com/v1/checkout/sessions',
            auth=(secret_key, ''),
            data={
                'payment_method_types[]': 'card',
                'line_items[0][price_data][currency]': 'usd',
                'line_items[0][price_data][product_data][name]': 'T-shirt',
                'line_items[0][price_data][unit_amount]': 2000,
                'line_items[0][quantity]': 1,
                'mode': 'payment',
                'success_url': 'https://your-domain.com/success',
                'cancel_url': 'https://your-domain.com/cancel'
            }
        )
        response.raise_for_status()
        checkout_session = response.json()
        if 'url' in checkout_session:
            obfuscated_pk = urldecode(explode("#", checkout_session['url'])[1])
            decoded = base64.b64decode(obfuscated_pk)
            deobfed = ''.join([chr(5 ^ ord(c)) for c in decoded])
            shuroap = json.loads(deobfed)
            pklive = shuroap["apiKey"]
            return pklive
        else:
            return f"Error creating Checkout Session: {checkout_session['error']['message']}"
    except requests.exceptions.RequestException as e:
        return f"Error checking the key: {str(e)}"

def get_cur(secret_key):
    try:
        response = requests.get(
            'https://api.stripe.com/v1/balance',
            auth=(secret_key, '')
        )
        response.raise_for_status()
        decoded_response = response.json()
        json_data = json.dumps({
            "cura": decoded_response['available'][0]['currency'],
            "ama": decoded_response['available'][0]['amount'],
            "curp": decoded_response['pending'][0]['currency'],
            "amp": decoded_response['pending'][0]['amount']
        })
        return json_data
    except requests.exceptions.RequestException as e:
        return f"Error checking the key: {str(e)}"

def get_users(secret_key):
    if secret_key:
        headers = {
            'Authorization': f'Bearer {secret_key}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        params = {
            'limit': 15
        }
        try:
            response = requests.get(
                'https://api.stripe.com/v1/charges',
                headers=headers,
                params=params
            )
            response.raise_for_status()
            charges = response.json()
            charge_count = len(charges['data'])
            lists = [charge.get('description', 'No description') for charge in charges['data']]
            skdegcount = secret_key.split('_')[2]
            ass = skdegcount[:5]
            boobs = skdegcount[-5:]
            currency = charges['data'][0]['currency']
            country = charges['data'][0]['billing_details']['address']['country']
            json_data = json.dumps({
                "Lists": "\n".join(lists),
                "SK": f"sk_live_{ass}•fares•{boobs}",
                "users": charge_count,
                "currency": currency,
                "country": country
            })
            return json_data
        except requests.exceptions.RequestException as e:
            return f"Error checking the key: {str(e)}"

def webhook(request):
    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return 'ok'

dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("sk", check_sk))

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return 'ok'

if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
