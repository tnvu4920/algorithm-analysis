import random
import string


LETTERS = string.ascii_lowercase


class RandomString(str):
    def __new__(cls, n):
        str_value = ''.join(random.choice(LETTERS) for _ in range(n))
        obj = str.__new__(cls, str_value)
        return obj
