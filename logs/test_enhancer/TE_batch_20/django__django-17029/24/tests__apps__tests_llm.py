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

from types import SimpleNamespace
from types import SimpleNamespace
from django.test import SimpleTestCase, isolate_apps

def make_fake_app_config(name, models_list):
    """
    Create a fake app config object with a get_models method compatible
    with Apps' expectations.
    """

    class FakeAppConfig:

        def __init__(self, name):
            self.name = name

        def get_models(self, include_auto_created=False, include_swapped=False):
            return list(models_list)
    return FakeAppConfig(name)

def make_fake_model(app_label, model_name, swapped=None, swappable=None, expire_calls=None, registry=None):
    """
    Create a fake model class with a _meta object that has the attributes
    needed by get_swappable_settings_name and an _expire_cache method that
    optionally calls back into the registry to simulate repopulation.
    """
    meta = SimpleNamespace()
    meta.app_label = app_label
    meta.model_name = model_name
    meta.label_lower = f'{app_label}.{model_name}'.lower()
    meta.swapped = swapped
    meta.swappable = swappable

    def _expire_cache():
        if expire_calls:
            for arg in expire_calls:
                registry.get_swappable_settings_name(arg)
    meta._expire_cache = _expire_cache
    Model = SimpleNamespace(_meta=meta)
    return Model