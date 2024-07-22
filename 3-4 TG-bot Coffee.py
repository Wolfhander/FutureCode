import requests
import telebot
from random import choice

# Указываем токен для доступа к API Telegram
TOKEN = ''
# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Функция для получения случайного фото кофе
def get_random_coffee_image():
    response = requests.get('https://coffee.alexflipnote.dev/random.json')
    data = response.json()
    return data['file']

# Обработчик команды /coffee
@bot.message_handler(commands=['coffee'])
def send_coffee_photo(message):
    coffee_image_url = get_random_coffee_image()  # Получаем случайное изображение кофе
    bot.send_photo(message.chat.id, coffee_image_url)  # Отправляем его пользователю

# Запускаем бота
bot.polling(none_stop=True)