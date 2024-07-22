import telebot

# токен
TOKEN = ''
bot = telebot.TeleBot(TOKEN)

# ожидаем сообщения пользователя
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    # Дублируем текст 10 раз
    duplicated_text = message.text * 10
    # Отправляем обратно
    bot.send_message(message.chat.id, duplicated_text)

bot.polling(none_stop=True)