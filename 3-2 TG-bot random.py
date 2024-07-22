import telebot
import random

# токен
TOKEN = ''
# создание бота
bot = telebot.TeleBot(TOKEN)

# если есть слово "рандом"
@bot.message_handler(func=lambda message: 'рандом' in message.text.lower())
def random_number(message):
    # Отправляем случайное число от 0 до 100
    bot.send_message(message.chat.id, str(random.randint(0, 100)))

# все остальные сообщения
@bot.message_handler(func=lambda message: True)
def duplicate_message(message):
    # Дублируем текст
    bot.send_message(message.chat.id, message.text)

# запускаем бота
bot.polling(none_stop=True)