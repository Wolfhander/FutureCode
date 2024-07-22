# 1) Создайте родительский класс `Animal` с атрибутами `name` и `species`. 
# Дайте им также метод `make_sound()`, который выводит звук, издаваемый животными.
# 2) Создайте подклассы `Dog` и `Cat`, которые наследуют от класса `Animal`. 
# Дайте каждому из них свой собственный метод `make_sound()`, который выводит соответствующий звук (`"Гав"` для собаки и `"Мяу"` для кота).
class animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def make_sound(self):
        print(f'"Животное издает звук"')

class dog(animal):
    def make_sound(self):
        print(f'{self.name} говорит "Гав"')

class cat(animal):
    def make_sound(self):
        print(f'{self.name} говорит "Мяу"')

dog_inst = dog("Сэм", "Собака")
dog_inst.make_sound()

cat_inst = cat("Рыся", "Кошка")
cat_inst.make_sound()