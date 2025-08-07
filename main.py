import time
import threading
from datetime import datetime, timezone
import schedule
from modules import bybit_client, indicators, strategy_rules, chatgpt_assistant
import modules.db_connection as db
import bot

symbol = "BTCUSDT"
interval = 60 # временной интервал, по которому ты хочешь получить свечи (kline / candlestick data).
limit = 300 # Limit for data size per page. [1, 1000]. Default: 200


def job_send_signal():
    print(f"📤 Запуск сигнала в {datetime.now(timezone.utc).strftime('%d %b %Y %H:%M')} UTC")
    try:
        chat_ids = db.get_all_chat_ids()
        df = bybit_client.get_kline(symbol, interval, limit)
        df = indicators.add_indicators(df)
        signal = strategy_rules.generate_signals(df)
        # gpt_response = chatgpt_assistant.ask_gpt_about_market(df)

        for chat_id in chat_ids:
            try:
                bot.send_telegram_signal(chat_id, signal)
                # bot.send_telegram_ai_analyse(chat_id, gpt_response)
            except Exception as e:
                print(f"❌ Ошибка при отправке сигнала в чат {chat_id}: {e}")
        print("✅ Сигнал и аналитика отправлены")
    except Exception as e:
        print(f"❌ Ошибка при выполнении задания: {e}")



def start_scheduler():
    # schedule.every().hour.at(":00")
    schedule.every(10).seconds.do(job_send_signal)
    print("🕒 Планировщик запущен: сигналы будут отправляться каждые 10 секунд.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("⏹️ Планировщик остановлен пользователем.")



if __name__ == "__main__":
    polling_thread = threading.Thread(target=bot.run_bot)
    scheduler_thread = threading.Thread(target=start_scheduler)
    polling_thread.start()
    scheduler_thread.start()
    polling_thread.join()
    scheduler_thread.join()


# print("Торговый сигнал:", signal)
# print("GPT аналитика:", gpt_response)