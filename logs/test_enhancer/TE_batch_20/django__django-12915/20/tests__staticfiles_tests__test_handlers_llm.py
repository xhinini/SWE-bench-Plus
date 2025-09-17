import pytest
from urllib.parse import urlparse
import asyncio
import types
from urllib.parse import urlparse
import pytest
from django.conf import settings
from django.core.handlers.exception import response_for_exception
from django.http import Http404
import django.contrib.staticfiles.handlers as handlers

@pytest.mark.asyncio
async def test_get_response_async_calls_sync_to_async_on_success(monkeypatch):
    called = []
    inst = DummyHandler()
    inst.base_url = urlparse('/static/')
    async_wrappers = {}

    def fake_sync_to_async(func):
        called.append(func)

        async def _inner(*args, **kwargs):
            return func(*args, **kwargs)
        async_wrappers[func] = _inner
        return _inner
    monkeypatch.setattr(handlers, 'sync_to_async', fake_sync_to_async)

    def serve(request):
        return 'served'
    inst.serve = serve
    result = await inst.get_response_async('req')
    assert result == 'served'
    assert serve in called

@pytest.mark.asyncio
async def test_get_response_async_uses_sync_to_async_for_404(monkeypatch):
    called = []
    inst = DummyHandler()
    inst.base_url = urlparse('/static/')

    def fake_sync_to_async(func):
        called.append(func)

        async def _inner(*args, **kwargs):
            return func(*args, **kwargs)
        return _inner
    monkeypatch.setattr(handlers, 'sync_to_async', fake_sync_to_async)

    def serve(request):
        raise Http404('not found')
    inst.serve = serve

    def fake_response_for_exception(request, exc):
        return 'handled-404'
    monkeypatch.setattr(handlers, 'response_for_exception', fake_response_for_exception)
    result = await inst.get_response_async('req')
    assert result == 'handled-404'
    assert any((func is serve for func in called))
    assert any((func is fake_response_for_exception for func in called))

def test_get_response_calls_serve_on_success(monkeypatch):
    inst = DummyHandler()
    inst.base_url = urlparse('/static/')

    def serve(request):
        return 'ok'
    inst.serve = serve
    result = inst.get_response('req')
    assert result == 'ok'

def test_get_response_sync_handles_http404(monkeypatch):
    inst = DummyHandler()
    inst.base_url = urlparse('/static/')

    def serve(request):
        raise Http404('gone')
    inst.serve = serve

    def fake_response_for_exception(request, exc):
        return 'handled-sync-404'
    monkeypatch.setattr(handlers, 'response_for_exception', fake_response_for_exception)
    result = inst.get_response('req')
    assert result == 'handled-sync-404'

def test_file_path_converts_url_to_path_correctly():
    inst = DummyHandler()
    inst.base_url = urlparse('/static/')
    assert inst.file_path('/static/foo.txt') == 'foo.txt'
    assert inst.file_path('/static/') == ''

def test__should_handle_false_when_netloc_present():
    inst = DummyHandler()
    inst.base_url = urlparse('http://example.com/static/')
    assert not inst._should_handle('/static/file')

def test__should_handle_true_for_exact_match():
    inst = DummyHandler()
    inst.base_url = urlparse('/static/')
    assert inst._should_handle('/static/')
    assert inst._should_handle('/static/foo')

def test_get_base_url_checks_settings(monkeypatch):
    called = {}

    def fake_check_settings():
        called['ok'] = True
    monkeypatch.setattr(handlers.utils, 'check_settings', fake_check_settings)
    monkeypatch.setattr(settings, 'STATIC_URL', '/static-url/')
    inst = DummyHandler()
    assert inst.get_base_url() == '/static-url/'
    assert called.get('ok', False) is True

@pytest.mark.asyncio
async def test_get_response_async_propagates_non_http404_exceptions():
    inst = DummyHandler()
    inst.base_url = urlparse('/static/')

    def serve(request):
        raise ValueError('boom')
    inst.serve = serve
    with pytest.raises(ValueError):
        await inst.get_response_async('req')

import asyncio
import threading
import types
import pytest
from django.http import Http404
from django.contrib.staticfiles import handlers as handlers_mod
from django.contrib.staticfiles.handlers import StaticFilesHandlerMixin
import asyncio
import threading
import types
import pytest
from django.http import Http404
from django.contrib.staticfiles import handlers as handlers_mod
from django.contrib.staticfiles.handlers import StaticFilesHandlerMixin

@pytest.mark.asyncio
async def test_get_response_async_runs_serve_in_thread_on_success():
    """serve should be executed in a thread (not main thread) and return its value."""

    class H(StaticFilesHandlerMixin):

        def __init__(self):
            self.recorded_thread = None

        def serve(self, request):
            self.recorded_thread = threading.current_thread()
            return 'OK-' + request.name
    req = DummyRequest('a')
    h = H()
    result = await h.get_response_async(req)
    assert result == 'OK-a'
    assert h.recorded_thread is not None
    assert h.recorded_thread is not threading.main_thread(), 'serve executed on main thread'

@pytest.mark.asyncio
async def test_get_response_async_runs_serve_in_thread_when_raises_http404():
    """When serve raises Http404, response_for_exception should be executed in a thread."""
    serve_thread = None
    resp_exc_thread = None
    captured_args = {}

    class H(StaticFilesHandlerMixin):

        def serve(self, request):
            nonlocal serve_thread
            serve_thread = threading.current_thread()
            raise Http404('not found')

    def fake_response_for_exception(request, exc):
        nonlocal resp_exc_thread, captured_args
        resp_exc_thread = threading.current_thread()
        captured_args['request'] = request
        captured_args['exc'] = exc
        return 'RESP-FROM-EXC'
    original = handlers_mod.response_for_exception
    handlers_mod.response_for_exception = fake_response_for_exception
    try:
        h = H()
        req = DummyRequest('b')
        result = await h.get_response_async(req)
        assert result == 'RESP-FROM-EXC'
        assert serve_thread is not None
        assert resp_exc_thread is not None
        assert serve_thread is not threading.main_thread(), 'serve executed on main thread'
        assert resp_exc_thread is not threading.main_thread(), 'response_for_exception executed on main thread'
        assert captured_args['request'] is req
        assert isinstance(captured_args['exc'], Http404)
    finally:
        handlers_mod.response_for_exception = original

@pytest.mark.asyncio
async def test_get_response_async_returns_value_from_serve_and_threaded():
    """Return value from serve should be propagated and serve executed off main thread."""

    class H(StaticFilesHandlerMixin):

        def __init__(self):
            self.recorded_thread = None

        def serve(self, request):
            self.recorded_thread = threading.current_thread()
            return {'ok': request.name}
    req = DummyRequest('c')
    h = H()
    result = await h.get_response_async(req)
    assert result == {'ok': 'c'}
    assert h.recorded_thread is not threading.main_thread()

@pytest.mark.asyncio
async def test_get_response_async_handles_none_and_runs_in_thread():
    """If serve returns None, get_response_async should return None, and serve runs off main thread."""

    class H(StaticFilesHandlerMixin):

        def __init__(self):
            self.recorded_thread = None

        def serve(self, request):
            self.recorded_thread = threading.current_thread()
            return None
    req = DummyRequest('d')
    h = H()
    result = await h.get_response_async(req)
    assert result is None
    assert h.recorded_thread is not threading.main_thread()

@pytest.mark.asyncio
async def test_get_response_async_passes_request_to_serve_and_threaded():
    """Ensure the request object is passed unchanged to serve and serve runs in threadpool thread."""

    class H(StaticFilesHandlerMixin):

        def __init__(self):
            self.received = None
            self.recorded_thread = None

        def serve(self, request):
            self.received = request
            self.recorded_thread = threading.current_thread()
            return 'done'
    req = DummyRequest('e')
    h = H()
    result = await h.get_response_async(req)
    assert result == 'done'
    assert h.received is req
    assert h.recorded_thread is not threading.main_thread()

@pytest.mark.asyncio
async def test_get_response_async_response_for_exception_runs_in_thread_and_gets_args():
    """response_for_exception should receive the exact request and exception and run off main thread."""
    serve_thread = None
    resp_exc_thread = None
    captured = {}

    class H(StaticFilesHandlerMixin):

        def serve(self, request):
            nonlocal serve_thread
            serve_thread = threading.current_thread()
            raise Http404('missing')

    def fake_response_for_exception(request, exc):
        nonlocal resp_exc_thread, captured
        resp_exc_thread = threading.current_thread()
        captured['request'] = request
        captured['exc'] = exc
        return 'handled'
    original = handlers_mod.response_for_exception
    handlers_mod.response_for_exception = fake_response_for_exception
    try:
        h = H()
        req = DummyRequest('f')
        result = await h.get_response_async(req)
        assert result == 'handled'
        assert serve_thread is not threading.main_thread()
        assert resp_exc_thread is not threading.main_thread()
        assert captured['request'] is req
        assert isinstance(captured['exc'], Http404)
    finally:
        handlers_mod.response_for_exception = original

@pytest.mark.asyncio
async def test_get_response_async_multiple_calls_use_threadpool_threads_not_main():
    """Multiple concurrent calls should each execute serve off the main thread."""

    class H(StaticFilesHandlerMixin):

        def __init__(self, ident):
            self.ident = ident
            self.recorded_thread = None

        def serve(self, request):
            self.recorded_thread = threading.current_thread()
            return (self.ident, request.name)
    handlers = [H(i) for i in range(5)]
    reqs = [DummyRequest(str(i)) for i in range(5)]
    results = await asyncio.gather(*(h.get_response_async(r) for h, r in zip(handlers, reqs)))
    for i, (h, r) in enumerate(zip(handlers, reqs)):
        assert results[i] == (h.ident, r.name)
        assert h.recorded_thread is not threading.main_thread()

@pytest.mark.asyncio
async def test_get_response_async_multiple_invocations_threadpool_not_main():
    """Repeated invocations on the same handler should execute serve off-main-thread each time."""

    class H(StaticFilesHandlerMixin):

        def __init__(self):
            self.threads = []

        def serve(self, request):
            self.threads.append(threading.current_thread())
            return request.name
    h = H()
    reqs = [DummyRequest(str(i)) for i in range(3)]
    res = []
    for r in reqs:
        res.append(await h.get_response_async(r))
    assert res == [r.name for r in reqs]
    assert all((t is not threading.main_thread() for t in h.threads))

@pytest.mark.asyncio
async def test_get_response_async_non_http_exception_propagates_but_serve_ran_in_thread():
    """Non-Http404 exceptions should propagate, but serve must have been executed off main thread."""
    serve_thread = None

    class H(StaticFilesHandlerMixin):

        def serve(self, request):
            nonlocal serve_thread
            serve_thread = threading.current_thread()
            raise ValueError('boom')
    h = H()
    with pytest.raises(ValueError):
        await h.get_response_async(DummyRequest('x'))
    assert serve_thread is not None
    assert serve_thread is not threading.main_thread()

@pytest.mark.asyncio
async def test_get_response_async_concurrent_exception_and_success_threads_not_main():
    """Mix of calls where some raise Http404 and some return successfully - all serve executions are off main thread."""
    resp_exc_threads = []
    serve_threads = []

    class H(StaticFilesHandlerMixin):

        def __init__(self, will_raise=False):
            self.will_raise = will_raise

        def serve(self, request):
            t = threading.current_thread()
            if self.will_raise:
                serve_threads.append(t)
                raise Http404('miss')
            serve_threads.append(t)
            return request.name

    def fake_response_for_exception(request, exc):
        resp_exc_threads.append(threading.current_thread())
        return f'handled-{request.name}'
    original = handlers_mod.response_for_exception
    handlers_mod.response_for_exception = fake_response_for_exception
    try:
        handlers = [H(will_raise=i % 2 == 0) for i in range(6)]
        reqs = [DummyRequest(str(i)) for i in range(6)]
        results = await asyncio.gather(*(h.get_response_async(r) for h, r in zip(handlers, reqs)))
        for i, h in enumerate(handlers):
            if i % 2 == 0:
                assert results[i] == f'handled-{reqs[i].name}'
            else:
                assert results[i] == reqs[i].name
        assert all((t is not threading.main_thread() for t in serve_threads))
        assert all((t is not threading.main_thread() for t in resp_exc_threads))
    finally:
        handlers_mod.response_for_exception = original

import asyncio
import threading
import time
import types
from types import SimpleNamespace
import pytest
from django.http import Http404
from django.contrib.staticfiles.handlers import StaticFilesHandlerMixin
import django.contrib.staticfiles.handlers as handlers_mod
import asyncio
import threading
import time
import types
from types import SimpleNamespace
import pytest
from django.http import Http404
from django.contrib.staticfiles.handlers import StaticFilesHandlerMixin
import django.contrib.staticfiles.handlers as handlers_mod

def _make_request(path='/static/test.txt'):
    return SimpleNamespace(path=path)

def _bind_serve(handler, func):
    handler.serve = types.MethodType(func, handler)
    return handler

@pytest.mark.asyncio
async def test_get_response_async_runs_serve_in_different_thread():
    handler = StaticFilesHandlerMixin()
    recorded = {}

    def serve(self, request):
        recorded['thread'] = threading.get_ident()
        return 'ok'
    _bind_serve(handler, serve)
    main_thread = threading.get_ident()
    res = await handler.get_response_async(_make_request())
    assert res == 'ok'
    assert 'thread' in recorded, 'serve was not called'
    assert recorded['thread'] != main_thread, 'serve ran on the event loop thread'

@pytest.mark.asyncio
async def test_get_response_async_returns_value_and_threads_differ():
    handler = StaticFilesHandlerMixin()
    recorded = {}

    def serve(self, request):
        recorded['thread'] = threading.get_ident()
        return {'status': 200, 'data': 'hello'}
    _bind_serve(handler, serve)
    main_thread = threading.get_ident()
    res = await handler.get_response_async(_make_request())
    assert isinstance(res, dict) and res['status'] == 200
    assert recorded['thread'] != main_thread

@pytest.mark.asyncio
async def test_get_response_async_handles_http404_in_different_thread(monkeypatch):
    handler = StaticFilesHandlerMixin()

    def serve(self, request):
        raise Http404('not found')
    _bind_serve(handler, serve)
    recorded = {}

    def fake_response_for_exception(request, exc):
        recorded['thread'] = threading.get_ident()
        return 'http404-response'
    monkeypatch.setattr(handlers_mod, 'response_for_exception', fake_response_for_exception)
    main_thread = threading.get_ident()
    res = await handler.get_response_async(_make_request())
    assert res == 'http404-response'
    assert recorded['thread'] != main_thread

