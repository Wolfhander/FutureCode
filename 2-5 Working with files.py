# Создайте текстовый файл с названием "sample.txt" и написать программу для чтения и вывода его содержимого на экран.

with open("sample.txt", "w") as file:
    file.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit... Ну и что-то ещё записываем в файл sample.txt ")

with open("sample.txt", "r") as file:
    contents = file.read()
    print(contents)