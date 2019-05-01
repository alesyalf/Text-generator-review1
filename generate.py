# -*- coding: UTF-8 -*-
import sys
import argparse
import random
import re
import pickle
import collections


def createParser():
    """
    создаём парсер с командами
    :return: возвращаем парсер
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, required=True, help='path to the model ')
    parser.add_argument('--seed', nargs='?', type=str, help='initial word')
    parser.add_argument('--length', type=int, required=True, help='length of the sequence')
    parser.add_argument('--output', nargs='?', required=True, type=str, help='output file')
    return parser


def result(dict_of_dict, cur, res):
    choices = []
    keys = list(dict_of_dicts.keys())
    for i in dict_of_dicts[cur].keys():
        for j in range(dict_of_dicts[cur][i]):
            choices.append(i)
    if (len(choices) > 0):
        random_word = random.choice(choices)
    else:
        random_word = random.choice(keys)
    res.append(random_word)
    if dict_of_dicts.get(random_word) is None:
        random_word = random.choice(keys)
    return random_word


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    with open(namespace.model, "rb") as inputfile:
        dict_of_dicts = pickle.load(inputfile)
    words = list(dict_of_dicts.keys())
    if namespace.seed is None:  # если не ввели seed, то берём любое слово первым
        random_word = random.choice(words)
    else:
        random_word = namespace.seed  # иначе берём первое слово
    res = []
    cur = random_word
    res.append(random_word)  # результат
    for i in range(namespace.length):
        cur = result(dict_of_dicts, cur, res)

    if namespace.output is None:
        for i in res:
            sys.stdout.write(i + ' ')
    else:
        with open(namespace.output, 'w') as opened_file:
            for i in res:
                opened_file.write(i + ' ')

