import math

"""
Convert a given input of increments of time (in ascending order)
and converts it to number of seconds.
Supports up to a year.
"""
def time_in_seconds(input: tuple | list) -> int:
    seconds = 0
    factor = (1, 60, 60, 24, 7, 52) # Supports up to a year

    while len(input) > 0:
        input = [math.prod(x) for x in zip(input, factor)]
        seconds += input[0]
        input = input[1:]

    return seconds

"""
Convert given seconds into a more readable format.
Supports up to 23 hrs 59 mins 59 secs.
"""
def time_in_str(total_seconds: int) -> str:
    assert total_seconds > 0
    
    result = ''
    remaining = total_seconds
    
    remaining, sec = divmod(remaining, 60)
    remaining, min = divmod(remaining, 60)
    remaining, hrs = divmod(remaining, 24)
    
    if hrs > 0:
        result += f'{hrs} ' + ('hrs' if hrs > 1 else 'hr') + ' '
    if min > 0:
        result += f'{min} ' + ('mins' if min > 1 else 'min') + ' '
    if sec > 0:
        result += f'{sec} ' + ('secs' if sec > 1 else 'sec') + ' '

    return result.strip()

"""
Checks that the time is formatted within bound,
e.g. seconds is max 59 seconds, cannot 60 seconds.
Supports up to 1week-1s (i.e. 6:23:59:59).
Throws exception if attempt to check longer than or equals a week.
"""
def check_time_bounds(input: tuple | list) -> bool:
    bounds = (59, 59, 23, 6)
    
    if len(input) > len(bounds):
        raise Exception("Checking does not support >= 1 week")
    
    for x, y in zip(input, bounds):
        if x > y:
            return False
    
    return True
