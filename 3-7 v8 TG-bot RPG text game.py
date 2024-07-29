import telebot  # Импортируем библиотеку для работы с Telegram Bot API
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton  # Импортируем необходимые типы для создания интерфейса

# Указываем токен для доступа к API Telegram
TOKEN = ''
# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения состояния пользователей
users = {}

# Класс, представляющий пользователя игры
class User:
    def __init__(self):
        self.health = 100  # Изначальное здоровье пользователя
        self.inventory = []  # Список предметов в инвентаре пользователя

    # Метод для добавления предмета в инвентарь
    def add_item(self, item):
        self.inventory.append(item)

    # Метод для использования предмета из инвентаря
    def use_item(self, item):
        if item in self.inventory:
            if item == 'health_potion':  # Если предмет - зелье здоровья
                self.health += 20  # Увеличиваем здоровье на 20
                self.inventory.remove(item)  # Удаляем использованный предмет

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    users[message.chat.id] = User()  # Создаем нового пользователя и добавляем его в словарь
    welcome_text = """Приветствую Вас в RPG игре!
Вы отправляетесь в интересное приключение. 
В пути Вы можете использовать команды /status и /inventory
Готовы ли Вы начать?

Выберите действие:
"""  # Текст приветственного сообщения
    # Создание интерфейса с кнопками
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Начать приключение", callback_data="start_adventure"))  # Кнопка для начала приключения
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)  # Отправка сообщения с кнопками

# Обработка команды /status
@bot.message_handler(commands=['status'])
def status(message):
    user = users.get(message.chat.id)
    if user:
        bot.send_message(message.chat.id, f"Ваше здоровье: {user.health}\n Инвентарь: {', '.join(user.inventory) if user.inventory else 'пусто'}")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, запустите игру, нажав /start.")

# Обработка команды /inventory
@bot.message_handler(commands=['inventory'])
def inventory(message):
    user = users.get(message.chat.id)
    if user:
        bot.send_message(message.chat.id, f"Ваш инвентарь: {', '.join(user.inventory) if user.inventory else 'пусто'}")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, запустите игру, нажав /start.")

