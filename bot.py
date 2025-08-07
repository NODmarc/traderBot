from datetime import datetime, timezone
import requests
from config import TELEGRAM_BOT_API_KEY
import telebot
import modules.db_connection as db

bot = telebot.TeleBot(token=TELEGRAM_BOT_API_KEY)

chat_ids = db.get_all_chat_ids()

@bot.message_handler(commands=['start'])
def start_message(message):
    message_text = "Вы подписаны на торговые сигналы."
    bot.send_message(message.chat.id, message_text)
    db.insert_subscribers(message.chat.id)
    print(f"[INFO] User {message.chat.id} processed.")

@bot.message_handler(commands=['stop'])
def stop_message(message):
    db.delete_subscriber(message.chat.id)
    bot.send_message(message.chat.id, "Вы отписались от сигналов.")

def send_telegram_signal(chat_id, signal):
    now = datetime.now(timezone.utc).strftime('%d %b %Y UTC %H:%M')
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": f"📈Торговый сигнал на {now}:\n\n💡 {signal}",
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"✅ Сигнал отправлен в чат {chat_id}")
        else:
            print(f"❌ Ошибка Telegram API для чата {chat_id}: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка при отправке в чат {chat_id}: {e}")

def send_telegram_ai_analyse(chat_id, signal):
    now = datetime.now(timezone.utc).strftime('%d %b %Y UTC %H:%M')
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": signal,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"✅ Аналитика отправлена в чат {chat_id}")
        else:
            print(f"❌ Ошибка Telegram API для чата {chat_id}: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка при отправке в чат {chat_id}: {e}")

def run_bot():
    bot.polling()