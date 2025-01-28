import time
import datetime
from threading import Thread
import telebot
from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()

# Секретные данные из .env
API_TOKEN = os.getenv('API_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Создаем экземпляр бота
bot = telebot.TeleBot(API_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global CHAT_ID
    CHAT_ID = message.chat.id
    bot.reply_to(message,
                 f"\ud83d\udc4b Привет! Я бот, который будет напоминать тебе о зарядках и очистке кофемашины\nВаш Chat ID: {CHAT_ID}")

# Функции для отправки сообщений
def send_morning_exercise_reminder():
    if CHAT_ID:
        bot.send_message(CHAT_ID, "Не забудьте провести зарядку! \ud83c\udfcb\ufe0f\u200d\u2642\ufe0f")

def send_afternoon_exercise_reminder():
    if CHAT_ID:
        bot.send_message(CHAT_ID, "Пора размяться! \ud83c\udfc3\ufe0f\u200d\u2642\ufe0f")

def send_coffee_machine_cleaning_reminder():
    if CHAT_ID:
        bot.send_message(CHAT_ID, "Не забудьте очистить кофемашину! \u2615\ufe0f")

# Функция для проверки времени и отправки уведомлений
def reminder_scheduler():
    while True:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        current_day = now.strftime("%A")

        # Проверяем и отправляем напоминания
        if current_time == "22:32":  # Установите нужное время
            send_morning_exercise_reminder()
        elif current_time == "22:33":  # Установите нужное время
            send_afternoon_exercise_reminder()
        elif current_time == "22:34" and current_day in ["Wednesday", "Friday"]:  # Установите нужное время
            send_coffee_machine_cleaning_reminder()

        # Пауза на 60 секунд перед следующей проверкой
        time.sleep(60)

# Запускаем проверку времени в отдельном потоке
scheduler_thread = Thread(target=reminder_scheduler, daemon=True)
scheduler_thread.start()

# Основной цикл бота
bot.polling(none_stop=True)