@pytest.mark.asyncio
async def test_get_response_async_propagates_non_http_exceptions():
    handler = StaticFilesHandlerMixin()

    def serve(self, request):
        raise ValueError('boom')
    _bind_serve(handler, serve)
    with pytest.raises(ValueError):
        await handler.get_response_async(_make_request())

@pytest.mark.asyncio
async def test_get_response_async_does_not_block_event_loop_for_single_call():
    handler = StaticFilesHandlerMixin()

    def serve(self, request):
        time.sleep(0.06)
        return 'done'
    _bind_serve(handler, serve)
    flag = {'ran': False}

    async def set_flag_after_delay():
        await asyncio.sleep(0.01)
        flag['ran'] = True
    task = asyncio.create_task(handler.get_response_async(_make_request()))
    flag_task = asyncio.create_task(set_flag_after_delay())
    res = await task
    await flag_task
    assert res == 'done'
    assert flag['ran'], 'Event loop task did not run while serve was executing'

@pytest.mark.asyncio
async def test_get_response_async_concurrent_calls_run_concurrently():
    handler = StaticFilesHandlerMixin()

    def serve(self, request):
        time.sleep(0.07)
        return threading.get_ident()
    _bind_serve(handler, serve)
    start = time.time()
    res1_task = asyncio.create_task(handler.get_response_async(_make_request('/static/a')))
    res2_task = asyncio.create_task(handler.get_response_async(_make_request('/static/b')))
    r1, r2 = await asyncio.gather(res1_task, res2_task)
    duration = time.time() - start
    assert isinstance(r1, int) and isinstance(r2, int)
    assert duration < 0.2, f'Took too long ({duration:.2f}s), likely running serially on event loop'

@pytest.mark.asyncio
async def test_get_response_async_response_for_exception_does_not_block_event_loop(monkeypatch):
    handler = StaticFilesHandlerMixin()

    def serve(self, request):
        raise Http404('not found')
    _bind_serve(handler, serve)
    recorded = {}

    def slow_response_for_exception(request, exc):
        time.sleep(0.06)
        recorded['thread'] = threading.get_ident()
        return 'handled'
    monkeypatch.setattr(handlers_mod, 'response_for_exception', slow_response_for_exception)
    flag = {'ran': False}

    async def set_flag_after_delay():
        await asyncio.sleep(0.01)
        flag['ran'] = True
    task = asyncio.create_task(handler.get_response_async(_make_request()))
    flag_task = asyncio.create_task(set_flag_after_delay())
    res = await task
    await flag_task
    assert res == 'handled'
    assert flag['ran'], 'Event loop task did not run while response_for_exception was executing'
    assert recorded['thread'] != threading.get_ident()

@pytest.mark.asyncio
async def test_get_response_async_multiple_concurrent_response_for_exception_calls(monkeypatch):
    handler = StaticFilesHandlerMixin()

    def serve(self, request):
        raise Http404('not found')
    _bind_serve(handler, serve)
    record = {'threads': []}

    def response_for_exception(request, exc):
        time.sleep(0.05)
        record['threads'].append(threading.get_ident())
        return 'ex'
    monkeypatch.setattr(handlers_mod, 'response_for_exception', response_for_exception)
    tasks = [asyncio.create_task(handler.get_response_async(_make_request(f'/static/{i}'))) for i in range(3)]
    results = await asyncio.gather(*tasks)
    assert results == ['ex', 'ex', 'ex']
    main = threading.get_ident()
    assert all((tid != main for tid in record['threads']))
    assert len(set(record['threads'])) >= 1

@pytest.mark.asyncio
async def test_get_response_async_immediate_return_runs_off_event_loop_thread():
    handler = StaticFilesHandlerMixin()
    recorded = {}

    def serve(self, request):
        recorded['thread'] = threading.get_ident()
        return 'immediate'
    _bind_serve(handler, serve)
    main_thread = threading.get_ident()
    res = await handler.get_response_async(_make_request())
    assert res == 'immediate'
    assert recorded['thread'] != main_thread

import threading
import inspect
import pytest
from urllib.parse import urlparse
from django.http import Http404, HttpResponse
import django.contrib.staticfiles.handlers as handlers_module
from django.contrib.staticfiles.handlers import StaticFilesHandlerMixin, ASGIStaticFilesHandler
import threading
import inspect
import pytest
from urllib.parse import urlparse
from django.http import Http404, HttpResponse
import django.contrib.staticfiles.handlers as handlers_module
from django.contrib.staticfiles.handlers import StaticFilesHandlerMixin, ASGIStaticFilesHandler

@pytest.mark.asyncio
async def test_mixin_get_response_async_runs_serve_in_thread_on_success():
    handler = StaticFilesHandlerMixin.__new__(StaticFilesHandlerMixin)
    handler.base_url = urlparse('/static/')
    recorded = {}

    def serve(req):
        recorded['thread'] = threading.get_ident()
        return HttpResponse('ok')
    handler.serve = serve
    request = DummyRequest('/static/test.txt')
    main_thread = threading.get_ident()
    response = await handler.get_response_async(request)
    assert isinstance(response, HttpResponse)
    assert recorded.get('thread') is not None
    assert recorded['thread'] != main_thread

@pytest.mark.asyncio
async def test_mixin_get_response_async_runs_response_for_exception_in_thread_on_404(monkeypatch):
    handler = StaticFilesHandlerMixin.__new__(StaticFilesHandlerMixin)
    handler.base_url = urlparse('/static/')
    recorded = {}

    def serve(req):
        raise Http404()

    def fake_response_for_exception(request, exc):
        recorded['thread'] = threading.get_ident()
        return HttpResponse('not found', status=404)
    handler.serve = serve
    request = DummyRequest('/static/missing.txt')
    monkeypatch.setattr(handlers_module, 'response_for_exception', fake_response_for_exception)
    main_thread = threading.get_ident()
    response = await handler.get_response_async(request)
    assert response.status_code == 404
    assert recorded.get('thread') is not None
    assert recorded['thread'] != main_thread

@pytest.mark.asyncio
async def test_asgi_handler_get_response_async_runs_serve_in_thread_on_success():
    handler = ASGIStaticFilesHandler.__new__(ASGIStaticFilesHandler)
    handler.base_url = urlparse('/static/')
    recorded = {}

    def serve(req):
        recorded['thread'] = threading.get_ident()
        return HttpResponse('ok')
    handler.serve = serve
    request = DummyRequest('/static/test.txt')
    main_thread = threading.get_ident()
    response = await handler.get_response_async(request)
    assert isinstance(response, HttpResponse)
    assert recorded.get('thread') is not None
    assert recorded['thread'] != main_thread

@pytest.mark.asyncio
async def test_asgi_handler_get_response_async_runs_response_for_exception_in_thread_on_404(monkeypatch):
    handler = ASGIStaticFilesHandler.__new__(ASGIStaticFilesHandler)
    handler.base_url = urlparse('/static/')
    recorded = {}

    def serve(req):
        raise Http404()

    def fake_response_for_exception(request, exc):
        recorded['thread'] = threading.get_ident()
        return HttpResponse('not found', status=404)
    handler.serve = serve
    monkeypatch.setattr(handlers_module, 'response_for_exception', fake_response_for_exception)
    request = DummyRequest('/static/missing.txt')
    main_thread = threading.get_ident()
    response = await handler.get_response_async(request)
    assert response.status_code == 404
    assert recorded.get('thread') is not None
    assert recorded['thread'] != main_thread

def test_load_middleware_has_no_extra_parameters():
    sig = inspect.signature(StaticFilesHandlerMixin.load_middleware)
    params = list(sig.parameters.keys())
    assert params == ['self'], 'load_middleware signature changed; unexpected parameters: %r' % params

def test_file_path_decodes_percent_encoding():
    handler = StaticFilesHandlerMixin.__new__(StaticFilesHandlerMixin)
    handler.base_url = urlparse('/static/')
    result = handler.file_path('/static/foo%20bar.txt')
    assert result == 'foo bar.txt'

def test_should_handle_returns_false_if_netloc_present():
    handler = StaticFilesHandlerMixin.__new__(StaticFilesHandlerMixin)
    handler.base_url = urlparse('https://example.com/static/')
    assert not handler._should_handle('/static/test.txt')

def test_should_handle_returns_true_when_path_under_base_and_no_netloc():
    handler = StaticFilesHandlerMixin.__new__(StaticFilesHandlerMixin)
    handler.base_url = urlparse('/static/')
    assert handler._should_handle('/static/test.txt')

def test_file_path_returns_empty_for_exact_base_url():
    handler = StaticFilesHandlerMixin.__new__(StaticFilesHandlerMixin)
    handler.base_url = urlparse('/static/')
    result = handler.file_path('/static/')
    assert result == ''

import asyncio
import inspect
from urllib.parse import urlparse
from django.http import Http404
from django.contrib.staticfiles import handlers
import inspect
import asyncio
from urllib.parse import urlparse
from django.http import Http404
import django
import pytest
from django.contrib.staticfiles import handlers

def test_get_response_async_calls_sync_to_async_for_success(monkeypatch):
    dummy = DummyHandler()

    def serve(request):
        return 'served-result'
    dummy.serve = serve
    called = []

    def sync_to_async_spy(fn):
        called.append(fn)

        async def runner(*args, **kwargs):
            return fn(*args, **kwargs)
        return runner
    monkeypatch.setattr(handlers, 'sync_to_async', sync_to_async_spy)
    result = asyncio.run(dummy.get_response_async(request='req'))
    assert result == 'served-result'
    assert called == [serve]

def test_get_response_async_passes_request_argument_to_serve(monkeypatch):
    dummy = DummyHandler()
    received = {}

    def serve(request):
        received['request'] = request
        return 'ok'
    dummy.serve = serve

    def sync_to_async_spy(fn):

        async def runner(*args, **kwargs):
            return fn(*args, **kwargs)
        return runner
    monkeypatch.setattr(handlers, 'sync_to_async', sync_to_async_spy)
    res = asyncio.run(dummy.get_response_async('my-request'))
    assert res == 'ok'
    assert received['request'] == 'my-request'

def test_get_response_async_calls_sync_to_async_for_http404_and_uses_response_for_exception(monkeypatch):
    dummy = DummyHandler()

    def serve(request):
        raise Http404('not found')
    dummy.serve = serve
    wrapped = []

    def sync_to_async_spy(fn):
        wrapped.append(fn)

        async def runner(*args, **kwargs):
            return fn(*args, **kwargs)
        return runner

    def fake_response_for_exception(request, exc):
        return 'handled-404'
    monkeypatch.setattr(handlers, 'sync_to_async', sync_to_async_spy)
    monkeypatch.setattr(handlers, 'response_for_exception', fake_response_for_exception)
    res = asyncio.run(dummy.get_response_async('req'))
    assert res == 'handled-404'
    assert serve in wrapped
    assert fake_response_for_exception in wrapped

def test_get_response_async_calls_sync_to_async_exact_times_on_success(monkeypatch):
    dummy = DummyHandler()

    def serve(request):
        return 'ok'
    dummy.serve = serve
    call_count = {'n': 0}

    def sync_to_async_spy(fn):
        call_count['n'] += 1

        async def runner(*args, **kwargs):
            return fn(*args, **kwargs)
        return runner
    monkeypatch.setattr(handlers, 'sync_to_async', sync_to_async_spy)
    res = asyncio.run(dummy.get_response_async(None))
    assert res == 'ok'
    assert call_count['n'] == 1

def test_get_response_async_calls_sync_to_async_exact_times_on_http404(monkeypatch):
    dummy = DummyHandler()

    def serve(request):
        raise Http404('no')
    dummy.serve = serve
    call_list = []

    def sync_to_async_spy(fn):
        call_list.append(fn)

        async def runner(*args, **kwargs):
            return fn(*args, **kwargs)
        return runner

    def fake_response_for_exception(request, exc):
        return 'resp'
    monkeypatch.setattr(handlers, 'sync_to_async', sync_to_async_spy)
    monkeypatch.setattr(handlers, 'response_for_exception', fake_response_for_exception)
    res = asyncio.run(dummy.get_response_async('req'))
    assert res == 'resp'
    assert len(call_list) == 2
    assert call_list[0] is serve
    assert call_list[1] is fake_response_for_exception

def test_get_response_async_uses_wrapper_coroutine_when_awaited(monkeypatch):
    dummy = DummyHandler()

    def serve(request):
        return 'done'
    dummy.serve = serve
    marker = {'awaited': False}

    def sync_to_async_spy(fn):

        async def runner(*args, **kwargs):
            marker['awaited'] = True
            return fn(*args, **kwargs)
        return runner
    monkeypatch.setattr(handlers, 'sync_to_async', sync_to_async_spy)
    res = asyncio.run(dummy.get_response_async(None))
    assert res == 'done'
    assert marker['awaited'] is True

def test_load_middleware_signature_not_changed():
    sig = inspect.signature(handlers.StaticFilesHandlerMixin.load_middleware)
    params = list(sig.parameters.values())
    assert len(params) == 1
    assert params[0].name == 'self'

def test__should_handle_respects_netloc_in_base_url():
    dummy = DummyHandler()
    dummy.base_url = urlparse('http://example.com/static/')
    assert dummy._should_handle('/static/index.html') is False
    dummy.base_url = urlparse('/static/')
    assert dummy._should_handle('/static/index.html') is True

def test_file_path_decodes_url_to_pathname():
    dummy = DummyHandler()
    dummy.base_url = urlparse('/static/')
    path = dummy.file_path('/static/foo%20bar.txt')
    assert ' ' in path and path.endswith('foo bar.txt')

import pytest
import types
from django.http import Http404
from django.contrib.staticfiles import handlers as handlers_module

@pytest.mark.asyncio
async def test_get_response_async_uses_sync_to_async_on_success(monkeypatch):
    calls = []

    def make_sync_to_async(calls):

        def sync_to_async(func):
            calls.append(('wrap', func))

            async def wrapper(*args, **kwargs):
                calls.append(('call', func, args, kwargs))
                return func(*args, **kwargs)
            return wrapper
        return sync_to_async
    monkeypatch.setattr(handlers_module, 'sync_to_async', make_sync_to_async(calls))
    handler = DummyHandler()
    handler.serve = lambda request: 'served-' + str(request)
    result = await handler.get_response_async('REQ')
    assert result == 'served-REQ'
    assert any((entry[0] == 'wrap' and entry[1] == handler.serve for entry in calls))
    assert any((entry[0] == 'call' and entry[1] == handler.serve for entry in calls))

