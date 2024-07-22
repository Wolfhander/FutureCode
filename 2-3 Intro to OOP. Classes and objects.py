# Создайте класс `Car`, который имеет атрибуты `make` (марка автомобиля), `model` (модель автомобиля) и `year` (год выпуска). 
# Дайте им также метод `display_info()`, который выводит информацию о машине (марка, модель и год).
class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def display_info(self):
        print(f"Car Info: {self.make} {self.model} ({self.year})")
my_car = Car("Skoda", "Octavia A7FL", 2019)
my_car.display_info()