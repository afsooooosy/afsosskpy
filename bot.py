import logging
import requests
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request
import os

# إعدادات البوت وAPI KEY
API_KEY = "7389066468:AAHG5UyOxxHyO5oJ3h4S9_q9asorcPCxx04"
bot = Bot(API_KEY)

# إعداد Flask
app = Flask(__name__)

# إعداد سجل التحديثات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# دوال المساعدة
def get_balance(secret_key):
    url = "https://api.stripe.com/v1/balance"
    response = requests.get(url, auth=(secret_key, ''))
    return response.json()

def get_users(secret_key):
    url = "https://api.stripe.com/v1/charges?limit=15"
    response = requests.get(url, auth=(secret_key, ''))
    return response.json()

def get_pk(secret_key):
    url = "https://api.stripe.com/v1/checkout/sessions"
    data = {
        'payment_method_types[]': 'card',
        'line_items[0][price_data][currency]': 'usd',
        'line_items[0][price_data][product_data][name]': 'T-shirt',
        'line_items[0][price_data][unit_amount]': 2000,
        'line_items[0][quantity]': 1,
        'mode': 'payment',
        'success_url': 'https://example.com/success',
        'cancel_url': 'https://example.com/cancel'
    }
    response = requests.post(url, auth=(secret_key, ''), data=data)
    if response.status_code == 200:
        return response.json().get('url', '').split('#')[1]
    else:
        return response.json().get('error', {}).get('message', 'Unknown error')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! استخدم الأمر /sk لفحص مفتاح Stripe.")

async def check_sk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    secret_key = ' '.join(context.args)
    if not secret_key:
        await update.message.reply_text("يرجى إرسال المفتاح السري بعد الأمر /sk.")
        return

    pk = get_pk(secret_key)
    if 'pk_live' in pk:
        balance = get_balance(secret_key)
        users = get_users(secret_key)
        response_message = (
            f"PK: {pk}\n"
            f"Balance: {balance}\n"
            f"Users: {users}"
        )
        await update.message.reply_text(response_message)
    else:
        await update.message.reply_text(f"Error checking the key: {pk}")

# إعداد البوت
app = Application.builder().token(API_KEY).build()

# أوامر البوت
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("sk", check_sk))

# نقطة النهاية لـ webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    app.update_queue.put(update)
    return 'ok'

# إعداد webhook
@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    webhook_url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/webhook"
    bot.set_webhook(url=webhook_url)
    return f"Webhook set to {webhook_url}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
