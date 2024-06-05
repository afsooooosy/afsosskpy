import json
import time
import requests
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, Updater

app = Flask(__name__)

API_KEY = "7389066468:AAHG5UyOxxHyO5oJ3h4S9_q9asorcPCxx04"
bot = Bot(API_KEY)

def set_webhook():
    webhook_url = f"https://afsosskk.onrender.com/webhook"
    bot.set_webhook(webhook_url)

set_webhook()

def get_flag(code):
    flags = {'AD' => '🇦🇩', 'AE' => '🇦🇪', 'AF' => '🇦🇫', 'AG' => '🇦🇬', 'AI' => '🇦🇮', 'AL' => '🇦🇱', 'AM' => '🇦🇲', 'AO' => '🇦🇴', 'AQ' => '🇦🇶', 'AR' => '🇦🇷', 'AS' => '🇦🇸', 'AT' => '🇦🇹', 'AU' => '🇦🇺', 'AW' => '🇦🇼', 'AX' => '🇦🇽', 'AZ' => '🇦🇿', 'BA' => '🇧🇦', 'BB' => '🇧🇧', 'BD' => '🇧🇩', 'BE' => '🇧🇪', 'BG' => '🇧🇬', 'BH' => '🇧🇭', 'BI' => '🇧🇮', 'BJ' => '🇧🇯', 'BL' => '🇧🇱', 'BF' => '🇧🇫', 'BM' => '🇧🇲', 'BN' => '🇧🇳', 'BO' => '🇧🇴', 'BQ' => '🇧🇶', 'BR' => '🇧🇷', 'BS' => '🇧🇸', 'BT' => '🇧🇹', 'BV' => '🇧🇻', 'BW' => '🇧🇼', 'BY' => '🇧🇾', 'BZ' => '🇧🇿', 'CA' => '🇨🇦', 'CC' => '🇨🇨', 'CD' => '🇨🇩', 'CF' => '🇨🇫', 'CG' => '🇨🇬', 'CH' => '🇨🇭', 'CI' => '🇨🇮', 'CK' => '🇨🇰', 'CL' => '🇨🇱', 'CM' => '🇨🇲', 'CN' => '🇨🇳', 'CO' => '🇨🇴', 'CR' => '🇨🇷', 'CU' => '🇨🇺', 'CV' => '🇨🇻', 'CW' => '🇨🇼', 'CX' => '🇨🇽', 'CY' => '🇨🇾', 'CZ' => '🇨🇿', 'DE' => '🇩🇪', 'DJ' => '🇩🇯', 'DK' => '🇩🇰', 'DM' => '🇩🇲', 'DO' => '🇩🇴', 'DZ' => '🇩🇿', 'EC' => '🇪🇨', 'EE' => '🇪🇪', 'EG' => '🇪🇬', 'EH' => '🇪🇭', 'ER' => '🇪🇷', 'ES' => '🇪🇸', 'ET' => '🇪🇹', 'FI' => '🇫🇮', 'FJ' => '🇫🇯', 'FK' => '🇫🇰', 'FM' => '🇫🇲', 'FO' => '🇫🇴', 'FR' => '🇫🇷', 'GA' => '🇬🇦', 'GB' => '🇬🇧', 'GD' => '🇬🇩', 'GE' => '🇬🇪', 'GF' => '🇬🇫', 'GG' => '🇬🇬', 'GH' => '🇬🇭', 'GI' => '🇬🇮', 'GL' => '🇬🇱', 'GM' => '🇬🇲', 'GN' => '🇬🇳', 'GP' => '🇬🇵', 'GQ' => '🇬🇶', 'GR' => '🇬🇷', 'GS' => '🇬🇸', 'GT' => '🇬🇹', 'GU' => '🇬🇺', 'GW' => '🇬🇼', 'GY' => '🇬🇾', 'HK' => '🇭🇰', 'HM' => '🇭🇲', 'HN' => '🇭🇳', 'HR' => '🇭🇷', 'HT' => '🇭🇹', 'HU' => '🇭🇺', 'ID' => '🇮🇩', 'IE' => '🇮🇪', 'IL' => '🇮🇱', 'IM' => '🇮🇲', 'IN' => '🇮🇳', 'IO' => '🇮🇴', 'IQ' => '🇮🇶', 'IR' => '🇮🇷', 'IS' => '🇮🇸', 'IT' => '🇮🇹', 'JE' => '🇯🇪', 'JM' => '🇯🇲', 'JO' => '🇯🇴', 'JP' => '🇯🇵', 'KE' => '🇰🇪', 'KG' => '🇰🇬', 'KH' => '🇰🇭', 'KI' => '🇰🇮', 'KM' => '🇰🇲', 'KN' => '🇰🇳', 'KP' => '🇰🇵', 'KR' => '🇰🇷', 'KW' => '🇰🇼', 'KY' => '🇰🇾', 'KZ' => '🇰🇿', 'LA' => '🇱🇦', 'LB' => '🇱🇧', 'LC' => '🇱🇨', 'LI' => '🇱🇮', 'LK' => '🇱🇰', 'LR' => '🇱🇷', 'LS' => '🇱🇸', 'LT' => '🇱🇹', 'LU' => '🇱🇺', 'LV' => '🇱🇻', 'LY' => '🇱🇾', 'MA' => '🇲🇦', 'MC' => '🇲🇨', 'MD' => '🇲🇩', 'ME' => '🇲🇪', 'MF' => '🇲🇫', 'MG' => '🇲🇬', 'MH' => '🇲🇭', 'MK' => '🇲🇰', 'ML' => '🇲🇱', 'MM' => '🇲🇲', 'MN' => '🇲🇳', 'MO' => '🇲🇴', 'MP' => '🇲🇵', 'MQ' => '🇲🇶', 'MR' => '🇲🇷', 'MS' => '🇲🇸', 'MT' => '🇲🇹', 'MU' => '🇲🇺', 'MV' => '🇲🇻', 'MW' => '🇲🇼', 'MX' => '🇲🇽', 'MY' => '🇲🇾', 'MZ' => '🇲🇿', 'NA' => '🇳🇦', 'NC' => '🇳🇨', 'NE' => '🇳🇪', 'NF' => '🇳🇫', 'NG' => '🇳🇬', 'NI' => '🇳🇮', 'NL' => '🇳🇱', 'NO' => '🇳🇴', 'NP' => '🇳🇵', 'NR' => '🇳🇷', 'NU' => '🇳🇺', 'NZ' => '🇳🇿', 'OM' => '🇴🇲', 'PA' => '🇵🇦', 'PE' => '🇵🇪', 'PF' => '🇵🇫', 'PG' => '🇵🇬', 'PH' => '🇵🇭', 'PK' => '🇵🇰', 'PL' => '🇵🇱', 'PM' => '🇵🇲', 'PN' => '🇵🇳', 'PR' => '🇵🇷', 'PS' => '🇵🇸', 'PT' => '🇵🇹', 'PW' => '🇵🇼', 'PY' => '🇵🇾', 'QA' => '🇶🇦', 'RE' => '🇷🇪', 'RO' => '🇷🇴', 'RS' => '🇷🇸', 'RU' => '🇷🇺', 'RW' => '🇷🇼', 'SA' => '🇸🇦', 'SB' => '🇸🇧', 'SC' => '🇸🇨', 'SD' => '🇸🇩', 'SE' => '🇸🇪', 'SG' => '🇸🇬', 'SH' => '🇸🇭', 'SI' => '🇸🇮', 'SJ' => '🇸🇯', 'SK' => '🇸🇰', 'SL' => '🇸🇱', 'SM' => '🇸🇲', 'SN' => '🇸🇳', 'SO' => '🇸🇴', 'SR' => '🇸🇷', 'SS' => '🇸🇸', 'ST' => '🇸🇹', 'SV' => '🇸🇻', 'SX' => '🇸🇽', 'SY' => '🇸🇾', 'SZ' => '🇸🇿', 'TC' => '🇹🇨', 'TD' => '🇹🇩', 'TF' => '🇹🇫', 'TG' => '🇹🇬', 'TH' => '🇹🇭', 'TJ' => '🇹🇯', 'TK' => '🇹🇰', 'TL' => '🇹🇱', 'TM' => '🇹🇲', 'TN' => '🇹🇳', 'TO' => '🇹🇴', 'TR' => '🇹🇷', 'TT' => '🇹🇹', 'TV' => '🇹🇻', 'TW' => '🇹🇼', 'TZ' => '🇹🇿', 'UA' => '🇺🇦', 'UG' => '🇺🇬', 'UM' => '🇺🇲', 'US' => '🇺🇸', 'UY' => '🇺🇾', 'UZ' => '🇺🇿', 'VA' => '🇻🇦', 'VC' => '🇻🇨', 'VE' => '🇻🇪', 'VG' => '🇻🇬', 'VI' => '🇻🇮', 'VN' => '🇻🇳', 'VU' => '🇻🇺', 'WF' => '🇼🇫', 'WS' => '🇼🇸', 'XK' => '🇽🇰', 'YE' => '🇾🇪', 'YT' => '🇾🇹', 'ZA' => '🇿🇦', 'ZM' => '🇿🇲', 'ZW' => '🇿🇼'
        
        # باقي الرموز...
    }
    return flags.get(code.upper(), '◻️')

