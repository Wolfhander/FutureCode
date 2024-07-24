import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

# Указываем токен для доступа к API Telegram
TOKEN = ''
# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    # Создаем inline клавиатуру
    keyboard = InlineKeyboardMarkup()
    # Добавляем 5 одинаковых кнопок со смайликом
    for i in range(5):
        button = InlineKeyboardButton(text='😎', callback_data=str(i))
        keyboard.add(button)
    # Отправляем сообщение с клавиатурой
    bot.send_message(message.chat.id, "Выберите кнопку:", reply_markup=keyboard)

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    # Генерируем случайное победное значение
    winning_value = random.randint(0, 4)
    user_choice = int(call.data)

    # Сравниваем выбор пользователя с победным значением
    if user_choice == winning_value:
        result_message = "Вы выиграли! 🎉🎉🎉"
    else:
        result_message = f"Вы проиграли. 😢😢😢"

    # Отправляем результат пользователю
    bot.send_message(call.message.chat.id, result_message)

# Запускаем бота
bot.polling(none_stop=True)