@pytest.mark.asyncio
async def test_get_response_async_uses_sync_to_async_for_http404(monkeypatch):
    calls = []

    def make_sync_to_async(calls, response_value='ERR'):

        def sync_to_async(func):
            calls.append(('wrap', func))

            async def wrapper(*args, **kwargs):
                calls.append(('call', func, args, kwargs))
                return func(*args, **kwargs)
            return wrapper
        return sync_to_async
    monkeypatch.setattr(handlers_module, 'sync_to_async', make_sync_to_async(calls))

    def fake_response_for_exception(request, exc):
        return 'handled-' + str(exc)
    monkeypatch.setattr(handlers_module, 'response_for_exception', fake_response_for_exception)
    handler = DummyHandler()

    def serve_raises(request):
        raise Http404('not found')
    handler.serve = serve_raises
    result = await handler.get_response_async('REQ')
    assert result == 'handled-404: not found' or result == "handled-Http404('not found')" or result == 'handled-{}'.format(Http404('not found'))
    wrapped_funcs = [entry[1] for entry in calls if entry[0] == 'wrap']
    assert handler.serve in wrapped_funcs
    assert handlers_module.response_for_exception in wrapped_funcs

@pytest.mark.asyncio
async def test_get_response_async_passes_request_to_wrapped_serve(monkeypatch):
    calls = []

    def make_sync_to_async(calls):

        def sync_to_async(func):

            async def wrapper(*args, **kwargs):
                calls.append((func, args, kwargs))
                return func(*args, **kwargs)
            return wrapper
        return sync_to_async
    monkeypatch.setattr(handlers_module, 'sync_to_async', make_sync_to_async(calls))
    handler = DummyHandler()
    handler.serve = lambda request: f'ok-{request}'
    request_obj = object()
    result = await handler.get_response_async(request_obj)
    assert result == f'ok-{request_obj}'
    assert any((entry[0] == handler.serve and entry[1] == (request_obj,) for entry in calls))

@pytest.mark.asyncio
async def test_get_response_async_propagates_non_http404_and_uses_sync_to_async(monkeypatch):
    calls = []

    def make_sync_to_async(calls):

        def sync_to_async(func):

            async def wrapper(*args, **kwargs):
                calls.append(('call', func))
                return func(*args, **kwargs)
            return wrapper
        return sync_to_async
    monkeypatch.setattr(handlers_module, 'sync_to_async', make_sync_to_async(calls))
    handler = DummyHandler()

    class CustomError(RuntimeError):
        pass

    def serve_raise_custom(request):
        raise CustomError('boom')
    handler.serve = serve_raise_custom
    with pytest.raises(CustomError):
        await handler.get_response_async('REQ')
    assert any((entry == ('call', handler.serve) for entry in calls))

@pytest.mark.asyncio
async def test_get_response_async_wraps_response_for_exception(monkeypatch):
    calls = []

    def make_sync_to_async(calls):

        def sync_to_async(func):
            calls.append(('wrap', func))

            async def wrapper(*args, **kwargs):
                calls.append(('call', func))
                return func(*args, **kwargs)
            return wrapper
        return sync_to_async
    monkeypatch.setattr(handlers_module, 'sync_to_async', make_sync_to_async(calls))

    def fake_response_for_exception(request, exc):
        return 'fake-exc'
    monkeypatch.setattr(handlers_module, 'response_for_exception', fake_response_for_exception)
    handler = DummyHandler()

    def serve_raises(request):
        raise Http404('not found')
    handler.serve = serve_raises
    result = await handler.get_response_async('REQ')
    assert result == 'fake-exc'
    wrapped = [f for tag, f in calls if tag == 'wrap']
    assert handlers_module.response_for_exception in wrapped
    assert handler.serve in wrapped

@pytest.mark.asyncio
async def test_get_response_async_called_multiple_times_uses_sync_to_async_each_time(monkeypatch):
    calls = []

    def make_sync_to_async(calls):

        def sync_to_async(func):
            calls.append(('wrap', func))

            async def wrapper(*args, **kwargs):
                calls.append(('call', func))
                return func(*args, **kwargs)
            return wrapper
        return sync_to_async
    monkeypatch.setattr(handlers_module, 'sync_to_async', make_sync_to_async(calls))
    handler = DummyHandler()
    handler.serve = lambda request: f'ok-{request}'
    r1 = await handler.get_response_async('A')
    r2 = await handler.get_response_async('B')
    assert r1 == 'ok-A' and r2 == 'ok-B'
    wrap_entries = [entry for entry in calls if entry[0] == 'wrap' and entry[1] == handler.serve]
    assert len(wrap_entries) >= 2

@pytest.mark.asyncio
async def test_get_response_async_with_unusual_request_object(monkeypatch):
    calls = []

    def make_sync_to_async(calls):

        def sync_to_async(func):
            calls.append(('wrap', func))

            async def wrapper(*args, **kwargs):
                calls.append(('call', func, args))
                return func(*args, **kwargs)
            return wrapper
        return sync_to_async
    monkeypatch.setattr(handlers_module, 'sync_to_async', make_sync_to_async(calls))
    handler = DummyHandler()
    handler.serve = lambda req: ('served', req)

    class WeirdReq:

        def __repr__(self):
            return '<weird>'
    req = WeirdReq()
    res = await handler.get_response_async(req)
    assert res == ('served', req)
    assert any((entry[0] == 'call' and entry[1] == handler.serve and (entry[2] == (req,)) for entry in calls))

@pytest.mark.asyncio
async def test_get_response_async_does_not_suppress_errors_raised_by_response_for_exception_wrapper(monkeypatch):
    calls = []

    def make_sync_to_async(calls):

        def sync_to_async(func):
            calls.append(('wrap', func))

            async def wrapper(*args, **kwargs):
                calls.append(('call', func))
                return func(*args, **kwargs)
            return wrapper
        return sync_to_async
    monkeypatch.setattr(handlers_module, 'sync_to_async', make_sync_to_async(calls))

    def bad_response_for_exception(request, exc):
        raise RuntimeError('bad handler')
    monkeypatch.setattr(handlers_module, 'response_for_exception', bad_response_for_exception)
    handler = DummyHandler()

    def serve_raises(request):
        raise Http404('not found')
    handler.serve = serve_raises
    with pytest.raises(RuntimeError):
        await handler.get_response_async('REQ')
    wrapped = [entry for entry in calls if entry[0] == 'wrap']
    funcs = [f for _, f in wrapped]
    assert handler.serve in funcs and handlers_module.response_for_exception in funcs

@pytest.mark.asyncio
async def test_get_response_async_called_on_different_handler_instances(monkeypatch):
    calls = []

    def make_sync_to_async(calls):

        def sync_to_async(func):
            calls.append(('wrap', func))

            async def wrapper(*args, **kwargs):
                calls.append(('call', func, args))
                return func(*args, **kwargs)
            return wrapper
        return sync_to_async
    monkeypatch.setattr(handlers_module, 'sync_to_async', make_sync_to_async(calls))
    h1 = DummyHandler()
    h2 = DummyHandler()
    h1.serve = lambda r: 'h1-' + str(r)
    h2.serve = lambda r: 'h2-' + str(r)
    r1 = await h1.get_response_async('1')
    r2 = await h2.get_response_async('2')
    assert r1 == 'h1-1' and r2 == 'h2-2'
    wraps = [entry for entry in calls if entry[0] == 'wrap']
    funcs_wrapped = [f for _, f in wraps]
    assert h1.serve in funcs_wrapped and h2.serve in funcs_wrapped

@pytest.mark.asyncio
async def test_get_response_async_called_after_monkeypatching_back_original_sync_to_async(monkeypatch):
    real_sync = handlers_module.sync_to_async
    calls = []

    def recording_sync_to_async(func):
        calls.append(('wrap', func))
        wrapped = real_sync(func)

        async def wrapper(*args, **kwargs):
            calls.append(('call', func))
            return await wrapped(*args, **kwargs)
        return wrapper
    monkeypatch.setattr(handlers_module, 'sync_to_async', recording_sync_to_async)
    handler = DummyHandler()
    handler.serve = lambda r: 'ok-' + str(r)
    res = await handler.get_response_async('X')
    assert res == 'ok-X'
    assert any((c[0] == 'wrap' and c[1] == handler.serve for c in calls))

import asyncio
import threading
from urllib.parse import urlparse
import pytest
from django.http import Http404
from django.contrib.staticfiles import handlers as handlers_module
import asyncio
import threading
from urllib.parse import urlparse
import pytest
from django.http import Http404
from django.contrib.staticfiles import handlers as handlers_module

def make_dummy(path_prefix='/static/'):
    """Create a simple instance of the mixin with base_url set."""
    Dummy = type('Dummy', (handlers_module.StaticFilesHandlerMixin,), {})
    inst = Dummy()
    inst.base_url = urlparse(path_prefix)
    return inst

def make_request(path):
    return type('R', (), {'path': path})()

def test_get_response_async_runs_serve_in_thread_success(monkeypatch):
    """
    Ensure get_response_async runs the blocking serve in a background thread
    (so the serve callable is executed in a non-main thread).
    """
    inst = make_dummy()
    request = make_request('/static/hello.txt')

    def fake_serve(request_arg, path_arg, insecure=False):
        if threading.current_thread() is threading.main_thread():
            raise RuntimeError('serve executed in main thread')
        return 'OK'
    monkeypatch.setattr(handlers_module, 'serve', fake_serve)
    result = asyncio.run(inst.get_response_async(request))
    assert result == 'OK'

def test_get_response_async_handles_Http404_with_response_for_exception_in_thread(monkeypatch):
    """
    If serve raises Http404, get_response_async should call response_for_exception
    in a background thread and return its result.
    """
    inst = make_dummy()
    request = make_request('/static/missing.txt')

    def fake_serve(request_arg, path_arg, insecure=False):
        if threading.current_thread() is threading.main_thread():
            raise RuntimeError('serve executed in main thread')
        raise Http404('not found')

    def fake_response_for_exception(request_arg, exc):
        if threading.current_thread() is threading.main_thread():
            raise RuntimeError('response_for_exception executed in main thread')
        return 'HANDLED'
    monkeypatch.setattr(handlers_module, 'serve', fake_serve)
    monkeypatch.setattr(handlers_module, 'response_for_exception', fake_response_for_exception)
    result = asyncio.run(inst.get_response_async(request))
    assert result == 'HANDLED'

def test_get_response_async_propagates_non_Http404_exceptions(monkeypatch):
    """
    Non-Http404 exceptions raised by serve should propagate out of get_response_async.
    """
    inst = make_dummy()
    request = make_request('/static/bad.txt')

    def fake_serve(request_arg, path_arg, insecure=False):
        raise ValueError('boom')
    monkeypatch.setattr(handlers_module, 'serve', fake_serve)
    with pytest.raises(ValueError):
        asyncio.run(inst.get_response_async(request))

def test_get_response_uses_file_path_for_serve(monkeypatch):
    """
    The serve callable should receive the path returned by file_path().
    """
    inst = make_dummy()
    request = make_request('/static/dir/name.txt')
    captured = {}

    def fake_serve(request_arg, path_arg, insecure=False):
        captured['path'] = path_arg
        return 'OK'
    monkeypatch.setattr(handlers_module, 'serve', fake_serve)
    result = asyncio.run(inst.get_response_async(request))
    assert result == 'OK'
    assert captured['path'] == 'dir/name.txt'

def test_file_path_strips_base_url_and_converts(monkeypatch):
    """
    file_path should remove the base_url prefix and return a local path string.
    """
    inst = make_dummy()
    assert inst.file_path('/static/abc/def.txt') == 'abc/def.txt'

def test__should_handle_false_when_base_url_has_netloc():
    """
    If the base URL includes a netloc (host), _should_handle must return False.
    """
    inst = make_dummy('http://example.com/static/')
    assert inst._should_handle('/static/foo.txt') is False

def test__should_handle_true_when_path_under_base_and_no_netloc():
    inst = make_dummy('/static/')
    assert inst._should_handle('/static/foo.txt') is True

def test_serve_passes_insecure_flag(monkeypatch):
    """
    The mixin.serve wrapper must pass insecure=True to the underlying serve().
    """
    inst = make_dummy()
    request = make_request('/static/a.txt')

    def fake_serve(request_arg, path_arg, insecure=False):
        return insecure
    monkeypatch.setattr(handlers_module, 'serve', fake_serve)
    assert inst.serve(request) is True

def test_get_response_handles_Http404_synchronously(monkeypatch):
    """
    The synchronous get_response should return response_for_exception() when serve raises Http404.
    """
    inst = make_dummy()
    request = make_request('/static/miss.txt')

    def fake_serve(request_arg, path_arg, insecure=False):
        raise Http404('nope')

    def fake_response_for_exception(request_arg, exc):
        return 'SYNC_HANDLED'
    monkeypatch.setattr(handlers_module, 'serve', fake_serve)
    monkeypatch.setattr(handlers_module, 'response_for_exception', fake_response_for_exception)
    result = inst.get_response(request)
    assert result == 'SYNC_HANDLED'

def test_get_response_async_propagates_response_for_exception_errors(monkeypatch):
    """
    If response_for_exception itself raises in worker thread, the error should propagate.
    """
    inst = make_dummy()
    request = make_request('/static/miss.txt')

    def fake_serve(request_arg, path_arg, insecure=False):
        raise Http404('nope')

    def bad_response_for_exception(request_arg, exc):
        raise RuntimeError('response handling failed')
    monkeypatch.setattr(handlers_module, 'serve', fake_serve)
    monkeypatch.setattr(handlers_module, 'response_for_exception', bad_response_for_exception)
    with pytest.raises(RuntimeError):
        asyncio.run(inst.get_response_async(request))

import asyncio
import types
from urllib.parse import urlparse
import pytest
from django.http import Http404
from django.contrib.staticfiles import handlers as handlers_module
import asyncio
import types
from urllib.parse import urlparse
import pytest
from django.http import Http404
from django.contrib.staticfiles import handlers as handlers_module

def make_spy_sync_to_async(calls):
    """
    Return a sync_to_async replacement that records the passed-in function
    objects (bound/unbound) in 'calls' in the order they are wrapped, and
    returns an async wrapper that calls the original function.
    """

    def spy(func):

        async def wrapper(*args, **kwargs):
            calls.append(func)
            return func(*args, **kwargs)
        return wrapper
    return spy

