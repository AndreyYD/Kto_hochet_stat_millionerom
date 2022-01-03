"""
Модуль игры 'Кто хочет стать миллионером'
"""

import os
import hints
from questions import Questions
from colors import *

class Game:
    """
    Класс Игры
    """

    _the_winnings_for_the_correct_answer = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000,
                                           64000, 125000, 250000, 500000, 1000000]
    _number_of_questions = len(_the_winnings_for_the_correct_answer)
    _guaranteed_sum = [_the_winnings_for_the_correct_answer[4], _the_winnings_for_the_correct_answer[9],
                       _the_winnings_for_the_correct_answer[14]]

    def __init__(self, username):
        self._questions = Questions().get_questions()
        self._username = username
        self._current_question = -1
        self._current_won_sum = 0
        self._hints = [hints.Fifty_Fifty(), hints.Call_a_friend(), hints.Hall_help()]

    def _get_current_question(self):
        """
        Получить текущий вопрос
        :return: текущий вопрос
        """

        return self._questions[self._current_question]

    def _to_next_question(self):
        """
        Переход к следующиму вопросу
        :return: None
        """

        if self._current_question < Game._number_of_questions - 1:
            self._current_question += 1
            self._to_question()
        else:
            self._finish()

    def _to_current_question(self, show_question=True):
        """
        Вернуться к текущему вопросу
        :param show_question: показать вопрос, если True
        :return: None
        """

        self._to_question(is_next_question=False, show_question=show_question)

    def _to_question(self, is_next_question=True, show_question=True):
        """
        Вывести вопрос и дождаться выбора ответа пользователем
        :param is_next_question: следующий вопрос (True) или текущий вопрос (False)
        :param show_question: показывать вопрос ()True или не показывать вопро (False)
        :return: None
        """

        if is_next_question:
            Game.clear_scr()
            self._print_questions()

        if show_question:
            self._print_question(is_next_question)

        choice = self._get_user_choice()
        self._execute_users_choice(choice)

    def _print_questions(self):
        """
        Распечатать дерево списка вопросов со стрелкой на текущем вопросе
        :return: None
        """

        for i, l in enumerate(Game._the_winnings_for_the_correct_answer):
            if i == self._current_question:
                print("--> ", end='')
            else:
                print("    ", end='')

            if i == self._current_question - 1:
                negative(f"${l}")
            elif l in Game._guaranteed_sum:
                bold(f"${l}")
            else:
                print(f"${l}")

    def _print_question(self, is_next_question):
        """
        Распечатать вопрос
        :param is_next_question: следующий вопрос (True) или текущий вопрос (False)
        :return: None
        """

        if is_next_question:
            if self._current_question == 0:
                number = "первый"
            elif self._current_question == Game._number_of_questions - 1:
                number = "последний"
            else:
                number = "следующий"

            next_sum = Game._the_winnings_for_the_correct_answer[self._current_question]
            bold(f"\n{self._username}, Ваш {number} вопрос  на сумму ${next_sum}:")

        print(self._get_current_question())

    def _get_user_choice(self, choose_hint=False):
        """
        Получить выбор пользователя
        :param choose_hint: выбрать подсказку (True) или выбрать ответ (False)
        :return:
        """

        correct_choices = self._print_hint_choices() if choose_hint else self._print_answer_choices()
        choice = colored_input(f"\n{self._username}, выберите правильный ответ:")

        if choice in correct_choices:
            return choice

        red("Вы ответели неверно. Вожможно Вам повезет в следующий раз.\n")
        return self._get_user_choice(choose_hint)

    def _print_answer_choices(self):
        """
        Распечатать параметры ввода, после того, как будет задан вопрос
        :return: выбор ответа на вопрос
        """

        correct_input = []
        answer = self._get_current_question().current_answer_options()

        for i, a in enumerate(answer):
            if a != '':
                correct_input.append(str(i + 1))

        negative(f"({'/'.join(correct_input)} - для ответа, ", end='')

        if len(self._get_not_used_hints()) > 0:
            correct_input.extend(["П", "п"])
            negative("П - Получить подсказку, ", end='')

        correct_input.extend(["З", "з"])
        negative(f"З - Забрать деньги и закончить игру)")

        return correct_input

    def _print_hint_choices(self):
        """
        Параметры ввода для печати после выбора "Получить подсказку"
        :return: правильные параметры
        """

        not_used_hints = self._get_not_used_hints()
        blue(f"\n{self._username}, вы можете воспользоваться {len(not_used_hints)} подсказками: ")

        for i, hint in enumerate(not_used_hints):
            bold(f"{i + 1}: {hint.hint_name():20}",end='')
        bold(f"Н: Назад")

        correct_input = [str(i) for i in range(1, len(not_used_hints) + 1)]
        correct_input.extend(['н', 'Н'])

        return correct_input

    def _get_not_used_hints(self):
        """
        Получить неиспользованные подсказки
        :return: список неиспользованных подсказок
        """

        return list(filter(lambda i: not i.hint_used(), self._hints))

    def _execute_users_choice(self, choice):
        """
        Выполнить выбор пользователя
        :param choice: выбор пользователя
        :return: None
        """

        if choice in ['1', '2', '3', '4']:
            self._check_answer(int(choice))
        elif choice in ['п', 'П']:
            self._use_hint()
        elif choice in ['з', 'З']:
            if self._current_question > 0:
                self._current_won_sum = Game._the_winnings_for_the_correct_answer[self._current_question - 1]
            self._finish()

    def _check_answer(self, answer_number):
        """
        Проверить правильность ответа пользователя
        :param answer_number: выбор пользователя (номер ответа)
        :return: None
        """

        if self._get_current_question().check_the_answer(answer_number):
            magenda("\nЭто правильный ответ!\n")
            Game.wait_for_enter()
            prize = Game._the_winnings_for_the_correct_answer[self._current_question]
            if prize in Game._guaranteed_sum:
                self._current_won_sum = prize
            self._to_next_question()
        else:
            red("\nЭто неправильный ответ!\n")
            bold(f"Правильный ответ: '{self._get_current_question().get_correct_the_answer()}'\n")
            self._finish()

    def _use_hint(self):
        """
        Использовать подсказку
        :return: None
        """

        choice = self._get_user_choice(choose_hint=True)
        if choice in ['н', 'Н']:
            self._to_current_question()
        else:
            not_used_hints = self._get_not_used_hints()
            hint = self._get_current_question().get_hint(not_used_hints[int(choice) - 1])
            yellow(hint)
            self._to_current_question(show_question=False)

    def _finish(self):
        """
        Показать выйграш и закончить игру
        :return: None
        """
        print(f'\n{"="*50}')
        if self._current_won_sum == Game._guaranteed_sum[-1]:
            bold(f"{self._username}, Ваш выйграш составил $ 1.00.000. Поздравляем!!!")
        elif self._current_won_sum != 0:
            bold(f"{self._username}, Ваш выйграш составил $ {self._current_won_sum}. Поздравляем!!!")
        else:
            bold(f"{self._username}, к сожалению Ваш выйграш составил $ 0. Попробуйте сыграть ещё раз")

    @staticmethod
    def wait_for_enter():
        """
        Ожидания ввода
        :return: None
        """
        colored_input("\nНажмите Enter, чтобы продолжить")

    @staticmethod
    def clear_scr():
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

    def start(self):
        """
        Запуск программы
        :return: None
        """
        blue(f"\n{self._username}, добро пожаловать в игру!\n")
        self._to_next_question()
