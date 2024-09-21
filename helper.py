import math

def time_in_seconds(input :tuple|list) -> int:
    seconds = 0
    factor = (1, 60, 60, 24, 7, 52) # Supports up to a year

    while len(input) > 0:
        input = [math.prod(x) for x in zip(input, factor)]
        seconds += input[0]
        input = input[1:]

    return seconds

"""
Supports up to 23:59:59
"""
def time_in_str(total_seconds :int) -> str:
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
