"""
Модуль вопросов.

Class Question для работы с отдельными вопросами
Class Questions для работы со списком вопросов
"""

import os
import random

PROJECT_PATH = os.path.dirname(__file__)
QUESTIONS_WITH_FOLDER = 'Questions'
DEMARCATE = f"{'-'*50}"

class Question:
    """
    Отдельные вопросы
    """

    def __init__(self, question, answer_1, answer_2, answer_3, answer_4, true_answer):
        self._question = question
        self._answer = [answer_1, answer_2, answer_3, answer_4]
        self._current_answer_list = self._answer
        self._true_answer = true_answer

    def __str__(self):
        return f"{DEMARCATE}\n{self._question}\n{DEMARCATE}\n{self.current_answer()}{DEMARCATE}"

    def check_the_answer(self, answer_number):
        """
        Проверяет правильность ответа
        :param answer_number: номер ответа
        :return: True/False
        """

        return self._true_answer == answer_number

    def get_correct_the_answer(self):
        """
        Получение правильного ответа
        :return: правильный ответ
        """

        return self._answer[self._true_answer - 1]

    def get_hint(self, hint):
        """
        Получить подсказку
        :param hint: объект подсказки
        :return: подсказка
        """

        answer, phrase = hint.get_hint(self._current_answer_list, self._true_answer - 1)

        if answer:
            self._current_answer_list = answer
            phrase =self.current_answer()

        return f"\n{DEMARCATE}\n{phrase}{DEMARCATE}"

    def current_answer_options(self):
        """
        Возвращает текущие варианты ответов
        :return: текущие вопросы
        """

        return self._current_answer_list

    def current_answer(self):
        """
        Форматированный вывод текущих ответов
        :return: форматированный вывод текущих ответов
        """

        return f"1: {self._current_answer_list[0]:15} 3: {self._current_answer_list[2]:15}\n" \
               f"2: {self._current_answer_list[1]:15} 4: {self._current_answer_list[3]:15}\n"

class Questions:
    """
    Список вопросов случайных вопросов
    """

    _folder = QUESTIONS_WITH_FOLDER
    _path = os.path.join(PROJECT_PATH, _folder)

    def __init__(self):
        self._questions = None
        self._the_list_of_questions()

    def _the_list_of_questions(self):
        """
        Загружает список случайных вопросы.
        :return: Список из случайных вопросов для каждого тура
        """

        files_with_questions = self._all_questions_options()
        self._questions = [None] * len(files_with_questions)

        for file in files_with_questions:
            self._question_for_a_specific_tour(file)

    def _all_questions_options(self):
        """
        Загрузка всех текстовых файлов из папки 'Questions'
        :return: Список путей к текстовым файлам в папке 'Questions'
        """

        list_of_files_in_a_folder = os.listdir(Questions._path)
        list_of_paths_to_files_in_the_folder = []

        for file in list_of_files_in_a_folder:
            path = os.path.join(Questions._path, file)
            if os.path.isfile(path) and os.path.splitext(path)[1] == '.txt':
                list_of_paths_to_files_in_the_folder.append(path)

        return list_of_paths_to_files_in_the_folder

    def _question_for_a_specific_tour(self, path):
        """
        Загрузка случайного вопроса из списка текстовых файлов
        :param path: путь к текстовому файлу с вопросами
        :return: None
        """

        with open(path, "r") as file:
            data = file.readlines()

        line = random.choice(data)
        q, a1, a2, a3, a4, ca = line[:-1].split("\t")
        ind = int(os.path.basename(path)[:-4])
        self._questions[ind-1] = Question(q, a1, a2, a3, a4, int(ca))

    def get_questions(self):
        """
        Получить список вопросов
        :return: список вопросов
        """

        return self._questions
