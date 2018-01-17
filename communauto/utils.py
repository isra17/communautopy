import datetime
import math
import re


def camel_to_snake(camel):
    snake = camel[:1].lower()
    last_upper = snake.isupper()
    for c in camel[1:]:
        if c.isupper() and not last_upper:
            snake += '_'
        snake += c.lower()
        last_upper = c.isupper()
    return snake

def parse_date(date):
    ts = int(date[date.index('(')+1:date.rindex(')')])
    return datetime.datetime.fromtimestamp(ts/1000)