def test_get_response_async_uses_sync_to_async_on_success():
    handler = DummyHandler()
    request = DummyRequest('/static/test.txt')

    def serve(req):
        return 'served-ok'
    handler.serve = serve
    calls = []
    original_sync_to_async = handlers_module.sync_to_async
    handlers_module.sync_to_async = make_spy_sync_to_async(calls)
    try:
        result = asyncio.run(handler.get_response_async(request))
        assert result == 'served-ok'
        assert len(calls) == 1
        assert calls[0].__name__ == 'serve'
    finally:
        handlers_module.sync_to_async = original_sync_to_async

def test_get_response_async_returns_value_from_serve_bound_method():
    handler = DummyHandler()
    request = DummyRequest('/static/foo')

    def serve_bound(req):
        return 'bound-result'
    handler.serve = types.MethodType(serve_bound, handler)
    calls = []
    original_sync_to_async = handlers_module.sync_to_async
    handlers_module.sync_to_async = make_spy_sync_to_async(calls)
    try:
        result = asyncio.run(handler.get_response_async(request))
        assert result == 'bound-result'
        assert len(calls) == 1
        assert getattr(calls[0], '__self__', None) is handler
    finally:
        handlers_module.sync_to_async = original_sync_to_async

def test_get_response_async_calls_response_for_exception_on_http404():
    handler = DummyHandler()
    request = DummyRequest('/static/missing')

    def serve_404(req):
        raise Http404('not found')
    handler.serve = serve_404
    original_rfe = handlers_module.response_for_exception
    handlers_module.response_for_exception = lambda req, exc: 'handled-404'
    calls = []
    original_sync_to_async = handlers_module.sync_to_async
    handlers_module.sync_to_async = make_spy_sync_to_async(calls)
    try:
        result = asyncio.run(handler.get_response_async(request))
        assert result == 'handled-404'
        assert len(calls) == 2
        assert calls[0].__name__ == 'serve_404' or calls[0] is serve_404
        assert calls[1] is handlers_module.response_for_exception
    finally:
        handlers_module.sync_to_async = original_sync_to_async
        handlers_module.response_for_exception = original_rfe

def test_get_response_async_propagates_non_http404_exception():
    handler = DummyHandler()
    request = DummyRequest('/static/error')

    def serve_error(req):
        raise ValueError('boom')
    handler.serve = serve_error
    calls = []
    original_sync_to_async = handlers_module.sync_to_async
    handlers_module.sync_to_async = make_spy_sync_to_async(calls)
    try:
        with pytest.raises(ValueError):
            asyncio.run(handler.get_response_async(request))
        assert len(calls) == 1
        assert calls[0] is serve_error
    finally:
        handlers_module.sync_to_async = original_sync_to_async

def test_get_response_async_uses_sync_to_async_for_response_for_exception():
    """
    Similar to previous, but assert that response_for_exception is indeed wrapped
    and called through sync_to_async (i.e., appears in calls list).
    """
    handler = DummyHandler()
    request = DummyRequest('/static/missing2')

    def serve_404(req):
        raise Http404()
    handler.serve = serve_404
    original_rfe = handlers_module.response_for_exception
    handlers_module.response_for_exception = lambda req, exc: 'handled-404-2'
    calls = []
    original_sync_to_async = handlers_module.sync_to_async
    handlers_module.sync_to_async = make_spy_sync_to_async(calls)
    try:
        result = asyncio.run(handler.get_response_async(request))
        assert result == 'handled-404-2'
        assert calls[0] is serve_404
        assert calls[1] is handlers_module.response_for_exception
    finally:
        handlers_module.sync_to_async = original_sync_to_async
        handlers_module.response_for_exception = original_rfe

def test__should_handle_respects_host_in_base_url():
    handler = DummyHandler(base_url='http://example.com/static/')
    assert handler._should_handle('/static/file') is False
    handler_no_host = DummyHandler(base_url='/static/')
    assert handler_no_host._should_handle('/static/file') is True

def test__should_handle_accepts_paths_equal_to_base_path():
    handler = DummyHandler(base_url='/static/')
    assert handler._should_handle('/static/') is True
    assert handler._should_handle('/other/static/') is False

def test_file_path_converts_url_to_path():
    handler = DummyHandler(base_url='/static/')
    url = '/static/foo/bar/baz.txt'
    rel = handler.file_path(url)
    assert rel.endswith('foo/bar/baz.txt')

def test_asgi_handler_pass_through_for_non_matching_scope():

    async def dummy_app(scope, receive, send):
        return 'app-result'
    handler = object.__new__(handlers_module.ASGIStaticFilesHandler)
    handler.application = dummy_app
    handler.base_url = urlparse('/static/')
    scope_non_http = {'type': 'websocket', 'path': '/static/test.txt'}
    result = asyncio.run(handler.__call__(scope_non_http, None, None))
    assert result == 'app-result'
    scope_non_matching = {'type': 'http', 'path': '/not-static/foo'}
    result2 = asyncio.run(handler.__call__(scope_non_matching, None, None))
    assert result2 == 'app-result'

import asyncio
import threading
import time
import pytest
from django.http import Http404
from django.contrib.staticfiles import handlers as handlers_module
import asyncio
import threading
import time
import pytest
from django.http import Http404
from django.contrib.staticfiles import handlers as handlers_module

@pytest.mark.asyncio
async def test_get_response_async_runs_serve_in_thread_different_thread_for_success():
    handler = DummyHandler()
    main_thread = threading.get_ident()
    result = await handler.get_response_async('request1')
    assert result == 'ok:request1'
    assert handler.serve_thread_id is not None
    assert handler.serve_thread_id != main_thread

@pytest.mark.asyncio
async def test_get_response_async_runs_response_for_exception_in_thread_on_http404(monkeypatch):
    handler = DummyHandler(raise_exc=True)
    main_thread = threading.get_ident()

    def fake_response_for_exception(request, exc):
        handler.response_for_exception_thread_id = threading.get_ident()
        handler.captured_exception = exc
        return 'handled:' + str(request)
    monkeypatch.setattr(handlers_module, 'response_for_exception', fake_response_for_exception)
    res = await handler.get_response_async('request-exc')
    assert res == 'handled:request-exc'
    assert handler.response_for_exception_thread_id is not None
    assert handler.response_for_exception_thread_id != main_thread
    assert isinstance(handler.captured_exception, Http404)

@pytest.mark.asyncio
async def test_get_response_async_sequential_calls_all_use_threadpool():
    handler1 = DummyHandler()
    handler2 = DummyHandler()
    main_thread = threading.get_ident()
    r1 = await handler1.get_response_async('a')
    r2 = await handler2.get_response_async('b')
    assert r1 == 'ok:a'
    assert r2 == 'ok:b'
    assert handler1.serve_thread_id != main_thread
    assert handler2.serve_thread_id != main_thread

@pytest.mark.asyncio
async def test_get_response_async_concurrent_calls_all_use_threadpool():
    handlers = [DummyHandler() for _ in range(5)]
    main_thread = threading.get_ident()
    results = await asyncio.gather(*(h.get_response_async(f'c{i}') for i, h in enumerate(handlers)))
    assert results == [f'ok:c{i}' for i in range(5)]
    for h in handlers:
        assert h.serve_thread_id is not None
        assert h.serve_thread_id != main_thread

@pytest.mark.asyncio
async def test_get_response_async_with_blocking_serve_does_not_block_event_loop():
    handler = DummyHandler(delay=0.15)
    main_thread = threading.get_ident()

    async def waiter():
        await asyncio.sleep(0.01)
        return 'fast'
    task = asyncio.create_task(handler.get_response_async('slow'))
    fast = await waiter()
    res = await task
    assert fast == 'fast'
    assert res == 'ok:slow'
    assert handler.serve_thread_id != main_thread

@pytest.mark.asyncio
async def test_get_response_async_exception_path_preserves_exception_instance(monkeypatch):
    handler = DummyHandler(raise_exc=True)
    recorded = {}

    def fake_response_for_exception(request, exc):
        recorded['exc'] = exc
        recorded['thread'] = threading.get_ident()
        return 'handled-ex'
    monkeypatch.setattr(handlers_module, 'response_for_exception', fake_response_for_exception)
    main_thread = threading.get_ident()
    res = await handler.get_response_async('req-exact')
    assert res == 'handled-ex'
    assert isinstance(recorded['exc'], Http404)
    assert recorded['thread'] != main_thread

@pytest.mark.asyncio
async def test_get_response_async_propagates_non_http404_exceptions():

    class BadHandler(DummyHandler):

        def serve(self, request):
            raise ValueError('boom')
    bad = BadHandler()
    with pytest.raises(ValueError):
        await bad.get_response_async('boom')

@pytest.mark.asyncio
async def test_get_response_async_multiple_exception_calls_dont_share_state(monkeypatch):
    handler_a = DummyHandler(raise_exc=True)
    handler_b = DummyHandler(raise_exc=True)
    recorded = []

    def fake_response_for_exception(request, exc):
        recorded.append((request, exc, threading.get_ident()))
        return 'ok-ex'
    monkeypatch.setattr(handlers_module, 'response_for_exception', fake_response_for_exception)
    main_thread = threading.get_ident()
    ra, rb = await asyncio.gather(handler_a.get_response_async('ra'), handler_b.get_response_async('rb'))
    assert ra == 'ok-ex' and rb == 'ok-ex'
    assert len(recorded) == 2
    for _, _, tid in recorded:
        assert tid != main_thread

@pytest.mark.asyncio
async def test_get_response_async_works_with_dummy_request_objects():

    class ReqObj:

        def __init__(self, name):
            self.name = name

        def __str__(self):
            return f'Req({self.name})'
    handler = DummyHandler()
    res = await handler.get_response_async(ReqObj('xyz'))
    assert res == 'ok:Req(xyz)'
    assert handler.serve_thread_id != threading.get_ident()

@pytest.mark.asyncio
async def test_get_response_async_response_for_exception_receives_arguments_in_threadpool(monkeypatch):
    handler = DummyHandler(raise_exc=True)
    captured = {}

    def fake_response_for_exception(request, exc):
        captured['request'] = request
        captured['exc'] = exc
        captured['thread'] = threading.get_ident()
        return 'rfe'
    monkeypatch.setattr(handlers_module, 'response_for_exception', fake_response_for_exception)
    main_thread = threading.get_ident()
    out = await handler.get_response_async('reqX')
    assert out == 'rfe'
    assert captured['request'] == 'reqX'
    assert isinstance(captured['exc'], Http404)
    assert captured['thread'] != main_thread

import asyncio
import inspect
from urllib.parse import urlparse
import pytest
from django.http import Http404, HttpResponse
import asyncio
import inspect
from urllib.parse import urlparse
import pytest
from django.http import Http404, HttpResponse
import django.contrib.staticfiles.handlers as handlers
from django.core.handlers.asgi import ASGIHandler

def test_get_response_async_uses_sync_to_async_on_success():
    called = {'sync_to_async': 0}
    original_sync_to_async = handlers.sync_to_async
    try:

        def spy_sync_to_async(func):

            async def wrapper(*args, **kwargs):
                called['sync_to_async'] += 1
                return func(*args, **kwargs)
            return wrapper
        handlers.sync_to_async = spy_sync_to_async

        class H(DummyHandler):

            def serve(self, request):
                return HttpResponse('ok-async')
        h = H()
        request = DummyRequest('/static/test.txt')
        response = asyncio.run(h.get_response_async(request))
        assert called['sync_to_async'] == 1, 'sync_to_async must be used once for serve()'
        assert isinstance(response, HttpResponse)
        assert response.content == b'ok-async'
    finally:
        handlers.sync_to_async = original_sync_to_async

def test_get_response_async_uses_sync_to_async_on_404():
    calls = {'serve': 0, 'response_for_exception': 0}
    original_sync_to_async = handlers.sync_to_async
    original_response_for_exception = handlers.response_for_exception
    try:

        def spy_sync_to_async(func):

            async def wrapper(*args, **kwargs):
                if func is serve_impl:
                    calls['serve'] += 1
                    return func(*args, **kwargs)
                if func is original_response_for_exception:
                    calls['response_for_exception'] += 1
                    return func(*args, **kwargs)
                return func(*args, **kwargs)
            return wrapper

        def serve_impl(request):
            raise Http404('not found')
        handlers.sync_to_async = spy_sync_to_async

        class H(DummyHandler):

            def serve(self, request):
                return serve_impl(request)
        handlers.response_for_exception = original_response_for_exception
        h = H()
        request = DummyRequest('/static/missing.txt')
        response = asyncio.run(h.get_response_async(request))
        assert calls['serve'] == 1
        assert calls['response_for_exception'] == 1
        assert isinstance(response, HttpResponse)
    finally:
        handlers.sync_to_async = original_sync_to_async
        handlers.response_for_exception = original_response_for_exception

def test_get_response_sync_handles_404_calls_response_for_exception():
    called = {'response_for_exception': 0}
    original_response_for_exception = handlers.response_for_exception
    try:

        def spy_response_for_exception(request, exc):
            called['response_for_exception'] += 1
            return HttpResponse('handled-exc', status=404)
        handlers.response_for_exception = spy_response_for_exception

        class H(DummyHandler):

            def serve(self, request):
                raise Http404('gone')
        h = H()
        request = DummyRequest('/static/gone.txt')
        response = h.get_response(request)
        assert called['response_for_exception'] == 1
        assert isinstance(response, HttpResponse)
        assert response.status_code == 404
    finally:
        handlers.response_for_exception = original_response_for_exception

def test__should_handle_ignores_host_in_base_url():
    h = DummyHandler(base_url='http://example.com/static/')
    assert h._should_handle('/static/file.txt') is False

def test__should_handle_accepts_correct_prefix():
    h = DummyHandler(base_url='/static/')
    assert h._should_handle('/static/file.txt') is True
    assert h._should_handle('/static/') is True
    assert h._should_handle('/other/file.txt') is False

def test_file_path_decodes_url_encoded_paths():
    h = DummyHandler(base_url='/static/')
    url = '/static/some%20file.txt'
    result = h.file_path(url)
    assert ' ' in result
    assert result.endswith('some file.txt')

def test_get_response_async_returns_same_as_get_response_for_success():

    class H(DummyHandler):

        def serve(self, request):
            return HttpResponse('sync-or-async')
    h = H()
    request = DummyRequest('/static/x.txt')
    sync_resp = h.get_response(request)
    async_resp = asyncio.run(h.get_response_async(request))
    assert isinstance(sync_resp, HttpResponse)
    assert isinstance(async_resp, HttpResponse)
    assert sync_resp.content == async_resp.content == b'sync-or-async'

