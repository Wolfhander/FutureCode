try:
 #Приветствие, описание функционала калькулятор
 print(f'Приветствую, это простой калькулятор, способный складывать (+), вычитать (-), умножать (*) и делить (/)')
 #Определение функций
 def add(x,y):
    return x + y
 def subtract(x,y):
    return x - y
 def multiply(x,y):
    return x * y
 def divide(x,y):
    return x / y
 #Набор функций калькулятор
 print("Возможные действия:")
 print(" + Сложение")
 print(" - Вычитание")
 print(" * Умножение")
 print(" / Деление")
 #Выбор пользоваталем действия
 while True:
    choice = input("Выберите действие( +, -, *, / ): ")
    if choice in ('+', '-', '*', '/'):
 #Ввод пользователем значений
        number1 = float(input("Введите первое число: "))
        number2 = float(input("Введите второе число: "))
 #Выполнение действия и вывод результата
        if choice == '+':
           print('Вычисление: ',number1, "+", number2)
           print('Результат: ',add(number1, number2))
        elif choice == '-':
           print('Вычисление: ',number1, "-", number2)
           print('Результат: ',subtract(number1, number2))
        elif choice == '*':
           print('Вычисление: ',number1, "*", number2)
           print('Результат: ',multiply(number1, number2))
        elif choice == '/':
           print('Вычисление: ',number1, "/", number2)
           print('Результат: ',divide(number1, number2))
        break
except Exception as err:
 print (f"Произошла ошибка: введённые данные некорректны или выполнение действия невозможно. Причина ошибки: {err}")
