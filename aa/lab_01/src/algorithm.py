from lab_01.src.config import ITER, MAX_TIME, TO_SEC
from functools import lru_cache
import numpy as np
from pprint import pprint
from time import process_time_ns
import tracemalloc


class AlgorithmError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        result = 'Incorrect name of algorithm, you should used ' \
                 '\'levenshtein_matrix\', \'damerau_levenshtein\', ' \
                 '\'levenshtein_recursively\', \'levenshtein_recursively_cache\''
        if self.message:
            result += f'. {self.message}'

        return result


class Algorithm:
    def __init__(self, name):
        self.name = name
        self.algorithms_keys = {
            'levenshtein_matrix': levenshtein_matrix,
            'damerau_levenshtein': damerau_levenshtein,
            'levenshtein_recursively': levenshtein_recursively,
            'levenshtein_recursively_cache': levenshtein_recursively_cache
        }

    def execute(self, str_1, str_2):
        if self.name in self.algorithms_keys:
            return self.algorithms_keys[self.name](str_1, str_2)
        else:
            raise AlgorithmError

    def get_time(self, str_1, str_2):
        if self.name in self.algorithms_keys:
            total = 0
            last = ITER
            for i in range(ITER):
                if total > MAX_TIME:
                    last = i
                    break

                start = process_time_ns()
                self.algorithms_keys[self.name](str_1, str_2)
                total += process_time_ns() - start

            return total / last / TO_SEC
        else:
            raise AlgorithmError

    def get_memory(self, str_1, str_2):
        if self.name in self.algorithms_keys:
            for _ in range(ITER // 100):
                tracemalloc.clear_traces()
                tracemalloc.start()
                self.algorithms_keys[self.name](str_1, str_2)
            return tracemalloc.get_traced_memory()[1]
        else:
            raise AlgorithmError


def levenshtein_matrix(str_1, str_2):
    len_1, len_2 = len(str_1), len(str_2)
    matrix = [[], [i for i in range(len_1 + 1)]]

    for i in range(1, len_2 + 1):
        matrix[0], matrix[1] = matrix[1], [i]

        for j in range(1, len_1 + 1):
            replace_letter = 0 if str_2[i - 1] == str_1[j - 1] else 1
            matrix[1].append(
                min(
                    matrix[1][j - 1] + 1,
                    matrix[0][j] + 1,
                    matrix[0][j - 1] + replace_letter
                )
            )

    return matrix[1][len_1]


def damerau_levenshtein(str_1, str_2):
    def d(i, j):
        if i == 0 and j == 0:
            return 0
        elif j == 0:
            return i
        elif i == 0:
            return j
        else:
            replace_letter = 0 if str_1[i - 1] == str_2[j - 1] else 1
            if i > 1 and j > 1 and str_1[i - 1] == str_2[j - 2] and str_1[i - 2] == str_2[j - 1]:
                exchange = d(i - 2, j - 2) + 1
            else:
                exchange = float('inf')

            return min(
                d(i, j - 1) + 1,
                d(i - 1, j) + 1,
                d(i - 1, j - 1) + replace_letter,
                exchange
            )

    distance = d(len(str_1), len(str_2))
    return distance


def levenshtein_recursively(str_1, str_2):
    def d(i, j):
        if i == 0 and j == 0:
            return 0
        elif j == 0:
            return i
        elif i == 0:
            return j
        else:
            replace_letter = 0 if str_1[i - 1] == str_2[j - 1] else 1
            return min(
                d(i, j - 1) + 1,
                d(i - 1, j) + 1,
                d(i - 1, j - 1) + replace_letter
            )

    distance = d(len(str_1), len(str_2))
    return distance


def levenshtein_recursively_cache(str_1, str_2):
    @lru_cache(maxsize=len(str_1) * len(str_2))
    def d(i, j):
        if i == 0 and j == 0:
            return 0
        elif j == 0:
            return i
        elif i == 0:
            return j
        else:
            replace_letter = 0 if str_1[i - 1] == str_2[j - 1] else 1
            return min(
                d(i, j - 1) + 1,
                d(i - 1, j) + 1,
                d(i - 1, j - 1) + replace_letter
            )

    distance = d(len(str_1), len(str_2))
    return distance
