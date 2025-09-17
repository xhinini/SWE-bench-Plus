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