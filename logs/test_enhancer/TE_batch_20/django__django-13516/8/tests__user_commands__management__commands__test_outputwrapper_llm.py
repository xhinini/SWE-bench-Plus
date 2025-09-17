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

import pytest
from django.core.management.base import OutputWrapper

def test_flush_calls_underlying_flush():
    out = DummyOutWithFlush()
    wrapper = OutputWrapper(out)
    assert not out.flushed
    wrapper.flush()
    assert out.flushed is True

def test_flush_is_noop_if_underlying_has_no_flush():
    out = DummyOutNoFlush()
    wrapper = OutputWrapper(out)
    wrapper.flush()
    assert out.written == ''

def test_write_appends_default_ending_once():
    out = DummyOutWithFlush()
    wrapper = OutputWrapper(out)
    wrapper.write('hello')
    assert out.written == 'hello\n'
    out.written = ''
    wrapper.write('world\n')
    assert out.written == 'world\n'

def test_write_respects_custom_ending_and_no_duplicate():
    out = DummyOutWithFlush()
    wrapper = OutputWrapper(out, ending='')
    wrapper.write('no-newline')
    assert out.written == 'no-newline'
    out.written = ''
    wrapper2 = OutputWrapper(out, ending='--')
    wrapper2.write('x')
    assert out.written == 'x--'
    out.written = ''
    wrapper2.write('y--')
    assert out.written == 'y--'

def test_write_uses_given_style_func_argument_over_default():
    out = DummyOutWithFlush()
    wrapper = OutputWrapper(out)
    style = lambda s: s.upper()
    wrapper.write('abc', style_func=style)
    assert out.written == 'ABC\n'

def test_style_func_setter_and_getter_when_tty_true():

    class TtyOut(DummyOutWithFlush):

        def isatty(self):
            return True
    out = TtyOut()
    wrapper = OutputWrapper(out)
    f = lambda s: '<styled>' + s
    wrapper.style_func = f
    assert wrapper.style_func is not None
    assert wrapper.style_func('x') == '<styled>x'

def test_style_func_setter_sets_identity_when_not_tty_or_none():
    out = DummyOutNoFlush()
    wrapper = OutputWrapper(out)
    wrapper.style_func = lambda s: 'SHOULD_NOT_USE'
    assert wrapper.style_func('input') == 'input'
    wrapper.style_func = None
    assert wrapper.style_func('input2') == 'input2'

def test_isatty_delegates_to_underlying_stream():
    out = DummyOutWithFlush()
    wrapper = OutputWrapper(out)
    assert wrapper.isatty() is True
    out2 = DummyOutNoFlush()
    wrapper2 = OutputWrapper(out2)
    assert wrapper2.isatty() is False

def test___getattr___delegates_other_attributes_to_underlying():
    out = DummyOutWithFlush()
    wrapper = OutputWrapper(out)
    assert wrapper.custom == 'custom-attr'

def test_write_preserves_style_func_property_when_no_style_arg_passed():

    class TtyOut(DummyOutWithFlush):

        def isatty(self):
            return True
    out = TtyOut()
    wrapper = OutputWrapper(out)
    wrapper.style_func = lambda s: 'X:' + s
    wrapper.write('payload')
    assert out.written == 'X:payload\n'

pass
import io
import types
import pytest
from django.core.management.base import OutputWrapper, BaseCommand, CommandError

def test_flush_calls_underlying_flush():
    dummy = DummyStream()
    wrapper = OutputWrapper(dummy)
    wrapper.flush()
    assert dummy.flushed == 1

def test_flush_no_attribute_no_error():

    class NoFlushStream:

        def __init__(self):
            self.written = []

        def write(self, s):
            self.written.append(s)

        def isatty(self):
            return False
    s = NoFlushStream()
    wrapper = OutputWrapper(s)
    wrapper.flush()
    assert s.written == []

def test_style_func_set_only_if_isatty_true():
    dummy = DummyStream(isatty_value=True)
    wrapper = OutputWrapper(dummy)
    wrapper.style_func = lambda s: s.upper()
    wrapper.write('hello')
    assert dummy.written == ['HELLO\n']

def test_style_func_not_set_if_not_isatty():
    dummy = DummyStream(isatty_value=False)
    wrapper = OutputWrapper(dummy)
    wrapper.style_func = lambda s: s.upper()
    wrapper.write('world')
    assert dummy.written == ['world\n']

def test_write_appends_ending_but_not_duplicate():
    dummy = DummyStream()
    wrapper = OutputWrapper(dummy, ending='\n')
    wrapper.write('line\n')
    assert dummy.written == ['line\n']
    wrapper.write('another')
    assert dummy.written[-1] == 'another\n'

def test_write_style_func_parameter_overrides_property():
    dummy = DummyStream(isatty_value=False)
    wrapper = OutputWrapper(dummy)
    wrapper.write('x', style_func=lambda s: s + 'X')
    assert dummy.written == ['xX\n']

def test___getattr___delegates_arbitrary_methods():
    dummy = DummyStream()
    wrapper = OutputWrapper(dummy)
    wrapper.marker('OK')
    assert 'MARKER:OK' in dummy.written[0]

def test_execute_writes_output_to_provided_stdout_and_returns_output():

    class MyCommand(BaseCommand):

        def handle(self, *args, **options):
            return 'RESULT'
    dummy_out = DummyStream()
    dummy_err = DummyStream()
    cmd = MyCommand(stdout=io.StringIO(), stderr=io.StringIO())
    result = cmd.execute(force_color=False, no_color=False, stdout=dummy_out, stderr=dummy_err, skip_checks=True)
    assert result == 'RESULT'
    assert dummy_out.written == ['RESULT\n']

