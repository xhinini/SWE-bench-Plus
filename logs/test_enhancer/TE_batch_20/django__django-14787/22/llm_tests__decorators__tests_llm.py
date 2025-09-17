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

import inspect
from django.test import SimpleTestCase
from django.utils.decorators import method_decorator
from functools import wraps

def make_func_decorator():
    """
    Create a simple function decorator that uses wraps and records
    inspect.unwrap(func) on the wrapper it returns.
    """

    def dec(func):

        @wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        inner._wrapped_original = inspect.unwrap(func)
        return inner
    return dec

def make_class_decorator():
    """
    Create a callable class decorator that behaves like the above.
    """

    class Dec:

        def __call__(self, func):

            @wraps(func)
            def inner(*args, **kwargs):
                return func(*args, **kwargs)
            inner._wrapped_original = inspect.unwrap(func)
            return inner
    return Dec()

from functools import wraps, update_wrapper
from django.utils.decorators import method_decorator
from functools import wraps, update_wrapper
from django.test import SimpleTestCase
from django.utils.decorators import method_decorator

class MethodDecoratorRegressionTests(SimpleTestCase):

    def test_descriptor_returning_function_object_preserves_name(self):
        seen = {}

        def record_name_decorator(func):

            @wraps(func)
            def inner(*args, **kwargs):
                seen['name'] = getattr(func, '__name__', None)
                return func(*args, **kwargs)
            return inner

        class function_wrapper:

            def __init__(self, wrapped):
                self.wrapped = wrapped
                self.__name__ = wrapped.__name__

            def __get__(self, instance, cls=None):

                def bound(*a, **kw):
                    return self.wrapped(instance, *a, **kw)
                return bound

        class C:

            @method_decorator(record_name_decorator)
            @function_wrapper
            def method(self):
                return 'ok'
        C().method()
        self.assertEqual(seen.get('name'), 'method')

from functools import wraps
from django.utils.decorators import method_decorator
from django.test import SimpleTestCase
from functools import wraps
from django.test import SimpleTestCase
from django.utils.decorators import method_decorator

class WrappedInspectionTests(SimpleTestCase):

    def test_wrapped_present_on_method_decorated_function(self):

        def inspector(func):

            @wraps(func)
            def wrapper(*args, **kwargs):
                wrapped = getattr(func, '__wrapped__', None)
                return getattr(wrapped, '__name__', None)
            return wrapper

        class Test:

            @method_decorator(inspector)
            def method(self):
                return 'ok'
        self.assertEqual(Test().method(), 'method')

    def test_wrapped_present_when_decorating_via_class_name_argument(self):

        def inspector(func):

            @wraps(func)
            def wrapper(*args, **kwargs):
                wrapped = getattr(func, '__wrapped__', None)
                return getattr(wrapped, '__name__', None)
            return wrapper

        @method_decorator(inspector, name='method')
        class Test:

            def method(self):
                return 'ok'
        self.assertEqual(Test().method(), 'method')

    def test_wrapped_present_for_descriptor_wrapped_method(self):

        def inspector(func):

            @wraps(func)
            def wrapper(*args, **kwargs):
                wrapped = getattr(func, '__wrapped__', None)
                return getattr(wrapped, '__name__', None)
            return wrapper

        class bound_wrapper:

            def __init__(self, wrapped):
                self.wrapped = wrapped
                self.__name__ = wrapped.__name__

            def __call__(self, arg):
                return self.wrapped(arg)

            def __get__(self, instance, cls=None):
                return bound_wrapper(self.wrapped.__get__(instance, cls))

        class descriptor_wrapper:

            def __init__(self, wrapped):
                self.wrapped = wrapped
                self.__name__ = wrapped.__name__

            def __get__(self, instance, cls=None):
                return bound_wrapper(self.wrapped.__get__(instance, cls))
        method_dec = method_decorator(inspector)

        class Test:

            @method_dec
            @descriptor_wrapper
            def method(self, arg):
                return arg
        self.assertEqual(Test().method(1), 'method')

    def test_wrapped_present_for_call_method(self):

        def inspector(func):

            @wraps(func)
            def wrapper(*args, **kwargs):
                wrapped = getattr(func, '__wrapped__', None)
                return getattr(wrapped, '__name__', None)
            return wrapper

        class Test:

            @method_decorator(inspector)
            def __call__(self):
                return 'ok'
        t = Test()
        self.assertEqual(t(), '__call__')

    def test_wrapped_preserved_with_method_and_class_decorators(self):

        def inspector(func):

            @wraps(func)
            def wrapper(*args, **kwargs):
                wrapped = getattr(func, '__wrapped__', None)
                return getattr(wrapped, '__name__', None)
            return wrapper

        @method_decorator(inspector, name='method')
        class Test:

            @method_decorator(inspector)
            def method(self):
                return 'ok'
        self.assertEqual(Test().method(), 'method')

