from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
import logging

# إعداد تسجيل الدخول لمراقبة الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

API_KEY = "7389066468:AAHG5UyOxxHyO5oJ3h4S9_q9asorcPCxx04"
bot = Bot(API_KEY)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Use /sk <your_sk_key> to check your key.')

def check_sk_key(sk_key: str) -> str:
    headers = {
        "Authorization": f"Bearer {sk_key}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        # فحص التوازن
        balance_response = requests.get("https://api.stripe.com/v1/balance", headers=headers)
        balance_response.raise_for_status()
        balance_data = balance_response.json()

        # فحص المستخدمين
        charges_response = requests.get("https://api.stripe.com/v1/charges?limit=15", headers=headers)
        charges_response.raise_for_status()
        charges_data = charges_response.json()

        # فحص مفتاح PK
        checkout_data = {
            'payment_method_types': ['card'],
            'line_items': [{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'T-shirt'},
                    'unit_amount': 2000,
                },
                'quantity': 1,
            }],
            'mode': 'payment',
            'success_url': 'https://your-domain.com/success',
            'cancel_url': 'https://your-domain.com/cancel',
        }
        checkout_response = requests.post("https://api.stripe.com/v1/checkout/sessions", headers=headers, data=checkout_data)
        checkout_response.raise_for_status()
        checkout_session = checkout_response.json()
        
        if 'url' in checkout_session:
            pk_live = "pk_live_xxx"  # يتم استرجاع المفتاح من البيانات بشكل صحيح
        else:
            pk_live = "Error fetching PK"

        # جمع البيانات
        available_balance = balance_data['available'][0]
        pending_balance = balance_data['pending'][0]
        users_count = len(charges_data['data'])
        users_list = [charge['description'] for charge in charges_data['data'] if 'description' in charge]

        # إعداد الرسالة للرد
        result = (f"Key: {sk_key}\n"
                  f"Available Balance: {available_balance['amount']} {available_balance['currency']}\n"
                  f"Pending Balance: {pending_balance['amount']} {pending_balance['currency']}\n"
                  f"PK Live: {pk_live}\n"
                  f"Users Checked: {users_count}\n"
                  f"Users List: {', '.join(users_list) if users_list else 'No descriptions available.'}\n")
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"Error checking the key: {str(e)}")
        return f"Error checking the key: {str(e)}"

def check_sk(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text('Please use the correct format: /sk <your_sk_key>')
        return

    sk_key = context.args[0]
    result = check_sk_key(sk_key)
    update.message.reply_text(result)

def main() -> None:
    try:
        updater = Updater(API_KEY)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("sk", check_sk))

        updater.start_polling()
        updater.idle()
    except Exception as e:
        logger.error(f"Failed to start the bot: {e}")

if __name__ == '__main__':
    main()
