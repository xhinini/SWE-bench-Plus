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