def get_name(country_code):
    countries = {
        "AF": "Afghanistan", "AL": "Albania", "DZ": "Algeria", "AS": "American Samoa", "AD": "Andorra",
        "AO": "Angola", "AI": "Anguilla", "AQ": "Antarctica", "AG": "Antigua and Barbuda", "AR": "Argentina",
        # باقي الدول...
    }
    return countries.get(country_code.upper(), '')

def get_cur(sk_key):
    url = 'https://api.stripe.com/v1/balance'
    response = requests.get(url, auth=(sk_key, ''))
    data = response.json()
    return {
        "cura": data['available'][0]['currency'],
        "ama": data['available'][0]['amount'],
        "curp": data['pending'][0]['currency'],
        "amp": data['pending'][0]['amount']
    }

def get_pk(secret_key):
    url = 'https://api.stripe.com/v1/checkout/sessions'
    data = {
        'payment_method_types': ['card'],
        'line_items': [
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'T-shirt'},
                    'unit_amount': 2000,
                },
                'quantity': 1,
            }
        ],
        'mode': 'payment',
        'success_url': 'https://your-domain.com/success',
        'cancel_url': 'https://your-domain.com/cancel',
    }
    response = requests.post(url, data=data, auth=(secret_key, ''))
    session = response.json()
    if 'url' in session:
        obfuscated_pk = session['url'].split("#")[1]
        decoded = base64.b64decode(obfuscated_pk).decode('utf-8')
        deobfuscated = ''.join([chr(5 ^ ord(c)) for c in decoded])
        shuroap = json.loads(deobfuscated)
        return shuroap.get("apiKey", "Error")
    return session.get('error', {}).get('message', 'Error')

