import math

def time_in_seconds(input :tuple|list) -> int:
    seconds = 0
    factor = (1, 60, 60, 24, 7, 52) # Supports up to a year

    while len(input) > 0:
        input = [math.prod(x) for x in zip(input, factor)]
        seconds += input[0]
        input = input[1:]

    return seconds