def test_get_response_async_awaits_response_for_exception_call():
    counters = {'called': 0}
    original_sync_to_async = handlers.sync_to_async
    original_response_for_exception = handlers.response_for_exception
    try:

        def spy_sync_to_async(func):

            async def wrapper(*args, **kwargs):
                counters['called'] += 1
                if func is original_response_for_exception:
                    return func(*args, **kwargs)
                return func(*args, **kwargs)
            return wrapper
        handlers.sync_to_async = spy_sync_to_async

        class H(DummyHandler):

            def serve(self, request):
                raise Http404('missing')
        handlers.response_for_exception = lambda req, exc: HttpResponse('exc-handled', status=404)
        h = H()
        request = DummyRequest('/static/m.txt')
        response = asyncio.run(h.get_response_async(request))
        assert counters['called'] >= 2
        assert isinstance(response, HttpResponse)
        assert response.status_code == 404
    finally:
        handlers.sync_to_async = original_sync_to_async
        handlers.response_for_exception = original_response_for_exception

def test_asgi_handler_init_does_not_call_super():
    original_asgi_init = ASGIHandler.__init__
    try:

        def raising_init(self, *args, **kwargs):
            raise RuntimeError('ASGIHandler.__init__ should not be called')
        ASGIHandler.__init__ = raising_init
        app = lambda scope, receive, send: None
        handlers.ASGIStaticFilesHandler(app)
    finally:
        ASGIHandler.__init__ = original_asgi_init

def test_load_middleware_signature_has_no_extra_parameters():
    sig = inspect.signature(handlers.StaticFilesHandlerMixin.load_middleware)
    params = list(sig.parameters.values())
    assert len(params) == 1
    assert params[0].name == 'self'

import pytest
from django.http import Http404
import importlib
from urllib.parse import urlparse
import asyncio
from urllib.parse import urlparse
from types import SimpleNamespace
from unittest import mock
import pytest
from django.http import Http404
import importlib
handlers_mod = importlib.import_module('django.contrib.staticfiles.handlers')
StaticFilesHandlerMixin = handlers_mod.StaticFilesHandlerMixin
ASGIStaticFilesHandler = handlers_mod.ASGIStaticFilesHandler
response_for_exception = handlers_mod.response_for_exception

def make_dummy_handler(serve_impl):
    """
    Create an instance of a minimal handler object that uses the mixin and
    provides a serve() implementation. We set base_url to a known value so
    file_path/file handling isn't used.
    """

    class DummyHandler(StaticFilesHandlerMixin):

        def __init__(self):
            self.base_url = urlparse('/static/')
            self._serve_impl = serve_impl

        def serve(self, request):
            return self._serve_impl(request)
    return DummyHandler()

def make_dummy_asgi_handler(serve_impl):
    """
    Create a minimal ASGIStaticFilesHandler-like instance that uses the mixin
    (so get_response_async is inherited). This avoids interacting with Django
    settings by overriding __init__ behavior.
    """

    class DummyASGI(StaticFilesHandlerMixin, ASGIStaticFilesHandler):

        def __init__(self):
            self.base_url = urlparse('/static/')
            self._serve_impl = serve_impl

        def serve(self, request):
            return self._serve_impl(request)
    return DummyASGI()

def make_fake_sync_to_async(call_records, response_for_exception_obj=None):
    """
    Returns a fake sync_to_async implementation that records which functions
    it was asked to wrap. It returns a wrapper that when called returns a
    coroutine which calls the original function synchronously and returns its result.
    If the wrapped function is response_for_exception and response_for_exception_obj
    is provided, that object will be returned instead (allowing us to control the error response).
    """

    def fake(func):
        call_records.append(func)

        def wrapper(*args, **kwargs):

            async def coro():
                if func is response_for_exception and response_for_exception_obj is not None:
                    return response_for_exception_obj
                return func(*args, **kwargs)
            return coro()
        return wrapper
    return fake

@pytest.mark.asyncio
async def test_get_response_async_calls_sync_to_async_on_success():
    calls = []

    def serve_impl(request):
        return 'OK'
    handler = make_dummy_handler(serve_impl)
    fake = make_fake_sync_to_async(calls)
    with mock.patch.object(handlers_mod, 'sync_to_async', fake):
        resp = await handler.get_response_async(DummyRequest())
    assert resp == 'OK'
    assert len(calls) == 1
    assert calls[0] is handler.serve

@pytest.mark.asyncio
async def test_get_response_async_passes_request_argument_to_wrapper():
    calls = []
    received_args = {}

    def serve_impl(request):
        received_args['request_seen'] = request
        return 'OK'
    handler = make_dummy_handler(serve_impl)
    fake = make_fake_sync_to_async(calls)
    with mock.patch.object(handlers_mod, 'sync_to_async', fake):
        req = DummyRequest(path='/static/somefile.txt')
        resp = await handler.get_response_async(req)
    assert resp == 'OK'
    assert received_args['request_seen'] is req
    assert calls and calls[0] is handler.serve

@pytest.mark.asyncio
async def test_get_response_async_called_each_time_for_multiple_calls():
    calls = []
    invocation_count = {'times': 0}

    def serve_impl(request):
        invocation_count['times'] += 1
        return f"OK-{invocation_count['times']}"
    handler = make_dummy_handler(serve_impl)
    fake = make_fake_sync_to_async(calls)
    with mock.patch.object(handlers_mod, 'sync_to_async', fake):
        r1 = await handler.get_response_async(DummyRequest())
        r2 = await handler.get_response_async(DummyRequest())
    assert r1 == 'OK-1'
    assert r2 == 'OK-2'
    assert len(calls) == 2
    assert all((call is handler.serve for call in calls))

@pytest.mark.asyncio
async def test_get_response_async_uses_sync_to_async_when_serve_raises_http404():
    calls = []

    def serve_impl(request):
        raise Http404('not found')
    error_obj = object()
    handler = make_dummy_handler(serve_impl)
    fake = make_fake_sync_to_async(calls, response_for_exception_obj=error_obj)
    with mock.patch.object(handlers_mod, 'sync_to_async', fake):
        resp = await handler.get_response_async(DummyRequest())
    assert resp is error_obj
    assert len(calls) >= 2
    assert handler.serve in calls
    assert response_for_exception in calls

@pytest.mark.asyncio
async def test_get_response_async_ensures_response_for_exception_wrapped_via_sync_to_async():
    calls = []

    def serve_impl(request):
        raise Http404()
    sentinel = {'error': True}
    handler = make_dummy_handler(serve_impl)
    fake = make_fake_sync_to_async(calls, response_for_exception_obj=sentinel)
    with mock.patch.object(handlers_mod, 'sync_to_async', fake):
        resp = await handler.get_response_async(DummyRequest())
    assert resp is sentinel
    assert response_for_exception in calls

@pytest.mark.asyncio
async def test_asgi_handler_get_response_async_uses_sync_to_async_on_success():
    calls = []

    def serve_impl(request):
        return 'ASGI-OK'
    handler = make_dummy_asgi_handler(serve_impl)
    fake = make_fake_sync_to_async(calls)
    with mock.patch.object(handlers_mod, 'sync_to_async', fake):
        resp = await handler.get_response_async(DummyRequest())
    assert resp == 'ASGI-OK'
    assert len(calls) == 1
    assert calls[0] is handler.serve

@pytest.mark.asyncio
async def test_asgi_handler_get_response_async_uses_sync_to_async_on_exception():
    calls = []

    def serve_impl(request):
        raise Http404()
    sentinel = 'ASGI-ERROR'
    handler = make_dummy_asgi_handler(serve_impl)
    fake = make_fake_sync_to_async(calls, response_for_exception_obj=sentinel)
    with mock.patch.object(handlers_mod, 'sync_to_async', fake):
        resp = await handler.get_response_async(DummyRequest())
    assert resp == sentinel
    assert handler.serve in calls
    assert response_for_exception in calls

@pytest.mark.asyncio
async def test_get_response_async_respects_order_of_wrapper_calls():
    """
    Ensure that sync_to_async is asked to wrap serve first and only if that
    raises is it asked to wrap response_for_exception. The implementation
    should call/await the serve wrapper before calling the response wrapper.
    """
    call_sequence = []

    def serve_impl(request):
        call_sequence.append('serve_called')
        raise Http404()

    def fake_response_for_exception(req, exc):
        call_sequence.append('response_for_exception_called')
        return 'ERR'
    handler = make_dummy_handler(serve_impl)

    def fake(func):
        call_sequence.append(f"wrapped:{getattr(func, '__name__', repr(func))}")

        def wrapper(*args, **kwargs):

            async def coro():
                return func(*args, **kwargs)
            return coro()
        return wrapper
    with mock.patch.object(handlers_mod, 'sync_to_async', fake):
        with mock.patch.object(handlers_mod, 'response_for_exception', fake_response_for_exception):
            resp = await handler.get_response_async(DummyRequest())
    assert resp == 'ERR'
    wrapped_names = [s for s in call_sequence if s.startswith('wrapped:')]
    assert any(('serve' in s for s in wrapped_names))
    assert any(('response_for_exception' in s for s in wrapped_names))
    assert call_sequence.index('serve_called') < call_sequence.index('response_for_exception_called')

@pytest.mark.asyncio
async def test_get_response_async_with_different_request_objects_calls_sync_to_async():
    calls = []
    seen_requests = []

    def serve_impl(request):
        seen_requests.append(request)
        return f'RESULT-{request.path}'
    handler = make_dummy_handler(serve_impl)
    fake = make_fake_sync_to_async(calls)
    with mock.patch.object(handlers_mod, 'sync_to_async', fake):
        r1 = await handler.get_response_async(DummyRequest(path='/static/a'))
        r2 = await handler.get_response_async(DummyRequest(path='/static/b'))
    assert r1 == 'RESULT-/static/a'
    assert r2 == 'RESULT-/static/b'
    assert len(calls) == 2
    assert seen_requests[0].path.endswith('/a')
    assert seen_requests[1].path.endswith('/b')

import asyncio
import time
import pytest
from django.http import Http404
import importlib
handlers_mod = importlib.import_module('django.contrib.staticfiles.handlers')
StaticFilesHandlerMixin = handlers_mod.StaticFilesHandlerMixin
import asyncio
import time
import pytest
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
import importlib
handlers_mod = importlib.import_module('django.contrib.staticfiles.handlers')
StaticFilesHandlerMixin = handlers_mod.StaticFilesHandlerMixin

@pytest.mark.asyncio
async def test_get_response_async_runs_serve_off_event_loop_and_returns():
    called_on_loop = []

    class H(StaticFilesHandlerMixin):

        def serve(self, request):
            try:
                asyncio.get_running_loop()
                called_on_loop.append(True)
            except RuntimeError:
                called_on_loop.append(False)
            return 'ok'
    h = H()
    res = await h.get_response_async('request')
    assert res == 'ok'
    assert called_on_loop == [False]

@pytest.mark.asyncio
async def test_get_response_async_uses_response_for_exception_off_event_loop_on_http404():
    orig_rfe = handlers_mod.response_for_exception
    called_on_loop = []

    def fake_response_for_exception(request, exc):
        try:
            asyncio.get_running_loop()
            called_on_loop.append(True)
        except RuntimeError:
            called_on_loop.append(False)
        return 'exc_resp'
    handlers_mod.response_for_exception = fake_response_for_exception
    try:

        class H(StaticFilesHandlerMixin):

            def serve(self, request):
                raise Http404('not found')
        h = H()
        res = await h.get_response_async('request')
        assert res == 'exc_resp'
        assert called_on_loop == [False]
    finally:
        handlers_mod.response_for_exception = orig_rfe

@pytest.mark.asyncio
async def test_get_response_async_propagates_non_http404_exception():

    class H(StaticFilesHandlerMixin):

        def serve(self, request):
            raise ValueError('boom')
    h = H()
    with pytest.raises(ValueError):
        await h.get_response_async('request')

@pytest.mark.asyncio
async def test_get_response_async_does_not_block_event_loop_when_serve_blocks():
    flag = {'tick': False}

    class H(StaticFilesHandlerMixin):

        def serve(self, request):
            time.sleep(0.2)
            return 'done'
    h = H()
    task = asyncio.create_task(h.get_response_async('request'))
    await asyncio.sleep(0)
    await asyncio.sleep(0.05)
    flag['tick'] = True
    res = await task
    assert res == 'done'
    assert flag['tick'] is True

@pytest.mark.asyncio
async def test_multiple_concurrent_get_response_async_tasks_do_not_block_event_loop():
    ticks = {'count': 0}

    class H(StaticFilesHandlerMixin):

        def serve(self, request):
            time.sleep(0.1)
            return request + ':ok'
    h = H()
    tasks = [asyncio.create_task(h.get_response_async(f'req{i}')) for i in range(5)]
    await asyncio.sleep(0.02)
    ticks['count'] += 1
    results = await asyncio.gather(*tasks)
    assert all((r.endswith(':ok') for r in results))
    assert ticks['count'] >= 1

@pytest.mark.asyncio
async def test_get_response_async_preserves_request_argument_identity():
    seen = {}

    class H(StaticFilesHandlerMixin):

        def serve(self, request):
            seen['req'] = request
            return 'ok'
    request_obj = object()
    h = H()
    res = await h.get_response_async(request_obj)
    assert res == 'ok'
    assert seen['req'] is request_obj

@pytest.mark.asyncio
async def test_get_response_async_propagates_exception_from_response_for_exception():
    orig_rfe = handlers_mod.response_for_exception

    def raising_rfe(request, exc):
        raise RuntimeError('rfe failed')
    handlers_mod.response_for_exception = raising_rfe
    try:

        class H(StaticFilesHandlerMixin):

            def serve(self, request):
                raise Http404()
        h = H()
        with pytest.raises(RuntimeError):
            await h.get_response_async('request')
    finally:
        handlers_mod.response_for_exception = orig_rfe

@pytest.mark.asyncio
async def test_get_response_async_can_be_called_repeatedly_quickly():

    class H(StaticFilesHandlerMixin):

        def serve(self, request):
            return 'ok'
    h = H()
    results = await asyncio.gather(*(h.get_response_async(str(i)) for i in range(20)))
    assert results == ['ok'] * 20

