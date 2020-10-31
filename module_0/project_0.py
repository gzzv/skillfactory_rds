# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 16:26:27 2020

@author: Ildar
"""

import numpy as np
def score_game(game_core):
    '''Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число'''
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(1,101, size=(1000))
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return(score)

def game_core_v3(number):
    '''Сначала устанавливаем предсказание равным половине диапазона, 
    а потом перемещаем границы в зависимости от того, больше число или меньше нужного.
        Функция принимает загаданное число и возвращает число попыток'''
    count = 0
    low_limit = 1 # фиксируем нижнюю границу диапазона
    high_limit = 100 # фиксируем верхнюю границу диапазона
    predict = (low_limit + high_limit)//2 # первое предсказание берем равным половине диапазона, т.е 50
    while number != predict:
        predict = (low_limit + high_limit)//2 # внутри цикла будем смещать границы и таким образом менять предсказание
        count+=1
        if number > predict: 
            low_limit = predict + 1 # операция смещения границы, если загаданное число больше предсказания
        elif number < predict: 
            high_limit = predict - 1 # если заданное число меньше предсказания
    return(count) # выход из цикла, если угадали

score_game(game_core_v3)