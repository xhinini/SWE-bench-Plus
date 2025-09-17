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

from django.test import SimpleTestCase
from django.utils.decorators import method_decorator
from functools import wraps

def capture_name(func):

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.decorated_name = getattr(func, '__name__', None)
    return wrapper

def capture_qualname(func):

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.decorated_qualname = getattr(func, '__qualname__', None)
    return wrapper

def uses_wraps(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

from django.utils.decorators import method_decorator
from django.test import SimpleTestCase
import inspect
from django.test import SimpleTestCase
from django.utils.decorators import method_decorator
import inspect

def make_check_decorator(marker):

    def decorator(func):
        has_wrapped = hasattr(func, '__wrapped__')
        wrapped_name = getattr(func, '__wrapped__', None).__name__ if has_wrapped else None

        def wrapper(*args, **kwargs):
            return (marker, has_wrapped, wrapped_name)
        return wrapper
    return decorator

import inspect
from functools import wraps
from django.test import SimpleTestCase
from django.utils.decorators import method_decorator
import inspect
from functools import wraps
from django.test import SimpleTestCase
from django.utils.decorators import method_decorator

def wraps_decorator(func):

    @wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner

def introspecting_decorator(func):

    @wraps(func)
    def inner(*args, **kwargs):
        wrapped = getattr(func, '__wrapped__', None)
        return (func.__name__, getattr(wrapped, '__name__', None))
    return inner

import inspect
from functools import wraps
from unittest import mock
from django.test import SimpleTestCase
from django.utils.decorators import method_decorator
import inspect
from functools import wraps
from unittest import mock
from django.test import SimpleTestCase
from django.utils.decorators import method_decorator

def simple_wraps_decorator(func):
    """
    A simple decorator that preserves the wrapped function's metadata via wraps.
    """

    @wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner

def capturing_decorator(storage):
    """
    A decorator that captures the __name__ of the function it receives when applied.
    """

    def deco(func):
        storage.append(getattr(func, '__name__', None))

        @wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner
    return deco

def attribute_setting_decorator(func):
    """
    A decorator that sets a custom attribute on the wrapper it returns.
    """

    @wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    inner.custom_marker = True
    return inner