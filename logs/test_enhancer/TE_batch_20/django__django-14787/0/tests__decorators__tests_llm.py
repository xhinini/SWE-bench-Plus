from functools import wraps
from django.test import SimpleTestCase
from django.utils.decorators import method_decorator

def attr_setter_via_wrapped(func):
    """
    A decorator that, if the received callable has a __wrapped__ attribute,
    sets an attribute on the underlying wrapped function. Otherwise sets it
    on the callable itself. Uses wraps() to be a typical real-world decorator.
    """
    if hasattr(func, '__wrapped__'):
        func.__wrapped__.marker = 'underlying'
    else:
        func.marker = 'wrapper'

    @wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner