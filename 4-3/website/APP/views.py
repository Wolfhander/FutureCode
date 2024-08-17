from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path
import random

def index(request):
    return HttpResponse('Hello World')


def gen_numb(request):
    # Генерируем 3 случайных числа от 0 до 3
    numbers = [random.randint(0, 3) for _ in range(3)]

    if numbers[0] == numbers[1] == numbers[2]:
        # Если все числа равны
        response = f"Числа: {numbers}. Победа, все 3 числа равны!"
    elif len(set(numbers)) == len(numbers):
        # Если все числа уникальны
        response = f"Числа: {numbers}. Повезет в следующий раз!"
    else:
        # Если некоторые числа равны, но не все три сразу
        response = f"Числа: {numbers}. До победы оставался всего один шажок!"

    return HttpResponse(response)