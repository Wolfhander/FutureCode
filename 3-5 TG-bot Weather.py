import telebot
import requests

TOKEN = ''
WEATHER_URL = 'https://api.open-meteo.com/v1/forecast'

# коды погоды (взял с http://meteoweb.ru/maps001.php , описание для метеонаблюдателей, не корректировал)
weather_codes = {
    0: 'Ясно',
    1: 'В основном ясно',
    2: 'Облачно с прояснениями',
    3: 'Пасмурно',
    4:	'видимость снижена из-за дыма (смога)',
    5:	'мгла',
    6:	'в воздухе содержатся частицы пыли, не поднятые ветром в районе станции в период наблюдений',
    7:	'ветер поднимает пыль или частицы песка в районе станции (или непосредственно на территории станции), но песчаная буря не наблюдается, не наблюдаются и песчаные вихри',
    8:	'хорошо оформленные песчаные или пыльные вихри в районе станции (или на ее территории) на момент наблюдений или в предшествующий час, но нет ни песчаной, ни пыльной бури',
    9:	'песчаная или пыльная буря, видимая со станции в момент наблюдений, или наблюдавшаяся в течение предшествующего часа на территории станции',
    10:	'дымка',
    11:	'"пятна" приземного тумана',
    12:	'сплошной слой приземного тумана. Высота слоя не выше 2 м на суше и не более 10 м над поверхностью воды',
    13:	'зарницы (видны молнии, но грома не слышно)',
    14:	'видны зоны выпадающих осадков из облаков, но осадки не достигают поверхности земли (моря)',
    15:	'видны выпадающие осадки, достигающие поверхности земли (моря), но на расстоянии более 5 км от станции',
    16:	'видны выпадающие осадки, достигающие поверхности земли (моря) рядом со станцией, но не на самой станции',
    17:	'гроза, но на момент наблюдений осадков нет',
    18:	'шквалы на территории станции или в пределах видимости',
    19:	'воронки под основаниями кучево-дождевой облачности, не достигающие поверхности земли в момент наблюдений или в течение предшествующего часа',
    20:	'морось или снежные зерна',
    21:	'дождь',
    22:	'снег',
    23:	'дождь со снегом, снежная крупа',
    24:	'переохлажденный дождь или морось (гололедные явления)',
    25:	'ливневый дождь',
    26:	'ливневый снег',
    27:	'ливневый град или ливневый дождь с градом',
    28:	'туман, ледяной туман',
    29:	'гроза (с осадками или без них)',
    30:	'слабая или умеренная песчаная или пыльная буря, интенсивность которой убывала в течение часа, предшествующего наблюдениям',
    31:	'слабая или умеренная пыльная или песчаная буря без изменения интенсивности в течение предшествующего часа',
    32:	'слабая или умеренная пыльная или песчаная буря, интенсивность которой увеличивалась в течение часа, предшествующего наблюдениям',
    33:	'сильная пыльная или песчаная буря, интенсивность которой убывала в течение часа, предшествующего наблюдениям',
    34:	'сильная пыльная или песчаная буря без изменения интенсивности в течение предшествующего часа',
    35:	'сильная пыльная или песчаная буря, интенсивность которой увеличивалась в течение часа, предшествующего наблюдениям',
    36:	'слабый или умеренный поземок',
    37:	'сильный поземок (но ниже уровня глаз наблюдателя)',
    38:	'слабая или умеренная метель',
    39:	'сильная метель',
    40:	'туман, видимый со станции в момент наблюдений, но не на территории станции в течение предшествующего часа',
    41:	'разорванный туман',
    42:	'туман, ставший тоньше за прошедший час; небо видно',
    43:	'туман, ставший тоньше за прошедший час; небо не видно',
    44:	'туман без изменений; небо видно',
    45:	'туман без изменений; небо не видно',
    46:	'туман либо образовался, либо усилился за прошедший час; небо видно',
    47:	'туман либо образовался, либо усилился за прошедший час; небо не видно',
    48:	'туман, сквозь который небо видно',
    49:	'туман, сквозь который небо не видно.',
    50:	'слабая морось с перерывами на момент наблюдений',
    51:	'слабая морось без перерывов на момент наблюдений',
    52:	'умеренная морось с перерывами на момент наблюдений',
    53:	'умеренная морось без перерывов на момент наблюдений',
    54:	'сильная (плотная) морось с перерывами на момент наблюдений',
    55:	'сильная (плотная) морось без перерывов на момент наблюдений',
    56:	'слабая переохлажденная морось',
    57:	'умеренная или сильная (плотная) переохлажденная морось',
    58:	'слабая морось с дождем',
    59:	'умеренный или сильный дождь с моросью',
    60:	'слабый дождь с перерывами на момент наблюдений',
    61:	'слабый дождь без перерывов на момент наблюдений',
    62:	'умеренный дождь с перерывами на момент наблюдений',
    63:	'умеренный без перерывов на момент наблюдений',
    64:	'сильный дождь с перерывами на момент наблюдений',
    65:	'сильный без перерывов на момент наблюдений',
    66:	'слабый переохлажденный дождь',
    67:	'умеренный или сильный переохлажденный дождь',
    68:	'слабый дождь (или морось) со снегом',
    69:	'умеренный или сильный дождь (морось) со снегом',
    70:	'слабый снег с перерывами на момент наблюдений',
    71:	'слабый снег без перерывов на момент наблюдений',
    72:	'умеренный снег с перерывами на момент наблюдений',
    73:	'умеренный снег без перерывов на момент наблюдений',
    74:	'сильный снег с перерывами на момент наблюдений',
    75:	'сильный снег без перерывов на момент наблюдений',
    76:	'ледяные иглы (с туманом или без него)',
    77:	'снежные зерна (с туманом или без него)',
    78:	'отдельные звездоподобные кристаллы снег',
    79:	'ледяной дождь',
    80:	'слабый ливневый дождь',
    81:	'умеренный или сильный ливневый дождь',
    82:	'сильнейший ливневый дождь',
    83:	'слабый ливневый снег с дождем',
    84:	'умеренный или сильный ливневый снег с дождем',
    85:	'слабый ливневый снег',
    86:	'умеренный или сильный ливневый снег',
    87:	'слабый ливневый мелкий град (снежная или ледяная крупа) с дождем или без него, или с дождем и снегом',
    88: 'умеренный или сильный мелкий град (снежная или ледяная крупа) с дождем или без него, или с дождем и снегом',
    89:	'слабый град с дождем или без него, или с дождем и снегом, не связанный с грозой',
    90:	'умеренный или сильный град с дождем или без него, или с дождем и снегом, не связанный с грозой',
    91:	'слабый дождь на момент наблюдений',
    92:	'умеренный или сильный дождь на момент наблюдений',
    93:	'слабый снег или дождь со снегом (или градом) на момент наблюдений',
    94:	'умеренный или сильный снег или дождь со снегом (или градом) на момент наблюдений',
    95:	'слабая или умеренная гроза без града, но с дождем или снегом на момент наблюдений',
    96:	'слабая или умеренная гроза с градом на момент наблюдений',
    97:	'сильная гроза без града, но с дождем или снегом на момент наблюдений',
    98:	'гроза, сопровождаемая песчаной или пылевой бурей на момент наблюдений',
    99:	'сильная гроза с градом на момент наблюдений',
}
# Направление ветра (румбы и градусы)
def get_wind_direction(degree):
    directions = [
        (0, "С"), (22.5, "ССВ"), (45, "СВ"), (67.5, "ВСВ"),
        (90, "В"), (112.5, "ВЮВ"), (135, "ЮВ"), (157.5, "ЮЮВ"),
        (180, "Ю"), (202.5, "ЮЮЗ"), (225, "ЮЗ"), (247.5, "ЗЮЗ"),
        (270, "З"), (292.5, "ЗСЗ"), (315, "СЗ"), (337.5, "ССЗ"),
        (360, "С"),
    ]
    return min(directions, key=lambda x: abs(x[0] - degree))[1]

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /weather
@bot.message_handler(commands=['weather'])
def send_location_request(message):
    # Запрос геопозиции и кнопка для отправки
    bot.send_message(message.chat.id, "Отправьте ваше местоположение.", reply_markup=telebot.types.ReplyKeyboardMarkup(
        one_time_keyboard=True).add(telebot.types.KeyboardButton("Отправить местоположение", request_location=True)))
# Получение координат из геопозиции, запрос погоды по координатам
@bot.message_handler(content_types=['location'])
def get_weather(message):
    lat = message.location.latitude
    lon = message.location.longitude
    response = requests.get(WEATHER_URL, params={'latitude': lat, 'longitude': lon, 'current_weather': True}).json()

    temperature = response['current_weather']['temperature']
    wind_speed = response['current_weather']['windspeed']
    wind_direction = response['current_weather']['winddirection']
    weather_code = response['current_weather']['weathercode']

    weather_description = weather_codes.get(weather_code, 'неизвестно')
    wind_direction_text = f"{get_wind_direction(wind_direction)} ({wind_direction}°)"

    bot.send_message(message.chat.id, f"Температура: {temperature}°C \n Скорость ветра: {wind_speed} м/с \n "
                                        f"Направление ветра: {wind_direction_text} \n Описание погоды: {weather_description}")

# Запускаем бота
bot.polling(none_stop=True)