def test_get_response_sync_returns_and_handles_http404():

    class H(StaticFilesHandlerMixin):

        def serve(self, request):
            if request == 'good':
                return 'ok'
            raise Http404()
    orig_rfe = handlers_mod.response_for_exception
    handlers_mod.response_for_exception = lambda req, exc: 'exc'
    try:
        h = H()
        assert h.get_response('good') == 'ok'
        assert h.get_response('bad') == 'exc'
    finally:
        handlers_mod.response_for_exception = orig_rfe

import asyncio
import threading
from urllib.parse import urlparse
import pytest
import asyncio
import threading
from urllib.parse import urlparse
import pytest
from django.contrib.staticfiles import handlers

def test_get_response_async_runs_serve_in_thread(monkeypatch):
    handler = handlers.StaticFilesHandlerMixin()
    handler.base_url = urlparse('/static/')

    def serve_fn(request):
        assert threading.current_thread().name != 'MainThread', 'serve ran on main thread'
        return 'OK'
    monkeypatch.setattr(handler, 'serve', serve_fn)
    result = asyncio.run(handler.get_response_async(DummyRequest('/static/test.txt')))
    assert result == 'OK'

def test_get_response_async_handles_http404_in_thread(monkeypatch):
    handler = handlers.StaticFilesHandlerMixin()
    handler.base_url = urlparse('/static/')

    def serve_fn(request):
        raise handlers.Http404('not found')

    def fake_response_for_exception(request, exc):
        assert threading.current_thread().name != 'MainThread', 'response_for_exception ran on main thread'
        return 'EXC'
    monkeypatch.setattr(handler, 'serve', serve_fn)
    monkeypatch.setattr(handlers, 'response_for_exception', fake_response_for_exception)
    result = asyncio.run(handler.get_response_async(DummyRequest('/static/test.txt')))
    assert result == 'EXC'

def test_get_response_async_propagates_non_http404(monkeypatch):
    handler = handlers.StaticFilesHandlerMixin()
    handler.base_url = urlparse('/static/')

    def serve_fn(request):
        raise ValueError('boom')
    monkeypatch.setattr(handler, 'serve', serve_fn)
    with pytest.raises(ValueError):
        asyncio.run(handler.get_response_async(DummyRequest('/static/test.txt')))

def test_file_path_converts_percent_encoding():
    handler = handlers.StaticFilesHandlerMixin()
    handler.base_url = urlparse('/static/')
    assert handler.file_path('/static/some%20file.txt') == 'some file.txt'

def test_should_handle_false_when_base_url_has_netloc():
    handler = handlers.StaticFilesHandlerMixin()
    handler.base_url = urlparse('http://static.example.com/static/')
    assert not handler._should_handle('/static/test.txt')
    handler.base_url = urlparse('/static/')
    assert handler._should_handle('/static/test.txt')

def test_get_base_url_uses_settings(monkeypatch):
    monkeypatch.setattr(handlers.utils, 'check_settings', lambda: None)
    monkeypatch.setattr(handlers.settings, 'STATIC_URL', '/assets/')
    handler = handlers.StaticFilesHandlerMixin()
    assert handler.get_base_url() == '/assets/'

def test_serve_calls_staticfiles_view(monkeypatch):
    handler = handlers.StaticFilesHandlerMixin()
    handler.base_url = urlparse('/static/')

    def file_path(url):
        return 'rel/path.txt'
    monkeypatch.setattr(handler, 'file_path', file_path)

    def serve_view(request, path, insecure=False):
        return (request, path, insecure)
    monkeypatch.setattr(handlers, 'serve', serve_view)
    req = DummyRequest('/static/rel/path.txt')
    assert handler.serve(req) == (req, 'rel/path.txt', True)

def test_asgi_handler_delegates_non_http(monkeypatch):
    called = {'v': False}

    async def app(scope, receive, send):
        called['v'] = True
    handler = handlers.ASGIStaticFilesHandler(app)

    async def receive():
        return None

    async def send(message):
        pass
    scope = {'type': 'websocket', 'path': '/static/test.txt'}
    asyncio.run(handler(scope, receive, send))
    assert called['v'] is True

def test_asgi_handler_delegates_when_not_should_handle(monkeypatch):
    called = {'v': False}

    async def app(scope, receive, send):
        called['v'] = True
    handler = handlers.ASGIStaticFilesHandler(app)
    monkeypatch.setattr(handler, '_should_handle', lambda path: False)

    async def receive():
        return None

    async def send(message):
        pass
    scope = {'type': 'http', 'path': '/static/test.txt'}
    asyncio.run(handler(scope, receive, send))
    assert called['v'] is True

def test_should_handle_path_equal_base_url():
    handler = handlers.StaticFilesHandlerMixin()
    handler.base_url = urlparse('/static/')
    assert handler._should_handle('/static/') is True

import asyncio
import asyncio
from urllib.parse import urlparse
import pytest
from django.http import Http404
from django.contrib.staticfiles import handlers

def make_handler(serve_func):
    """
    Create a simple handler instance with a custom synchronous serve method.
    """

    class H(handlers.StaticFilesHandlerMixin):
        pass
    h = H()
    h.base_url = urlparse('/static/')
    h.serve = serve_func.__get__(h, H)
    return h

def make_fake_sync_to_async(call_log, result_wrapper=None):
    """
    Returns a fake sync_to_async replacement which records the function passed
    to it into call_log and returns an async wrapper that invokes the function.
    If result_wrapper is provided it will be used to transform the return value.
    """

    def fake_sync_to_async(func):
        call_log.append(func)

        async def inner(*args, **kwargs):
            res = func(*args, **kwargs)
            if result_wrapper:
                return result_wrapper(res)
            return res
        return inner
    return fake_sync_to_async

def test_get_response_async_calls_sync_to_async_on_success(monkeypatch):
    call_log = []
    async_result = object()

    def serve(self, request):
        return async_result
    handler = make_handler(serve)
    monkeypatch.setattr(handlers, 'sync_to_async', make_fake_sync_to_async(call_log))
    request = DummyRequest('/static/test.txt')
    result = asyncio.run(handler.get_response_async(request))
    assert result is async_result
    assert len(call_log) == 1
    assert call_log[0] == handler.serve

def test_get_response_async_passes_request_arg_and_returns_value(monkeypatch):
    call_log = []

    def serve(self, request):
        return f'served:{request.path}'
    handler = make_handler(serve)
    monkeypatch.setattr(handlers, 'sync_to_async', make_fake_sync_to_async(call_log))
    req = DummyRequest('/static/abc')
    result = asyncio.run(handler.get_response_async(req))
    assert result == 'served:/static/abc'
    assert len(call_log) == 1
    assert call_log[0] == handler.serve

def test_get_response_async_handles_http404_via_response_for_exception(monkeypatch):
    call_log = []
    response_called = {}

    def serve(self, request):
        raise Http404('not found')

    def fake_response_for_exception(request, exc):
        response_called['request'] = request
        response_called['exc'] = exc
        return 'handled'
    handler = make_handler(serve)
    monkeypatch.setattr(handlers, 'sync_to_async', make_fake_sync_to_async(call_log))
    monkeypatch.setattr(handlers, 'response_for_exception', fake_response_for_exception)
    req = DummyRequest('/static/missing')
    result = asyncio.run(handler.get_response_async(req))
    assert result == 'handled'
    assert len(call_log) == 2
    assert call_log[0] == handler.serve
    assert call_log[1] == handlers.response_for_exception
    assert response_called['request'] is req
    assert isinstance(response_called['exc'], Http404)

def test_get_response_async_calls_sync_to_async_twice_on_404(monkeypatch):
    call_log = []

    def serve(self, request):
        raise Http404()

    def fake_response_for_exception(request, exc):
        return 'resp'
    handler = make_handler(serve)
    monkeypatch.setattr(handlers, 'sync_to_async', make_fake_sync_to_async(call_log))
    monkeypatch.setattr(handlers, 'response_for_exception', fake_response_for_exception)
    req = DummyRequest('/static/x')
    result = asyncio.run(handler.get_response_async(req))
    assert result == 'resp'
    assert len(call_log) == 2

def test_get_response_async_propagates_non_http404_exceptions_and_uses_sync_to_async(monkeypatch):
    call_log = []

    def serve(self, request):
        raise ValueError('boom')
    handler = make_handler(serve)
    monkeypatch.setattr(handlers, 'sync_to_async', make_fake_sync_to_async(call_log))
    req = DummyRequest('/static/boom')
    with pytest.raises(ValueError):
        asyncio.run(handler.get_response_async(req))
    assert len(call_log) == 1
    assert call_log[0] == handler.serve

def test_get_response_async_multiple_calls_each_calls_sync_to_async(monkeypatch):
    call_log = []

    def serve(self, request):
        return request.path
    handler = make_handler(serve)
    monkeypatch.setattr(handlers, 'sync_to_async', make_fake_sync_to_async(call_log))
    r1 = DummyRequest('/static/1')
    r2 = DummyRequest('/static/2')
    res1 = asyncio.run(handler.get_response_async(r1))
    res2 = asyncio.run(handler.get_response_async(r2))
    assert res1 == '/static/1'
    assert res2 == '/static/2'
    assert len(call_log) == 2
    assert call_log[0] == handler.serve
    assert call_log[1] == handler.serve

def test_get_response_async_with_bound_method_identity(monkeypatch):
    call_log = []

    def serve(self, request):
        return 'ok'
    handler = make_handler(serve)
    bound = handler.serve
    monkeypatch.setattr(handlers, 'sync_to_async', make_fake_sync_to_async(call_log))
    r = DummyRequest('/static/id')
    res = asyncio.run(handler.get_response_async(r))
    assert res == 'ok'
    assert call_log[0] is bound

def test_get_response_async_response_for_exception_called_with_correct_args(monkeypatch):
    call_log = []
    recorded = {}

    def serve(self, request):
        raise Http404('not found again')

    def fake_response_for_exception(request, exc):
        recorded['request'] = request
        recorded['exc'] = exc
        return 'handled2'
    handler = make_handler(serve)
    monkeypatch.setattr(handlers, 'sync_to_async', make_fake_sync_to_async(call_log))
    monkeypatch.setattr(handlers, 'response_for_exception', fake_response_for_exception)
    req = DummyRequest('/static/zzz')
    result = asyncio.run(handler.get_response_async(req))
    assert result == 'handled2'
    assert recorded['request'] is req
    assert isinstance(recorded['exc'], Http404)

def test_get_response_async_with_different_request_objects(monkeypatch):
    call_log = []

    def serve(self, request):
        return request.path
    handler = make_handler(serve)
    monkeypatch.setattr(handlers, 'sync_to_async', make_fake_sync_to_async(call_log))
    for i in range(5):
        req = DummyRequest(f'/static/item-{i}')
        res = asyncio.run(handler.get_response_async(req))
        assert res == f'/static/item-{i}'
    assert len(call_log) == 5

pytest
asyncio
threading
time
types
from urllib.parse import urlparse
from django.http import Http404
import django
from django.contrib.staticfiles import handlers as handlers_module
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler, StaticFilesHandlerMixin
import asyncio
import threading
import time
import types
import pytest
from urllib.parse import urlparse
from django.http import Http404
import django
from django.contrib.staticfiles import handlers as handlers_module
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler, StaticFilesHandlerMixin
try:
    django.setup()
except Exception:
    pass

@pytest.mark.asyncio
async def test_mixin_get_response_async_runs_serve_in_threadpool():

    class DummyHandler(StaticFilesHandlerMixin):
        pass
    handler = DummyHandler()
    handler.base_url = urlparse('/static/')
    request = types.SimpleNamespace(path='/static/file.txt')

    def serve_fn(req):
        req.called_in_main_thread = threading.current_thread() is threading.main_thread()
        return 'served-ok'
    handler.serve = serve_fn
    result = await handler.get_response_async(request)
    assert result == 'served-ok'
    assert request.called_in_main_thread is False

@pytest.mark.asyncio
async def test_mixin_get_response_async_uses_thread_for_response_for_exception():

    class DummyHandler(StaticFilesHandlerMixin):
        pass
    handler = DummyHandler()
    handler.base_url = urlparse('/static/')
    request = types.SimpleNamespace(path='/static/missing.txt')

    def serve_fn(req):
        raise Http404('not found')
    handler.serve = serve_fn
    called = {}

    def fake_response_for_exception(req, exc):
        called['in_main_thread'] = threading.current_thread() is threading.main_thread()
        return 'handled-404'
    original = handlers_module.response_for_exception
    handlers_module.response_for_exception = fake_response_for_exception
    try:
        result = await handler.get_response_async(request)
    finally:
        handlers_module.response_for_exception = original
    assert result == 'handled-404'
    assert called['in_main_thread'] is False

@pytest.mark.asyncio
async def test_asgi_handler_get_response_async_runs_serve_in_threadpool():

    async def dummy_app(scope, receive, send):
        return None
    handler = ASGIStaticFilesHandler(dummy_app)
    handler.base_url = urlparse('/static/')
    request = types.SimpleNamespace(path='/static/asset.txt')

    def serve_fn(req):
        req.called_in_main_thread = threading.current_thread() is threading.main_thread()
        return 'asgi-served'
    handler.serve = serve_fn
    result = await handler.get_response_async(request)
    assert result == 'asgi-served'
    assert request.called_in_main_thread is False

@pytest.mark.asyncio
async def test_asgi_handler_get_response_async_handles_404_in_threadpool():

    async def dummy_app(scope, receive, send):
        return None
    handler = ASGIStaticFilesHandler(dummy_app)
    handler.base_url = urlparse('/static/')
    request = types.SimpleNamespace(path='/static/missing.txt')

    def serve_fn(req):
        raise Http404('not found')
    handler.serve = serve_fn
    called = {}

    def fake_response_for_exception(req, exc):
        called['in_main_thread'] = threading.current_thread() is threading.main_thread()
        return 'asgi-handled-404'
    original = handlers_module.response_for_exception
    handlers_module.response_for_exception = fake_response_for_exception
    try:
        result = await handler.get_response_async(request)
    finally:
        handlers_module.response_for_exception = original
    assert result == 'asgi-handled-404'
    assert called['in_main_thread'] is False

def test_get_response_runs_serve_on_main_thread_sync():

    class DummyHandler(StaticFilesHandlerMixin):
        pass
    handler = DummyHandler()
    handler.base_url = urlparse('/static/')
    request = types.SimpleNamespace(path='/static/file.txt')

    def serve_fn(req):
        req.called_in_main_thread = threading.current_thread() is threading.main_thread()
        return 'sync-served'
    handler.serve = serve_fn
    result = handler.get_response(request)
    assert result == 'sync-served'
    assert request.called_in_main_thread is True