def get_users(sk_key):
    url = 'https://api.stripe.com/v1/charges'
    headers = {
        'Authorization': f'Bearer {sk_key}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    params = {'limit': 15}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    charges = data.get('data', [])
    charge_count = len(charges)
    skdegcount = sk_key.split('_')[2]
    ass, boobs = skdegcount[:5], skdegcount[-5:]
    lists = [charge.get('description', 'No description') for charge in charges]
    currency = charges[0]['currency']
    country = charges[0]['billing_details']['address']['country']
    return {
        "Lists": "\n".join(lists),
        "SK": f"sk_live_{ass}•fares•{boobs}",
        "users": charge_count,
        "currency": currency,
        "country": country
    }

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    caption = """
<b>Sk CHECKER
• Usage: </b><code>/sk sk_live_xxx</code>
<b>• Status: ON ✅</b>
"""
    bot.send_photo(chat_id=chat_id, photo="https://t.me/" + update.message.from_user.username, caption=caption, parse_mode="HTML", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("FaresM", url="https://t.me/a_aaq"), InlineKeyboardButton("Group", url="https://t.me/a_aaq")]
    ]))

def check_sk(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    secret_key = context.args[0]
    bot.send_message(chat_id, "CHICK", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("FarrsM", url="https://t.me/a_aaq"), InlineKeyboardButton("Group", url="https://t.me/a_aaq")]
    ]))
    time_icons = ['🕛', '🕧', '🕐', '🕜', '🕑', '🕝', '🕒', '🕞', '🕓', '🕟', '🕔', '🕠', '🕕', '🕡', '🕖', '🕢', '🕗', '🕣', '🕘', '🕤', '🕙', '🕥', '🕚', '🕦']
    for i in range(11):
        progress = '⭕' * i + '⚪️' * (10 - i)
        time_icon = time_icons[i % len(time_icons)]
        message = f"{time_icon} Processing... [{progress}] {i * 10}%\n\n🔗 Check out our channels:\n🔹 <a href=\"https://t.me/a_aaq\">FaresM</a>\n🔹 <a href=\"https://t.me/a_aaq\">Group</a>"
        bot.edit_message_text(chat_id=chat_id, message_id=update.message.message_id + 1, text=message, parse_mode='HTML', reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("FaresM", url="https://t.me/a_aaq"), InlineKeyboardButton("Group", url="https://t.me/a_aaq")]
        ]))
        time.sleep(1)
    result = get_pk(secret_key)
    if "Error" in result:
        msg = f"<b>→ Sk Checker\n→ Result: Dead\n• Key: </b><code>{secret_key}</code>\n→ Checked By: @{update.message.from_user.username} [Free]"
    else:
        pk = result
        users_info = get_users(secret_key)
        currency_info = get_cur(secret_key)
        sk = users_info["SK"]
        users = users_info["users"]
        country = users_info["country"]
        currency = users_info["currency"]
        lists = users_info["Lists"]
        cura = currency_info["cura"]
        ama = currency_info["ama"]
        curp = currency_info["curp"]
        amp = currency_info["amp"]
        flag = get_flag(country)
        namec = get_name(country)
        msg = f"""
<b>→ Sk Checker\n→ 🚺: ⚠️\n\n• Key: </b><code>{sk}</code>\n<b>• Pk: </b><code>{pk}</code>\n<b>• Currency: </b>{currency}\n<b>• Available Balance: </b>{ama}\n<b>→ Currency : </b>{cura}\n<b>• Pending Balance: {amp}\n→ Currency : {curp}\n• Response: Live Key ✅\n• Country: {namec} {flag}\n• Users Checked : {users}\n→Names : {lists}\n\n→ 🔗 Check out our channels:</b>\n🔹 <a href="https://t.me/a_aaq">FaresM</a>\n🔹 <a href="https://t.me/a_aaq">Group</a>\n<b> Checked By: @{update.message.from_user.username} [Free]</b>
"""
    bot.edit_message_text(chat_id=chat_id, message_id=update.message.message_id + 1, text=msg, parse_mode='HTML', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("FaresM", url="https://t.me/a_aaq"), InlineKeyboardButton("Group", url="https://t.me/a_aaq")]
    ]))

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

def main():
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("sk", check_sk))

    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
