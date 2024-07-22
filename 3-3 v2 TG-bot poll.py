import telebot
from telebot import types

# Указываем токен для доступа к API Telegram
TOKEN = ''
# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который создаёт опрос. Для создания опроса напишите первой строй сам вопрос и с каждой новой строки укажите от 2 до 10 вариантов ответа.")

# Обработчик сообщений типа text
@bot.message_handler(content_types=['text'])
def create_poll(message):
    # Разделяем сообщение на строки
    lines = message.text.split('\n')
    # Проверяем количество строк
    if len(lines) < 3 or len(lines) > 11:
        bot.send_message(chat_id=message.chat.id, text='Что-то непонятное, напишите /start и я расскажу о себе и что требуется.')
    else:
        question = lines[0] # Первая строка - вопрос для опроса
        options = lines[1:11] # Остальные строки - варианты ответов (до 11 включительно)
        # Отправляем опрос и закрепляем его в чате
        poll = bot.send_poll(chat_id=message.chat.id, question=question, options=options, is_anonymous=False)
        bot.pin_chat_message(chat_id=message.chat.id, message_id=poll.message_id)

# Запускаем бота
bot.polling()