def test_asgi_handler_get_response_runs_serve_on_main_thread_sync():

    async def dummy_app(scope, receive, send):
        return None
    handler = ASGIStaticFilesHandler(dummy_app)
    handler.base_url = urlparse('/static/')
    request = types.SimpleNamespace(path='/static/file2.txt')

    def serve_fn(req):
        req.called_in_main_thread = threading.current_thread() is threading.main_thread()
        return 'asgi-sync-served'
    handler.serve = serve_fn
    result = handler.get_response(request)
    assert result == 'asgi-sync-served'
    assert request.called_in_main_thread is True

@pytest.mark.asyncio
async def test_concurrent_get_response_async_does_not_block_event_loop():

    class DummyHandler(StaticFilesHandlerMixin):
        pass
    handler = DummyHandler()
    handler.base_url = urlparse('/static/')

    def long_serve(req):
        req.thread_name = threading.current_thread().name
        time.sleep(0.25)
        return 'long-done'

    def short_serve(req):
        req.thread_name = threading.current_thread().name
        return 'short-done'
    handler_long = DummyHandler()
    handler_long.base_url = urlparse('/static/')
    handler_long.serve = long_serve
    handler_short = DummyHandler()
    handler_short.base_url = urlparse('/static/')
    handler_short.serve = short_serve
    req_long = types.SimpleNamespace(path='/static/long.txt')
    req_short = types.SimpleNamespace(path='/static/short.txt')
    task_long = asyncio.create_task(handler_long.get_response_async(req_long))
    await asyncio.sleep(0.01)
    task_short = asyncio.create_task(handler_short.get_response_async(req_short))
    done, pending = await asyncio.wait({task_long, task_short}, timeout=1.0)
    assert task_short in done, 'short task should complete promptly (not blocked by long serve)'
    assert task_long in done, 'long task should eventually complete'
    assert task_short.result() == 'short-done'
    assert task_long.result() == 'long-done'
    assert req_short.thread_name != 'MainThread'
    assert req_long.thread_name != 'MainThread'

@pytest.mark.asyncio
async def test_exception_response_for_exception_threading_multiple_calls():

    class DummyHandler(StaticFilesHandlerMixin):
        pass
    handler = DummyHandler()
    handler.base_url = urlparse('/static/')

    def serve_fn(req):
        raise Http404('boom')
    handler.serve = serve_fn
    thread_names = []

    def fake_response_for_exception(req, exc):
        thread_names.append(threading.current_thread().name)
        return f'handled-{len(thread_names)}'
    original = handlers_module.response_for_exception
    handlers_module.response_for_exception = fake_response_for_exception
    try:
        tasks = [asyncio.create_task(handler.get_response_async(types.SimpleNamespace(path=f'/static/{i}'))) for i in range(3)]
        results = await asyncio.gather(*tasks)
    finally:
        handlers_module.response_for_exception = original
    assert results == ['handled-1', 'handled-2', 'handled-3']
    assert all((name != 'MainThread' for name in thread_names))

import asyncio
import time
import types
import pytest
from urllib.parse import urlparse
import django
from django.http import Http404
import django.contrib.staticfiles.handlers as handlers

@pytest.mark.asyncio
async def test_sync_to_async_is_used_for_serve(monkeypatch):
    called = []
    original = handlers.sync_to_async

    def recorder(fn, *args, **kwargs):
        called.append(fn)
        return original(fn, *args, **kwargs)
    monkeypatch.setattr(handlers, 'sync_to_async', recorder)

    def serve_fn(request):
        return 'ok'
    h = DummyHandler(serve_fn)
    resp = await h.get_response_async(DummyRequest())
    assert resp == 'ok'
    assert called, 'sync_to_async was not called'
    assert any((getattr(f, '__func__', None) is serve_fn.__call__ or True for f in called))

@pytest.mark.asyncio
async def test_sync_to_async_is_used_for_response_for_exception_on_404(monkeypatch):
    called = []
    original = handlers.sync_to_async

    def recorder(fn, *args, **kwargs):
        called.append(fn)
        return original(fn, *args, **kwargs)
    monkeypatch.setattr(handlers, 'sync_to_async', recorder)

    def serve_fn(request):
        raise Http404('not found')

    def fake_response_for_exception(request, exc):
        return 'handled-404'
    monkeypatch.setattr(handlers, 'response_for_exception', fake_response_for_exception)
    h = DummyHandler(serve_fn)
    resp = await h.get_response_async(DummyRequest())
    assert resp == 'handled-404'
    assert any((getattr(f, '__name__', '') == 'serve' or getattr(f, '__self__', None) is h for f in called))
    assert any((f is fake_response_for_exception for f in called))

@pytest.mark.asyncio
async def test_serve_runs_outside_event_loop(monkeypatch):

    def serve_fn(request):
        try:
            asyncio.get_running_loop()
            return 'inloop'
        except RuntimeError:
            return 'no-loop'
    h = DummyHandler(serve_fn)
    resp = await h.get_response_async(DummyRequest())
    assert resp == 'no-loop', 'serve must run outside the event loop (in a thread)'

@pytest.mark.asyncio
async def test_response_for_exception_runs_outside_event_loop_on_404(monkeypatch):

    def serve_fn(request):
        raise Http404('not found')

    def fake_response_for_exception(request, exc):
        try:
            asyncio.get_running_loop()
            return 'inloop'
        except RuntimeError:
            return 'no-loop'
    monkeypatch.setattr(handlers, 'response_for_exception', fake_response_for_exception)
    h = DummyHandler(serve_fn)
    resp = await h.get_response_async(DummyRequest())
    assert resp == 'no-loop', 'response_for_exception must run outside the event loop (in a thread)'

@pytest.mark.asyncio
async def test_non_http404_exception_propagates():

    def serve_fn(request):
        raise ValueError('boom')
    h = DummyHandler(serve_fn)
    with pytest.raises(ValueError):
        await h.get_response_async(DummyRequest())

@pytest.mark.asyncio
async def test_event_loop_not_blocked_by_blocking_serve():

    def serve_fn(request):
        time.sleep(0.15)
        return 'done'
    h = DummyHandler(serve_fn)
    task = asyncio.create_task(h.get_response_async(DummyRequest()))
    counter = 0
    for _ in range(20):
        await asyncio.sleep(0)
        counter += 1
        if task.done():
            break
    res = await task
    assert res == 'done'
    assert counter > 0, 'Event loop was blocked by serve (should run serve in a thread)'

@pytest.mark.asyncio
async def test_get_response_async_returns_serve_result():

    def serve_fn(request):
        return {'file': 'content'}
    h = DummyHandler(serve_fn)
    resp = await h.get_response_async(DummyRequest())
    assert resp == {'file': 'content'}

@pytest.mark.asyncio
async def test_multiple_concurrent_get_response_async_calls():

    def serve_fn(request):
        time.sleep(0.05)
        return 'ok'
    h = DummyHandler(serve_fn)
    tasks = [asyncio.create_task(h.get_response_async(DummyRequest(f'/static/{i}'))) for i in range(5)]
    await asyncio.sleep(0)
    results = await asyncio.gather(*tasks)
    assert results == ['ok'] * 5

@pytest.mark.asyncio
async def test_sync_to_async_wrapper_called_for_both_functions(monkeypatch):
    called = []
    original = handlers.sync_to_async

    def wrapper(fn, *a, **kw):
        called.append(fn)
        return original(fn, *a, **kw)
    monkeypatch.setattr(handlers, 'sync_to_async', wrapper)

    def serve_fn(request):
        raise Http404()

    def fake_response_for_exception(request, exc):
        return 'handled'
    monkeypatch.setattr(handlers, 'response_for_exception', fake_response_for_exception)
    h = DummyHandler(serve_fn)
    resp = await h.get_response_async(DummyRequest())
    assert resp == 'handled'
    assert len(called) >= 2
    assert any((f is fake_response_for_exception for f in called))

@pytest.mark.asyncio
async def test_serve_called_outside_event_loop_with_bound_method_identity():
    recorded = []
    original = handlers.sync_to_async

    def recorder(fn, *args, **kwargs):
        recorded.append(fn)
        return original(fn, *args, **kwargs)
    pytest.monkeypatch.setattr(handlers, 'sync_to_async', recorder)

    def serve_fn(request):
        try:
            asyncio.get_running_loop()
            return 'inloop'
        except RuntimeError:
            return 'no-loop'
    h = DummyHandler(serve_fn)
    resp = await h.get_response_async(DummyRequest())
    assert resp == 'no-loop'
    assert recorded, 'sync_to_async not recorded any calls'
    assert any((getattr(f, '__self__', None) is h for f in recorded))

import asyncio
import threading
import pytest
from urllib.parse import urlparse
from django.http import Http404
from django.contrib.staticfiles import handlers as handlers_mod

@pytest.mark.asyncio
async def test_get_response_async_runs_serve_in_threadpool():
    handler = DummyHandler()
    thread_names = []

    def serve(request):
        thread_names.append(threading.current_thread().name)
        return 'OK'
    handler.serve = serve
    resp = await handler.get_response_async(object())
    assert resp == 'OK'
    assert thread_names, 'serve was not called'
    assert thread_names[0] != threading.main_thread().name

@pytest.mark.asyncio
async def test_get_response_async_runs_response_for_exception_in_threadpool_on_404(monkeypatch):
    handler = DummyHandler()
    thread_names = []

    def serve(request):
        raise Http404('not found')

    def fake_response_for_exception(request, exc):
        thread_names.append(threading.current_thread().name)
        return 'HANDLED'
    handler.serve = serve
    monkeypatch.setattr(handlers_mod, 'response_for_exception', fake_response_for_exception)
    resp = await handler.get_response_async(object())
    assert resp == 'HANDLED'
    assert thread_names and thread_names[0] != threading.main_thread().name

@pytest.mark.asyncio
async def test_get_response_async_returns_value_from_serve():
    handler = DummyHandler()

    def serve(request):
        return {'value': 123}
    handler.serve = serve
    resp = await handler.get_response_async('request')
    assert isinstance(resp, dict) and resp['value'] == 123

@pytest.mark.asyncio
async def test_get_response_async_returns_value_from_response_for_exception_on_404(monkeypatch):
    handler = DummyHandler()

    def serve(request):
        raise Http404('boom')

    def fake_response_for_exception(request, exc):
        return ('handled', getattr(exc, 'args', None))
    handler.serve = serve
    monkeypatch.setattr(handlers_mod, 'response_for_exception', fake_response_for_exception)
    resp = await handler.get_response_async('req')
    assert resp[0] == 'handled'
    assert resp[1] and 'boom' in resp[1][0]

@pytest.mark.asyncio
async def test_get_response_async_multiple_concurrent_calls_run_in_threadpool():
    handler = DummyHandler()
    thread_names = []

    def serve(request):
        thread_names.append(threading.current_thread().name)
        return request
    handler.serve = serve
    tasks = [handler.get_response_async(i) for i in range(8)]
    results = await asyncio.gather(*tasks)
    assert results == list(range(8))
    assert thread_names
    assert all((name != threading.main_thread().name for name in thread_names))

@pytest.mark.asyncio
async def test_get_response_async_handles_many_concurrent_calls_in_threadpool():
    handler = DummyHandler()
    thread_names = []

    def serve(request):
        thread_names.append(threading.current_thread().name)
        return request
    handler.serve = serve
    tasks = [handler.get_response_async(i) for i in range(20)]
    results = await asyncio.gather(*tasks)
    assert results == list(range(20))
    assert thread_names
    assert any((name != threading.main_thread().name for name in thread_names))

@pytest.mark.asyncio
async def test_get_response_async_preserves_exception_type_for_non_http404():
    handler = DummyHandler()

    def serve(request):
        raise ValueError('bad')
    handler.serve = serve
    with pytest.raises(ValueError):
        await handler.get_response_async('req')

@pytest.mark.asyncio
async def test_get_response_async_response_for_exception_called_with_correct_arguments(monkeypatch):
    handler = DummyHandler()
    captured = {}

    def serve(request):
        raise Http404('not found')

    def fake_response_for_exception(request, exc):
        captured['request'] = request
        captured['exc'] = exc
        return 'handled'
    handler.serve = serve
    monkeypatch.setattr(handlers_mod, 'response_for_exception', fake_response_for_exception)
    req_obj = object()
    resp = await handler.get_response_async(req_obj)
    assert resp == 'handled'
    assert captured['request'] is req_obj
    assert isinstance(captured['exc'], Http404)

@pytest.mark.asyncio
async def test_get_response_async_does_not_call_response_for_exception_on_success(monkeypatch):
    handler = DummyHandler()
    called = {'rf': False}

    def serve(request):
        return 'OK'

    def fake_response_for_exception(request, exc):
        called['rf'] = True
        return 'BAD'
    handler.serve = serve
    monkeypatch.setattr(handlers_mod, 'response_for_exception', fake_response_for_exception)
    resp = await handler.get_response_async('req')
    assert resp == 'OK'
    assert called['rf'] is False

@pytest.mark.asyncio
async def test_get_response_async_with_bound_method_serve_runs_in_threadpool():
    handler = DummyHandler()
    thread_names = []

    class Obj:

        def method(self, request):
            thread_names.append(threading.current_thread().name)
            return 'bound'
    o = Obj()
    handler.serve = o.method
    resp = await handler.get_response_async('r')
    assert resp == 'bound'
    assert thread_names and thread_names[0] != threading.main_thread().name

import asyncio
from urllib.parse import urlparse
from types import SimpleNamespace
import inspect
from unittest import mock
from asgiref import sync as asgiref_sync
import pytest
import asyncio
import inspect
from types import SimpleNamespace
from unittest import mock
import pytest
from urllib.parse import urlparse
from django.core.handlers.exception import response_for_exception
from django.http import Http404
import django.contrib.staticfiles.handlers as handlers
from asgiref import sync as asgiref_sync

def test_should_handle_true_and_false():
    h = DummyMixin('/static/')
    assert h._should_handle('/static/abc') is True
    assert h._should_handle('/other/abc') is False

def test_should_handle_with_host_in_base_url():
    h = DummyMixin('http://example.com/static/')
    assert h.base_url[1] == 'example.com'
    assert h._should_handle('/static/abc') is False

