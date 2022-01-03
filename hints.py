"""
Модуль подсказок

Подсказки:
1) 50/50
2) Звонок другу
3) помощь зала
"""

import os
import random
import abc

PROJECT_PATH = os.path.dirname(__file__)

class Hint(abc.ABC):
    """
    Абстрактный базовый класс
    """

    def __init__(self):
        self._hint_used = False
        self._hint_name = None

    def hint_used(self):
        """
        Проверка на использование подсказки
        :return: возвращает была ли подсказка использована или нет
        """

        return self._hint_used

    def hint_name(self):
        """
        Имя подсказки
        :return: возвращает имя подсказки
        """

        return self._hint_name

    @abc.abstractmethod
    def get_hint(self, answers, correct_answer_number):
        """
        Абстрактный метод
        :param answers: список из четырех ответов
        :param correct_answer_number: номер правильного ответа в списке
        :return: кортеж ответов
        """

        pass

class Fifty_Fifty(Hint):
    """
    Подсказка 50/50
    """

    def __init__(self):
        super().__init__()
        self._hint_name = "50/50"

    def get_hint(self, answers, correct_answer_number):
        """
        Применить подсказку 50/50
        :param answers: список из четырех ответов
        :param correct_answer_number: номер правильного ответа в списке
        :return: вариант из двух ответов
        """

        self._hint_used = True

        possible_answer_number = list(range(0, 4))
        possible_answer_number.remove(correct_answer_number)
        hint_answer_number = [correct_answer_number, random.choice(possible_answer_number)]
        hint_answer = map(lambda  i: answers[i] if i in hint_answer_number else '', range(0, 4))

        return list(hint_answer), None

class Call_a_friend(Hint):
    """
    Подсказка звонок другу
    """
    _file_name = "friend_phrases.txt"
    _file_path = os.path.join(PROJECT_PATH, _file_name)

    def __init__(self):
        super().__init__()
        self._hint_name = "Звонок другу"
        self.loading_a_hint()

    def loading_a_hint(self):
        """
        Загрузка подсказки из файла
        :return: None
        """

        with open(Call_a_friend._file_path, 'r') as f:
            self._phrases = f.readlines()

    def get_hint(self, answer, correct_answer_number):
        """
        Применить подсказку звонок другу
        :param answer: список из четырех ответов
        :param correct_answer_number: предпологаемый правильный ответ
        :return:None, фраза подсказки
        """

        self._hint_used = True
        hint_answer = random.choice(list(filter(lambda i: i != '', answer)))
        phrase = random.choice(self._phrases)
        return None, phrase.format(hint_answer)

class Hall_help(Hint):
    """
    Подсказка помощь зала
    """

    def __init__(self):
        super().__init__()
        self._hint_name = "Помощь зала"

    def get_hint(self, answers, correct_answer_number):
        """
        Применить подсказку помощь зала
        :param answers: список из четырех ответов
        :param correct_answer_number: предпологаемый правильный ответ
        :return: None, фраза подсказки
        """

        self._hint_used = True

        maximum_number_of_votes_in_percentage = 100
        votes = [0] * 4
        votes[correct_answer_number] = random.randint(50, 100)
        maximum_number_of_votes_in_percentage -= votes[correct_answer_number]

        for i, a in enumerate(answers):
            if a == '' or i == correct_answer_number:
                continue
            if i == len(answers) - 1 or '' in answers:
                votes[i] = maximum_number_of_votes_in_percentage
                break
            else:
                votes[i] = random.randint(0, maximum_number_of_votes_in_percentage)
                maximum_number_of_votes_in_percentage -= votes[i]

        return None, self._generate_a_phrase(answers, votes)

    def _generate_a_phrase(self, answers, votes):
        """
        Сгенерировать фразу подсказку
        :param answers: список из четырех ответов
        :param votes: список голосов аудитории
        :return: фраза подсказки
        """

        phrase = ""

        for i in [0, 1, 2, 3]:
            tmp = f"{i + 1}: "
            if answers[i] != '':
                tmp += f"{answers[i]} - {votes[i]}%"
            phrase += f"{tmp:20}"

            if i in [2, 3]:
                phrase += "\n"

        return phrase