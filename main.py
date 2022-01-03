"""
Main module
"""

import os
from game import Game
from colors import *

def start_the_game(username):
    """
    Начаать игру
    :param username: имя пользователя
    :return: подтверждения или неподтверждение пользователя о начале игры
    """

    confirm_the_start_of_the_game = f"\n{username}, Вы хотите начать новую игру? (д/н): "
    start_game = input(confirm_the_start_of_the_game)

    while start_game not in ['д', 'Д', 'н', 'Н']:
        red("\nВы хотите начать новую игру? (д/н): ")
        start_game = input(confirm_the_start_of_the_game)

    return start_game

def main():
    """
    Запуск программы
    :return: None
    """

    username = input("\nВведите Ваше имя: ").upper()
    start_game = start_the_game(username)

    while start_game in ['д', 'Д']:
        game = Game(username)
        game.start()
        del game
        start_game = start_the_game(username)

    blue(f'\n{username}, До скорой встречи')

if __name__ == "__main__":
    main()