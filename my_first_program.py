#Запрос имени
name = input('Введите ваше имя: ')
#Запрос фамилии
last_name = input ('Введите вашу фамилию: ')
#Запрос отчества
patronymic_name = input ('Введите ваше отчество: ')
#Запрос дня рождения
day = int(input('Введите день вашего рождения: '))
#Запрос месяца рождения
month = int(input('Введите месяц вашего рождения(числом): '))
#Запрос года рождения
year = int(input('Введите год вашего рождения: '))
#Вычисление возраста
from datetime import date
today = date.today()
age = today.year - year - ((today.month, today.day) < (month, day))
#Вывод приветствия и информации о пользователе (F-строка)
print(f'Приветствую, меня зовут {last_name} {name} {patronymic_name} и мне {age} лет.')