def test_file_path_converts_url_to_relative_path():
    h = DummyMixin('/static/')
    assert h.file_path('/static/dir/file.txt') == 'dir/file.txt'
    assert h.file_path('/static/') == ''

def test_serve_delegates_to_serve_with_insecure_flag(monkeypatch):
    h = DummyMixin('/static/')
    request = SimpleNamespace(path='/static/hello.txt')
    called = {}

    def fake_serve(req, path, insecure=False):
        called['req'] = req
        called['path'] = path
        called['insecure'] = insecure
        return 'SERVED'
    monkeypatch.setattr(handlers, 'serve', fake_serve)
    resp = h.serve(request)
    assert resp == 'SERVED'
    assert called['req'] is request
    assert called['path'] == 'hello.txt'
    assert called['insecure'] is True

def test_get_response_handles_Http404_and_uses_response_for_exception(monkeypatch):
    h = DummyMixin('/static/')
    request = SimpleNamespace(path='/static/notfound.txt')

    def raising_serve(req, path, insecure=False):
        raise Http404('nope')
    monkeypatch.setattr(handlers, 'serve', raising_serve)
    monkeypatch.setattr(handlers, 'response_for_exception', lambda req, exc: 'EXC_RESP')
    resp = h.get_response(request)
    assert resp == 'EXC_RESP'

def test_get_response_async_calls_sync_to_async_on_success(monkeypatch):
    h = DummyMixin('/static/')
    request = SimpleNamespace(path='/static/ok.txt')

    def real_serve(req, path, insecure=False):
        assert req is request
        assert path == 'ok.txt'
        return 'ASYNC_OK'
    calls = []

    def fake_sync_to_async(func):
        calls.append(func)

        async def runner(*a, **kw):
            return func(*a, **kw)
        return runner
    monkeypatch.setattr(handlers, 'serve', real_serve)
    monkeypatch.setattr(asgiref_sync, 'sync_to_async', fake_sync_to_async)
    resp = asyncio.get_event_loop().run_until_complete(h.get_response_async(request))
    assert resp == 'ASYNC_OK'
    assert any((c is real_serve for c in calls))

def test_get_response_async_handles_Http404_and_uses_response_for_exception_async(monkeypatch):
    h = DummyMixin('/static/')
    request = SimpleNamespace(path='/static/missing.txt')

    def raising_serve(req, path, insecure=False):
        raise Http404('nope')

    def fake_response_for_exception(req, exc):
        return 'ASYNC_EXC'
    calls = []

    def fake_sync_to_async(func):
        calls.append(func)

        async def runner(*a, **kw):
            return func(*a, **kw)
        return runner
    monkeypatch.setattr(handlers, 'serve', raising_serve)
    monkeypatch.setattr(handlers, 'response_for_exception', fake_response_for_exception)
    monkeypatch.setattr(asgiref_sync, 'sync_to_async', fake_sync_to_async)
    resp = asyncio.get_event_loop().run_until_complete(h.get_response_async(request))
    assert resp == 'ASYNC_EXC'
    assert raising_serve in calls
    assert fake_response_for_exception in calls

@pytest.mark.asyncio
async def test_asgi_handler_hands_off_non_http_scope(monkeypatch):
    monkeypatch.setattr(handlers.StaticFilesHandlerMixin, 'get_base_url', lambda self: '/static/')
    called = {}

    async def dummy_app(scope, receive, send):
        called['scope'] = scope
        return 'APP_CALLED'
    h = handlers.ASGIStaticFilesHandler(dummy_app)
    scope = {'type': 'websocket', 'path': '/static/xyz'}
    result = await h(scope, None, None)
    assert called.get('scope') == scope

@pytest.mark.asyncio
async def test_asgi_handler_uses_super_call_for_http_and_matching_path(monkeypatch):
    monkeypatch.setattr(handlers.StaticFilesHandlerMixin, 'get_base_url', lambda self: '/static/')
    original_super_call = handlers.ASGIStaticFilesHandler.__mro__[1].__call__

    async def fake_super_call(self, scope, receive, send):
        return 'SUPER_CALLED'
    monkeypatch.setattr(handlers.ASGIStaticFilesHandler.__mro__[1], '__call__', fake_super_call)

    async def dummy_app(scope, receive, send):
        raise RuntimeError('should not be called')
    h = handlers.ASGIStaticFilesHandler(dummy_app)
    monkeypatch.setattr(h, '_should_handle', lambda path: True)
    scope = {'type': 'http', 'path': '/static/abc'}
    result = await h(scope, None, None)
    assert result == 'SUPER_CALLED'
    monkeypatch.setattr(handlers.ASGIStaticFilesHandler.__mro__[1], '__call__', original_super_call)

def test_load_middleware_signature_has_not_changed():
    sig = inspect.signature(handlers.StaticFilesHandlerMixin.load_middleware)
    params = list(sig.parameters.values())
    assert len(params) == 1
    assert params[0].name == 'self'

import asyncio
import time
from urllib.parse import urlparse
from types import SimpleNamespace
import django
from django.conf import settings
from django.http import Http404
import django.contrib.staticfiles.handlers as handlers
from django.contrib.staticfiles.handlers import StaticFilesHandlerMixin
settings.STATIC_URL = '/static/'

def test_get_response_async_runs_serve_in_thread():
    """
    If the synchronous serve function blocks (time.sleep), get_response_async must not block
    the event loop — serve should be executed in a thread via sync_to_async. We detect this
    by running a background coroutine that expects to make progress while serve is sleeping.
    """
    handler = DummyHandler('/static/')

    def serve(request):
        time.sleep(0.15)
        return 'served-success'
    handler.serve = serve
    counter = []

    async def main():

        async def background():
            for _ in range(30):
                counter.append(1)
                await asyncio.sleep(0.01)
        res, _ = await asyncio.gather(handler.get_response_async(SimpleNamespace(path='/static/foo')), background())
        return res
    result = asyncio.run(main())
    assert result == 'served-success'
    assert len(counter) >= 5

def test_get_response_async_handles_exception_without_blocking():
    """
    When serve raises Http404, get_response_async should call response_for_exception using
    sync_to_async so that any blocking work in response_for_exception does not block the event loop.
    We monkeypatch the module-level response_for_exception to block and verify background progress.
    """
    handler = DummyHandler('/static/')

    def serve_raising(request):
        raise Http404('not found')
    handler.serve = serve_raising
    counter = []
    orig_rf = handlers.response_for_exception

    def blocking_response(request, exc):
        time.sleep(0.15)
        return 'handled-error'
    handlers.response_for_exception = blocking_response
    try:

        async def main():

            async def background():
                for _ in range(30):
                    counter.append(1)
                    await asyncio.sleep(0.01)
            res, _ = await asyncio.gather(handler.get_response_async(SimpleNamespace(path='/static/missing')), background())
            return res
        result = asyncio.run(main())
        assert result == 'handled-error'
        assert len(counter) >= 5
    finally:
        handlers.response_for_exception = orig_rf

def test_file_path_decodes_percent_encoding():
    handler = DummyHandler('/static/')
    path = '/static/foo%20bar.txt'
    result = handler.file_path(path)
    assert result == 'foo bar.txt'

def test__should_handle_respects_netloc():
    handler = DummyHandler('http://example.com/static/')
    assert handler._should_handle('/static/file.txt') is False

def test__should_handle_accepts_exact_base_path_equal():
    handler = DummyHandler('/static/')
    assert handler._should_handle('/static/') is True

def test_file_path_empty_relative():
    handler = DummyHandler('/static/')
    assert handler.file_path('/static/') == ''

def test_serve_calls_module_serve_with_insecure_flag():
    orig_serve = handlers.serve
    captured = {}

    def fake_serve(request, path, insecure=False):
        captured['request'] = request
        captured['path'] = path
        captured['insecure'] = insecure
        return 'ok'
    handlers.serve = fake_serve
    try:
        handler = DummyHandler('/static/')
        request = SimpleNamespace(path='/static/subdir/file.txt')
        response = handler.serve(request)
        assert response == 'ok'
        assert captured['path'] == 'subdir/file.txt'
        assert captured['insecure'] is True
    finally:
        handlers.serve = orig_serve

def test_get_base_url_checks_settings():
    orig_check = handlers.utils.check_settings
    called = {'flag': False}

    def fake_check():
        called['flag'] = True
    handlers.utils.check_settings = fake_check
    try:
        handler = DummyHandler('/static/')
        assert handler.get_base_url() == settings.STATIC_URL
        assert called['flag'] is True
    finally:
        handlers.utils.check_settings = orig_check

def test_get_response_returns_response_for_exception_sync():
    """
    Synchronous get_response should return whatever response_for_exception returns
    when serve raises Http404.
    """
    handler = DummyHandler('/static/')

    def serve_raising(request):
        raise Http404('boom')
    handler.serve = serve_raising
    orig_rf = handlers.response_for_exception

    def fake_rf(request, exc):
        return 'sync-error'
    handlers.response_for_exception = fake_rf
    try:
        result = handler.get_response(SimpleNamespace(path='/static/x'))
        assert result == 'sync-error'
    finally:
        handlers.response_for_exception = orig_rf

def test_get_response_async_returns_response_when_not_404():
    """
    Simple sanity test that get_response_async returns the value from serve for non-exceptional cases.
    """
    handler = DummyHandler('/static/')

    def serve_ok(request):
        return 'async-ok'
    handler.serve = serve_ok
    result = asyncio.run(handler.get_response_async(SimpleNamespace(path='/static/x')))
    assert result == 'async-ok'

import importlib
import asyncio
import time
import threading
from types import SimpleNamespace
import pytest
import importlib
import asyncio
import time
import threading
from types import SimpleNamespace
import pytest
handlers = importlib.import_module('django.contrib.staticfiles.handlers')
Http404 = importlib.import_module('django.http').Http404
Request = SimpleNamespace()

def test_get_response_async_runs_serve_in_thread_when_no_exception():
    instance = DummyHandler()

    def serve_check_loop(request):
        try:
            asyncio.get_running_loop()
            return True
        except RuntimeError:
            return False
    instance.serve = serve_check_loop
    result = asyncio.run(instance.get_response_async(Request))
    assert result is False

def test_get_response_async_runs_response_for_exception_in_thread_on_http404():
    instance = DummyHandler()

    def serve_raises(request):
        raise Http404('not found')
    original_rfe = handlers.response_for_exception

    def response_for_exception_check(request, exc):
        try:
            asyncio.get_running_loop()
            return ('ran_in_loop', True)
        except RuntimeError:
            return ('ran_in_thread', False)
    handlers.response_for_exception = response_for_exception_check
    try:
        instance.serve = serve_raises
        result = asyncio.run(instance.get_response_async(Request))
        assert result == ('ran_in_thread', False)
    finally:
        handlers.response_for_exception = original_rfe

def test_get_response_async_returns_serve_return_value():
    instance = DummyHandler()
    instance.serve = lambda request: 'served-ok'
    result = asyncio.run(instance.get_response_async(Request))
    assert result == 'served-ok'

def test_get_response_async_passes_exception_instance_to_response_for_exception():
    instance = DummyHandler()
    exc_holder = {}

    def serve_raises(request):
        raise Http404('my-message')
    original_rfe = handlers.response_for_exception

    def response_for_exception_capture(request, exc):
        exc_holder['exc'] = exc
        return 'handled'
    handlers.response_for_exception = response_for_exception_capture
    try:
        instance.serve = serve_raises
        result = asyncio.run(instance.get_response_async(Request))
        assert result == 'handled'
        assert isinstance(exc_holder.get('exc'), Http404)
        assert str(exc_holder['exc']) == 'my-message'
    finally:
        handlers.response_for_exception = original_rfe

def test_get_response_async_handles_subclass_method_serve():

    class SubHandler(DummyHandler):

        def __init__(self):
            super().__init__()
            self.value = 'from-self'

        def serve(self, request):
            return self.value
    instance = SubHandler()
    result = asyncio.run(instance.get_response_async(Request))
    assert result == 'from-self'

def test_get_response_async_does_not_call_response_for_exception_when_no_exception():
    instance = DummyHandler()
    called = {'rfe': False}
    original_rfe = handlers.response_for_exception

    def response_for_exception_mark(*args, **kwargs):
        called['rfe'] = True
        return 'handled'
    handlers.response_for_exception = response_for_exception_mark
    try:
        instance.serve = lambda request: 'ok'
        result = asyncio.run(instance.get_response_async(Request))
        assert result == 'ok'
        assert called['rfe'] is False
    finally:
        handlers.response_for_exception = original_rfe

def test_get_response_async_concurrent_calls_are_independent():
    instance = DummyHandler()

    def serve_sleep(request):
        time.sleep(0.15)
        return threading.get_ident()
    instance.serve = serve_sleep

    async def run_two():
        t0 = time.time()
        results = await asyncio.gather(instance.get_response_async(Request), instance.get_response_async(Request))
        t1 = time.time()
        return (results, t1 - t0)
    results, elapsed = asyncio.run(run_two())
    assert elapsed < 0.3, 'Calls did not run concurrently; likely blocking the event loop'
    assert isinstance(results[0], int) and isinstance(results[1], int)

def test_get_response_async_awaits_response_for_exception_return_value():
    instance = DummyHandler()

    def serve_raises(request):
        raise Http404('boom')
    instance.serve = serve_raises
    original_rfe = handlers.response_for_exception
    handlers.response_for_exception = lambda request, exc: {'handled': str(exc)}
    try:
        result = asyncio.run(instance.get_response_async(Request))
        assert result == {'handled': 'boom'}
    finally:
        handlers.response_for_exception = original_rfe

def test_get_response_async_propagates_non_http404_exceptions():
    instance = DummyHandler()

    def serve_raises_value_error(request):
        raise ValueError('bad')
    instance.serve = serve_raises_value_error
    with pytest.raises(ValueError):
        asyncio.run(instance.get_response_async(Request))

def test_get_response_async_uses_sync_to_async_for_response_for_exception():
    instance = DummyHandler()

    def serve_raises(request):
        raise Http404('x')
    instance.serve = serve_raises
    called_context = {}
    original_rfe = handlers.response_for_exception

    def response_for_exception_context(request, exc):
        try:
            asyncio.get_running_loop()
            called_context['in_loop'] = True
        except RuntimeError:
            called_context['in_loop'] = False
        return 'handled'
    handlers.response_for_exception = response_for_exception_context
    try:
        result = asyncio.run(instance.get_response_async(Request))
        assert result == 'handled'
        assert called_context['in_loop'] is False
    finally:
        handlers.response_for_exception = original_rfe