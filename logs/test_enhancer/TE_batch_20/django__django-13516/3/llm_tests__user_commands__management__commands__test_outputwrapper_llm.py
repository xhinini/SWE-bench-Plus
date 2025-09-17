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

import io
import pytest
from django.core.management.base import OutputWrapper, BaseCommand, CommandError
from django.core.management.base import no_style, color_style
import io
import pytest
from django.core.management.base import OutputWrapper, BaseCommand, CommandError
from django.core.management.base import no_style, color_style

def test_flush_calls_underlying_flush():
    buf = DummyWithFlush()
    wrapper = OutputWrapper(buf)
    assert not buf.flushed
    wrapper.flush()
    assert buf.flushed is True

def test_flush_with_no_underlying_flush_does_not_error():
    buf = DummyNoFlush()
    wrapper = OutputWrapper(buf)
    wrapper.flush()

def test_write_appends_ending_once():
    sio = io.StringIO()
    wrapper = OutputWrapper(sio, ending='\n')
    wrapper.write('hello')
    assert sio.getvalue() == 'hello\n'
    wrapper.write('world\n')
    assert sio.getvalue().endswith('world\n')
    assert sio.getvalue().count('\n') == 2

def test_write_uses_explicit_style_func_argument_over_property():
    out = DummyIsattyTrue()
    wrapper = OutputWrapper(out, ending='')

    def upper_style(s):
        return s.upper()
    wrapper.style_func = upper_style

    def lower_style(s):
        return s.lower()
    wrapper.write('MiXeD', style_func=lower_style, ending='')
    assert out.written == 'mixed'
    wrapper.write('Aa', ending='')
    assert out.written.endswith('AA')

def test_style_func_setter_respects_isatty():
    out_true = DummyIsattyTrue()
    out_false = DummyIsattyFalse()
    wrapper_true = OutputWrapper(out_true, ending='')
    wrapper_false = OutputWrapper(out_false, ending='')

    def mark(s):
        return 'X' + s + 'X'
    wrapper_true.style_func = mark
    wrapper_false.style_func = mark
    wrapper_true.write('ok', ending='')
    assert out_true.written == 'XokX'
    wrapper_false.write('ok', ending='')
    assert out_false.written == 'ok'

def test___getattr___proxies_other_attributes():

    class Under:

        def __init__(self):
            self.foo = 123
    u = Under()
    w = OutputWrapper(u)
    assert w.foo == 123

def test_write_preserves_existing_ending_and_does_not_duplicate():
    sio = io.StringIO()
    wrapper = OutputWrapper(sio, ending='\n')
    wrapper.write('line\n')
    assert sio.getvalue() == 'line\n'

def test_basecommand_sets_stderr_style_when_color_enabled():
    out = DummyIsattyTrue()
    cmd = BaseCommand(stdout=io.StringIO(), stderr=out, no_color=False, force_color=False)
    wrapper = cmd.stderr
    wrapper.write('errormsg', ending='')
    assert out.written != 'errormsg'

def test_basecommand_init_conflicting_color_flags_raises():
    with pytest.raises(CommandError):
        BaseCommand(stdout=io.StringIO(), stderr=io.StringIO(), no_color=True, force_color=True)