from functools import wraps
from django.utils.decorators import method_decorator
from functools import wraps
from django.test import SimpleTestCase
from django.utils.decorators import method_decorator

class MethodDecoratorRegressionTests(SimpleTestCase):

    def test_preserve_name_and_wrapped_on_method(self):
        captured = {}

        def inspector(func):

            def inner(*args, **kwargs):
                captured['name'] = getattr(func, '__name__', None)
                captured['has_wrapped'] = hasattr(func, '__wrapped__')
                return func(*args, **kwargs)
            return wraps(func)(inner)

        class Test:

            @method_decorator(inspector)
            def method(self):
                return 'ok'
        Test().method()
        self.assertEqual(captured['name'], 'method')
        self.assertTrue(captured['has_wrapped'])

    def test_decorating_dunder_call_preserves_name(self):
        captured = {}

        def inspector(func):

            def inner(*args, **kwargs):
                captured['name'] = getattr(func, '__name__', None)
                captured['has_wrapped'] = hasattr(func, '__wrapped__')
                return func(*args, **kwargs)
            return wraps(func)(inner)

        class Callable:

            @method_decorator(inspector)
            def __call__(self):
                return 'hello'
        Callable()()
        self.assertEqual(captured['name'], '__call__')
        self.assertTrue(captured['has_wrapped'])

    def test_iterable_of_decorators_preserves_name_and_wrapped(self):
        captured = {}

        def inspector_a(func):

            def inner(*args, **kwargs):
                captured.setdefault('a', {})['name'] = getattr(func, '__name__', None)
                captured['a']['wrapped'] = hasattr(func, '__wrapped__')
                return func(*args, **kwargs)
            return wraps(func)(inner)

        def inspector_b(func):

            def inner(*args, **kwargs):
                captured.setdefault('b', {})['name'] = getattr(func, '__name__', None)
                captured['b']['wrapped'] = hasattr(func, '__wrapped__')
                return func(*args, **kwargs)
            return wraps(func)(inner)
        decorators = (inspector_a, inspector_b)

        class Test:

            @method_decorator(decorators)
            def method(self):
                return 'ok'
        Test().method()
        self.assertEqual(captured['a']['name'], 'method')
        self.assertTrue(captured['a']['wrapped'])
        self.assertEqual(captured['b']['name'], 'method')
        self.assertTrue(captured['b']['wrapped'])

    def test_descriptor_wrapper_preserves_name(self):
        captured = {}

        def simple_dec(func):

            def wrapper(arg):
                return func('test:' + arg)
            return wraps(func)(wrapper)

        class descriptor_wrapper:

            def __init__(self, wrapped):
                self.wrapped = wrapped
                self.__name__ = wrapped.__name__

            def __get__(self, instance, cls=None):

                def bound(arg):
                    return self.wrapped.__get__(instance, cls)(arg)
                return bound
        method_dec = method_decorator(simple_dec)

        class Test:

            @method_dec
            @descriptor_wrapper
            def method(self, arg):
                return arg
        self.assertEqual(Test().method('hello'), 'test:hello')
        seen = {}

        def inspector(func):

            def inner(*a, **k):
                seen['name'] = getattr(func, '__name__', None)
                seen['has_wrapped'] = hasattr(func, '__wrapped__')
                return func(*a, **k)
            return wraps(func)(inner)

        class Test2:

            @method_decorator(inspector)
            @descriptor_wrapper
            def method(self, arg):
                return arg
        Test2().method('x')
        self.assertEqual(seen['name'], 'method')
        self.assertTrue(seen['has_wrapped'])

    def test_class_decoration_preserves_name_and_wrapped(self):
        captured = {}

        def inspector(func):

            def inner(*args, **kwargs):
                captured['name'] = getattr(func, '__name__', None)
                captured['has_wrapped'] = hasattr(func, '__wrapped__')
                return func(*args, **kwargs)
            return wraps(func)(inner)

        @method_decorator(inspector, name='method')
        class Test:

            def method(self):
                return 'ok'
        Test().method()
        self.assertEqual(captured['name'], 'method')
        self.assertTrue(captured['has_wrapped'])