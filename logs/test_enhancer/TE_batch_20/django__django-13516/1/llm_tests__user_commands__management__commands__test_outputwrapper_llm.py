import io
import sys
import types
import pytest
import io
import sys
import types
import pytest
from django.core.management.base import OutputWrapper, BaseCommand, CommandError

def test_flush_calls_underlying_flush():
    ds = DummyStream()
    ow = OutputWrapper(ds)
    ow.flush()
    assert ds._flushed is True

def test_flush_does_not_raise_if_underlying_has_no_flush():

    class NoFlushStream:

        def __init__(self):
            self.written = []

        def write(self, s):
            self.written.append(s)
    s = NoFlushStream()
    ow = OutputWrapper(s)
    ow.flush()

def test_write_appends_ending_when_missing():
    s = io.StringIO()
    ow = OutputWrapper(s)
    ow.write('hello')
    assert s.getvalue().endswith('\n')
    assert s.getvalue() == 'hello\n'

def test_write_preserves_message_if_endswith_ending():
    s = io.StringIO()
    ow = OutputWrapper(s)
    ow.write('line-with-newline\n')
    assert s.getvalue() == 'line-with-newline\n'

def test_write_uses_style_func_property_if_no_arg_passed():
    s = io.StringIO()
    ow = OutputWrapper(s)
    ow.style_func = lambda m: '[STYLED]' + m
    ow.write('a')
    assert s.getvalue() == '[STYLED]a\n'

def test_write_uses_style_func_argument_to_override_property():
    s = io.StringIO()
    ow = OutputWrapper(s)
    ow.style_func = lambda m: '[BAD]' + m
    ow.write('x', style_func=lambda m: '[GOOD]' + m)
    assert s.getvalue() == '[GOOD]x\n'

def test_style_func_setter_respects_isatty():

    class TtyStream:

        def isatty(self):
            return True

        def write(self, s):
            pass
    ts = TtyStream()
    ow = OutputWrapper(ts)
    called = {}

    def sty(m):
        called['ok'] = True
        return m
    ow.style_func = sty
    assert callable(ow.style_func)
    ow.style_func('x')
    assert called.get('ok') is True

def test_isatty_reflects_underlying_isatty():
    s1 = DummyStream(isatty=True)
    s2 = DummyStream(isatty=False)
    ow1 = OutputWrapper(s1)
    ow2 = OutputWrapper(s2)
    assert ow1.isatty() is True
    assert ow2.isatty() is False

def test_basecommand_execute_uses_provided_stdout_and_stderr_wrappers():

    class MyCmd(BaseCommand):

        def handle(self, *args, **options):
            return 'RESULT'
    out = io.StringIO()
    err = io.StringIO()
    cmd = MyCmd()
    result = cmd.execute(stdout=out, stderr=err, skip_checks=True, force_color=False, no_color=False)
    assert result == 'RESULT'
    assert out.getvalue().strip() == 'RESULT'

def test_basecommand_execute_with_no_color_disables_stderr_style_func():

    class MyCmd(BaseCommand):

        def handle(self, *args, **options):
            self.stderr.write('ERRMSG')
            return ''
    out = io.StringIO()
    err = io.StringIO()
    cmd = MyCmd()
    cmd.execute(stdout=out, stderr=err, skip_checks=True, force_color=False, no_color=True)
    assert err.getvalue().strip() == 'ERRMSG'