# Обработка нажатий на inline-кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user = users[call.message.chat.id]  # Получаем объект пользователя из словаря

    if call.data == "start_adventure":
        bot.send_message(call.message.chat.id, "Вы находитесь в лесу и видите перед собой две тропы.")
        markup = InlineKeyboardMarkup()
        # Создаем кнопки для выбора пути
        markup.add(InlineKeyboardButton("Пойти налево", callback_data="go_left"))
        markup.add(InlineKeyboardButton("Пойти направо", callback_data="go_right"))
        bot.send_message(call.message.chat.id, "Выберите путь:", reply_markup=markup)

    elif call.data == "go_left":
        user.health -= 10  # Уменьшаем здоровье пользователя на 10
        bot.send_message(call.message.chat.id, "Вы наткнулись на ловушку и потеряли 10 здоровья. Сейчас у вас {} здоровья.".format(user.health))
        markup = InlineKeyboardMarkup()
        # Кнопки для дальнейших действий
        markup.add(InlineKeyboardButton("Исследовать дальше", callback_data="explore_further_left"))
        markup.add(InlineKeyboardButton("Вернуться обратно", callback_data="go_back"))
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)

    elif call.data == "explore_further_left":
        user.add_item('health_potion')  # Добавляем зелье здоровья в инвентарь пользователя
        bot.send_message(call.message.chat.id, "Вы нашли зелье здоровья и добавили его в свой инвентарь.")
        markup = InlineKeyboardMarkup()
        # Кнопки для использования зелья или возвращения на перекресток
        markup.add(InlineKeyboardButton("Использовать зелье", callback_data="use_health_potion"))
        markup.add(InlineKeyboardButton("Вернуться на перекресток", callback_data="go_back"))
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)

    elif call.data == "use_health_potion":
        user.use_item('health_potion')  # Используем зелье здоровья
        bot.send_message(call.message.chat.id, "Вы использовали зелье здоровья. Сейчас у вас {} здоровья.".format(user.health))
        markup = InlineKeyboardMarkup()
        # Кнопка для возвращения на перекресток
        markup.add(InlineKeyboardButton("Вернуться на перекресток", callback_data="go_back"))
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)

    elif call.data == "go_back":
        bot.send_message(call.message.chat.id, "Вы вернулись на перекресток и видите перед собой две тропы.")
        markup = InlineKeyboardMarkup()
        # Кнопки для выбора нового пути
        markup.add(InlineKeyboardButton("Пойти налево", callback_data="go_left"))
        markup.add(InlineKeyboardButton("Пойти направо", callback_data="go_right"))
        bot.send_message(call.message.chat.id, "Выберите путь:", reply_markup=markup)

    elif call.data == "go_right":
        bot.send_message(call.message.chat.id, "Вы встретили дружелюбного торговца. Он предлагает вам обменять зелье здоровья на меч.")
        markup = InlineKeyboardMarkup()
        # Если в инвентаре пользователя есть зелье здоровья, делаем кнопку для обмена
        if 'health_potion' in user.inventory:
            markup.add(InlineKeyboardButton("Обменять зелье на меч", callback_data="trade_sword"))
        # Кнопка для продолжения пути
        markup.add(InlineKeyboardButton("Продолжить путь", callback_data="continue_right"))
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)

    elif call.data == "trade_sword":
        # Если у пользователя есть зелье здоровья, осуществляем обмен
        if 'health_potion' in user.inventory:
            user.inventory.remove('health_potion')  # Удаляем зелье здоровья из инвентаря
            user.add_item('sword')  # Добавляем меч в инвентарь
            bot.send_message(call.message.chat.id, "Вы обменяли зелье на меч. Сейчас у вас в инвентаре: {}".format(', '.join(user.inventory)))
        markup = InlineKeyboardMarkup()
        # Кнопка для продолжения пути
        markup.add(InlineKeyboardButton("Продолжить путь", callback_data="continue_right"))
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)

    elif call.data == "continue_right":
        bot.send_message(call.message.chat.id, "Вы подошли к заброшенному замку, что вы сделаете?")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Войти в замок", callback_data="enter_castle"))
        markup.add(InlineKeyboardButton("Обойти замок", callback_data="bypass_castle"))
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)

    elif call.data == "enter_castle":
        bot.send_message(call.message.chat.id, "В замке вас встречает дух, который требует отгадать загадку для продолжения.")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Отгадать загадку", callback_data="solve_riddle"))
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)

    elif call.data == "solve_riddle":
        riddle = "Что уходит утром на четырех ногах, днем на двух, а вечером на трех?"
        bot.send_message(call.message.chat.id, "Загадка: {}".format(riddle))
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Человек", callback_data="correct_riddle"))
        markup.add(InlineKeyboardButton("Собака", callback_data="wrong_riddle"))
        bot.send_message(call.message.chat.id, "Выберите ответ:", reply_markup=markup)

    elif call.data == "correct_riddle":
        bot.send_message(call.message.chat.id, "Дух одобрительно кивает и открывает тайный ход за троном.")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Идти дальше", callback_data="secret_path"))
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)

    elif call.data == "secret_path":
        # Сообщение пользователю, что он выбрал тайный путь
        bot.send_message(call.message.chat.id, "Вы решаетесь пойти по тайному пути за троном.")

        # Описание первой комнаты на тайном пути
        bot.send_message(call.message.chat.id, "Вы оборачиваетесь и видите длинный темный коридор, освещенный факелами на стенах.")

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Исследовать коридор", callback_data="explore_corridor"))
        markup.add(InlineKeyboardButton("Вернуться обратно", callback_data="return_back"))
        bot.send_message(call.message.chat.id, "Что вы хотите сделать?", reply_markup=markup)

    elif call.data == "explore_corridor":
        # Детали исследования коридора
        bot.send_message(call.message.chat.id, "Вы медленно двигаетесь по коридору, и запах сыра начинает заполнять ваши ноздри.")

        # Выбор действия в коридоре
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Пройти до конца коридора", callback_data="reach_end"))
        markup.add(InlineKeyboardButton("Обследовать стены", callback_data="examine_walls"))
        bot.send_message(call.message.chat.id, "Что вы хотите сделать дальше?", reply_markup=markup)

    elif call.data == "return_back":
        # Действие при возвращении из тайного пути
        bot.send_message(call.message.chat.id, "Вы решаете вернуться обратно ко входу в замок, осознавая, что пока не готовы к таким приключениям.")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Вернуться ко входу в замок", callback_data="continue_right"))
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)

    elif call.data == "reach_end":
        # Событие при достижении конца коридора
        bot.send_message(call.message.chat.id, "Вы доходите до конца коридора и видите массивную дубовую дверь с тяжелым засовом.")

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Открыть дверь", callback_data="open_door"))
        markup.add(InlineKeyboardButton("Осмотреть дверь", callback_data="examine_door"))
        bot.send_message(call.message.chat.id, "Что сделать дальше?", reply_markup=markup)

    elif call.data == "examine_walls":
        # События при обследовании стен коридора
        bot.send_message(call.message.chat.id, "Вы внимательно исследуете стены и обнаруживаете потайную нишу с сундуком.")

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Открыть сундук", callback_data="open_chest"))
        markup.add(InlineKeyboardButton("Игнорировать и идти дальше", callback_data="reach_end"))
        bot.send_message(call.message.chat.id, "Ваши действия?", reply_markup=markup)

    elif call.data == "open_door":
        # Открытие массивной дубовой двери и событие после этого
        bot.send_message(call.message.chat.id, "Вы с трудом открываете тяжелую дверь и попадаете в зал, наполненный золотом и драгоценностями.")
        bot.send_message(call.message.chat.id, "Похоже, вы обнаружили сокровищницу замка.")

        # Дальнейшие действия в сокровищнице
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Поискать магические предметы", callback_data="find_magic_items"))
        markup.add(InlineKeyboardButton("Взять золото и уйти", callback_data="take_gold"))
        bot.send_message(call.message.chat.id, "Что вы хотите сделать?", reply_markup=markup)

    elif call.data == "examine_door":
        # Обследование двери
        bot.send_message(call.message.chat.id, "Вы обнаруживаете, что дверь запечатана магическим замком. Нужен ключ, чтобы открыть её.")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Вернуться и искать ключ", callback_data="explore_corridor"))
        bot.send_message(call.message.chat.id, "Похоже без ключа не обойтись. Возвращаемся и ищем ключ.", reply_markup=markup)

    elif call.data == "open_chest":
        # Событие при открытии сундука
        bot.send_message(call.message.chat.id, "Вы медленно открываете сундук и видите внутри множество странных артефактов.")

        # Дальнейшие действия с найденными артефактами
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Обследовать артефакты", callback_data="examine_artifacts"))
        markup.add(InlineKeyboardButton("Забрать сундук с собой", callback_data="take_chest"))
        bot.send_message(call.message.chat.id, "Ваши действия?", reply_markup=markup)

    elif call.data == "find_magic_items":
        # Поиск магических предметов в сокровищнице
        bot.send_message(call.message.chat.id, "Вы внимательно осматриваете сокровища и находите несколько магических предметов, которые могут вам пригодиться в дальнейшем.")
        # Заключительное сообщение для этого пути
        bot.send_message(call.message.chat.id, "Теперь у вас есть редкие магические предметы, которые помогут в вашем приключении. Ваше путешествие продолжается!")

    elif call.data == "take_gold":
        # Взятие золота и уход
        bot.send_message(call.message.chat.id, "Вы набиваете свои карманы золотом и решаете уйти, понимая, что здесь есть еще много неизведанных уголков.")
        # Заключительное сообщение для этого пути
        bot.send_message(call.message.chat.id, "Теперь вы богаты, но ваше приключение еще не окончено. Ваше путешествие продолжается!")

    elif call.data == "examine_artifacts":
        # Обследование артефактов
        bot.send_message(call.message.chat.id, "Вы обнаруживаете старинный магический ключ среди артефактов. Возможно, он подойдет к двери в конце коридора.")
        # Возвращение к коридору с новым ключом
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Вернуться к двери", callback_data="reach_end"))
        bot.send_message(call.message.chat.id, "Теперь у вас есть ключ. Возвращаемся к двери.", reply_markup=markup)

    elif call.data == "take_chest":
        # Забрать сундук с собой
        bot.send_message(call.message.chat.id, "Вы решаете взять сундук с собой, надеясь, что его содержимое пригодится вам в дальнейшем.")
        # Продолжение пути с сундуком
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Продолжить путь", callback_data="reach_end"))
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)

    elif call.data == "wrong_riddle":
        bot.send_message(call.message.chat.id, "Дух негодует и атакует вас. Вы теряете 20 здоровья.")
        user.health -= 20
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Попытаться снова", callback_data="enter_castle"))
        bot.send_message(call.message.chat.id, "Сейчас у вас {} здоровья. Выберите действие:".format(user.health), reply_markup=markup)

    elif call.data == "bypass_castle":
        bot.send_message(call.message.chat.id, "Вы обошли замок и продолжаете путь. На горизонте виднеется деревня.")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Направиться в деревню", callback_data="go_village"))
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)

    elif call.data == "go_village":
        bot.send_message(call.message.chat.id, "Прибыв в деревню, вы встречаете старейшину, который просит вашей помощи в борьбе с чудовищем, терзающим их земли.")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Согласиться помочь", callback_data="agree_help"))
        markup.add(InlineKeyboardButton("Отказаться", callback_data="decline_help"))
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)

    elif call.data == "agree_help":
        bot.send_message(call.message.chat.id, "Вы соглашается помочь деревне. Вам предстоит битва с чудовищем.")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Приготовиться к бою", callback_data="prepare_battle"))
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)

    elif call.data == "decline_help":
        bot.send_message(call.message.chat.id, "Вы отказались помочь деревне и продолжаете свое приключение в другую сторону.")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Продолжить путь", callback_data="continue_journey"))
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)

    elif call.data == "prepare_battle":
        bot.send_message(call.message.chat.id, "Вы сразились с чудовищем и победили его, жители деревни благодарны вам.")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Завершить приключение", callback_data="end_journey"))
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)

    elif call.data == "continue_journey":
        bot.send_message(call.message.chat.id, "Ваше приключение продолжается...")

    elif call.data == "end_journey":
        bot.send_message(call.message.chat.id, "Вы успешно завершили приключение. Спасибо за игру!")

# Запуск бота с бесконечным опросом новых сообщений
bot.infinity_polling()