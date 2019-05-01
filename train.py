# -*- coding: UTF-8 -*-
# -*- coding: cp1251 -*-
import re
import sys
import os
import argparse
import os.path
import pickle
import collections


def create_parser():
    """
    создаём парсер с командами
    :return: возвращаем парсер
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, required = True, help='path to directory')
    parser.add_argument('--model', type=str, required = True, help='path to the model')
    parser.add_argument('--lc', action='store_const', const=True, help='lowercase texts')
    return parser


def update_mass(line, dict_of_dicts, lowercase):
    """
    функция принимает строку и изменяет массивы
    :param line: строка
    :param list_of_dict: массив каунтеров
    :param words: все слова
    :param lowercase: надо ли переводить все буквы в нижний регистр
    """
    if (lowercase == True):  # нужно ли переводить строку в нижний регистр
        line = line.lower()
    reg = re.compile('[^a-zA-Zа-яА-Я ]')
    line = reg.sub('', line)  # выкидываем ненужные символы
    words_in_line = line.split()  # разбиваем строку на слова
    for i in range((len(words_in_line) - 1)):  # проходим по всем словам строки кроме последнего
        word = words_in_line[i]  # берём конкретное слово
        if dict_of_dicts.get(word) == None:
            counter = {}
            counter[words_in_line[i + 1]] = 1
            dict_of_dicts[word] = counter
        else:
            dict_of_dicts[word][words_in_line[i + 1]] = dict_of_dicts[word].get(words_in_line[i + 1], 0) + 1


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[
                                  1:])  # в namespace закидываем весь ввод из консоли кроме имени файла, поэтому начинаем со второго эелемента
    lowercase = namespace.lc  # isLowercase true or not
    dict_of_dicts = {}
    if (namespace.input_dir == None):  # если путь к папке не ввели
        line = sys.stdin.readline()  # то считываем текст из консоли  # давай назовем ее line
        update_mass(line, dict_of_dicts, lowercase)
    else:
        directory = namespace.input_dir  # путь к папке в которой лежат файлы
        files = os.listdir(directory)  # массив со всеми этими файлами
        for file in files:
            address = os.path.join(namespace.input_dir, file)
            with open(address, 'r') as opened_file:
                for line in opened_file:
                    update_mass(line, dict_of_dicts, lowercase)
    with open(namespace.model, "wb") as opened_file:
pickle.dump(dict_of_dicts, opened_file)