def test_execute_raises_when_both_no_color_and_force_color_are_true():

    class MyCommand(BaseCommand):

        def handle(self, *args, **options):
            return ''
    cmd = MyCommand(stdout=io.StringIO(), stderr=io.StringIO())
    with pytest.raises(CommandError) as excinfo:
        cmd.execute(force_color=True, no_color=True, stdout=None, stderr=None, skip_checks=True)
    assert "The --no-color and --force-color options can't be used together." in str(excinfo.value)

def test_execute_no_color_sets_stderr_style_func_to_none_when_no_external_stderr():

    class MyCommand(BaseCommand):

        def handle(self, *args, **options):
            return ''
    cmd = MyCommand(stdout=io.StringIO(), stderr=io.StringIO())
    cmd.execute(force_color=False, no_color=True, stdout=None, stderr=None, skip_checks=True)
    assert cmd.stderr.style_func is None

import io
import importlib
import pytest
import io
import importlib
import types
import pytest
base = importlib.import_module('django.core.management.base')
CommandError = base.CommandError
BaseCommand = base.BaseCommand
OutputWrapper = base.OutputWrapper
DEFAULT_DB_ALIAS = base.DEFAULT_DB_ALIAS

def test_write_appends_ending():
    out = io.StringIO()
    w = OutputWrapper(out)
    w.write('hello')
    assert out.getvalue() == 'hello\n'

def test_write_respects_explicit_ending():
    out = io.StringIO()
    w = OutputWrapper(out)
    w.write('no-newline', ending='')
    assert out.getvalue() == 'no-newline'
    w.write('already\n', ending='\n')
    assert out.getvalue().endswith('already\n')

def test_write_uses_passed_style_func():
    out = io.StringIO()
    w = OutputWrapper(out)
    w.write('abc', style_func=lambda s: s.upper())
    assert out.getvalue() == 'ABC\n'

def test_style_func_setter_honors_isatty(monkeypatch):

    class FakeOut:

        def __init__(self, isatty_value):
            self._isatty = isatty_value
            self.written = ''

        def isatty(self):
            return self._isatty

        def write(self, s):
            self.written += s
    f1 = FakeOut(True)
    w1 = OutputWrapper(f1)
    w1.style_func = lambda s: 'X' + s
    w1.write('a')
    assert f1.written == 'Xa\n'
    f2 = FakeOut(False)
    w2 = OutputWrapper(f2)
    w2.style_func = lambda s: 'X' + s
    w2.write('a')
    assert f2.written == 'a\n'

def test_flush_calls_underlying_flush():
    called = {'n': 0}

    class FakeOut:

        def write(self, s):
            pass

        def flush(self):
            called['n'] += 1
    f = FakeOut()
    w = OutputWrapper(f)
    w.flush()
    assert called['n'] == 1

def test_flush_no_error_when_no_flush():

    class FakeOutNoFlush:

        def write(self, s):
            pass
    f = FakeOutNoFlush()
    w = OutputWrapper(f)
    w.flush()

def test___getattr_forwards_methods():

    class FakeOut:

        def __init__(self):
            self.called_with = None

        def write(self, s):
            self.called_with = s

        def custom_method(self, x):
            return f'got-{x}'
    f = FakeOut()
    w = OutputWrapper(f)
    result = w.custom_method(123)
    assert result == 'got-123'
    w.write('hi')
    assert f.called_with.endswith('hi\n')

def test_style_func_set_to_none_disables_styling():

    class FakeOut:

        def __init__(self):
            self._data = ''

        def isatty(self):
            return True

        def write(self, s):
            self._data += s
    f = FakeOut()
    w = OutputWrapper(f)
    w.style_func = lambda s: '!' + s
    w.write('x')
    assert f._data.endswith('!x\n')
    w.style_func = None
    w.write('y')
    assert f._data.endswith('y\n')

def test_run_from_argv_handles_CommandError_without_traceback(monkeypatch):

    class BadCommand(BaseCommand):

        def execute(self, *args, **options):
            raise CommandError('boom', returncode=3)
    stdout = io.StringIO()
    stderr = io.StringIO()
    cmd = BadCommand(stdout=stdout, stderr=stderr)
    argv = ['manage.py', 'sub']
    with pytest.raises(SystemExit) as excinfo:
        cmd.run_from_argv(argv)
    assert excinfo.value.code == 3
    err = stderr.getvalue()
    assert 'CommandError' in err and 'boom' in err

def test_execute_wraps_output_in_transaction_when_requested(monkeypatch):

    class SQLCommand(BaseCommand):
        output_transaction = True

        def handle(self, *args, **options):
            return 'SELECT 1;'

    class FakeOps:

        def start_transaction_sql(self):
            return 'BEGIN;'

        def end_transaction_sql(self):
            return 'COMMIT;'

    class FakeConnection:

        def __init__(self):
            self.ops = FakeOps()
    fake_conn = FakeConnection()
    monkeypatch.setattr(base, 'connections', {DEFAULT_DB_ALIAS: fake_conn})

    class Style:

        def SQL_KEYWORD(self, s):
            return f'[{s}]'
    monkeypatch.setattr(base, 'color_style', lambda force_color=False: Style())
    monkeypatch.setattr(base, 'no_style', lambda: Style())
    stdout = io.StringIO()
    stderr = io.StringIO()
    cmd = SQLCommand(stdout=stdout, stderr=stderr)
    output = cmd.execute(skip_checks=True, stdout=stdout, stderr=stderr, force_color=False, no_color=False)
    expected = '[BEGIN;]\nSELECT 1;\n[COMMIT;]'
    assert output == expected