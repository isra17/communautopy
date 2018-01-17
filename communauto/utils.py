import re

def camel_to_snake(camel):
    snake = camel[:1].lower()
    for c in camel[1:]:
        snake += '_' + c.lower() if c.isupper() else c
    return snake
