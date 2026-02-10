import random


def random_number(number_of_digits: int) -> str:
    if number_of_digits <= 0:
        return ""
    max_value = int("9" * number_of_digits)
    value = random.randint(0, max_value)
    return str(value).zfill(number_of_digits)


def random_number_int(minimum: int, maximum: int) -> int:
    return random.randint(minimum, maximum)
