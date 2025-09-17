from types import SimpleNamespace
from pathlib import Path
from types import SimpleNamespace
from unittest import mock
from django.template import autoreload
from django.template.backends.django import DjangoTemplates
from django.test import SimpleTestCase

def make_backend(dirs=None, loader_dirs_list=None):
    """
    Create a DummyBackend instance with engine.dirs and engine.template_loaders
    configured as provided.

    - dirs: list of directory strings for engine.dirs
    - loader_dirs_list: list of lists; each inner list is returned by a loader's get_dirs()
    """
    if dirs is None:
        dirs = []
    if loader_dirs_list is None:
        loader_dirs_list = []
    backend = object.__new__(DummyBackend)
    engine = SimpleNamespace()
    engine.dirs = dirs
    loaders = []
    for ldirs in loader_dirs_list:
        loaders.append(SimpleNamespace(get_dirs=lambda ldirs=ldirs: ldirs))
    engine.template_loaders = loaders
    backend.engine = engine
    return backend