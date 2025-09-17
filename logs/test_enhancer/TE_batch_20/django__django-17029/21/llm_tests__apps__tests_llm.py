from django.apps import apps, AppConfig
from django.apps.registry import Apps
from django.test import SimpleTestCase
from typing import List

def _patch_cache_clears(target, calls: List[str]):
    """
    Replace cache_clear callables on the given Apps-like object to record
    invocation order. Returns a tuple of (restore_swappable, restore_models)
    callables to restore original attributes.
    """
    orig_swappable = target.get_swappable_settings_name.cache_clear
    orig_models = target.get_models.cache_clear

    def _make_recorder(name):

        def recorder():
            calls.append(name)
        return recorder
    target.get_swappable_settings_name.cache_clear = _make_recorder('swappable')
    target.get_models.cache_clear = _make_recorder('models')

    def restore_swappable():
        target.get_swappable_settings_name.cache_clear = orig_swappable

    def restore_models():
        target.get_models.cache_clear = orig_models
    return (restore_swappable, restore_models)