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

from types import SimpleNamespace
from pathlib import Path
from unittest import mock
from types import SimpleNamespace
from django.template import autoreload
from django.template.backends.django import DjangoTemplates

def make_backend(engine_dirs, loader_dirs_list):
    """
    Create a fake backend instance that passes isinstance(..., DjangoTemplates)
    by creating an instance of a subclass of DjangoTemplates without calling its
    initializer, and attaching a simple 'engine' object with 'dirs' and
    'template_loaders'.
    loader_dirs_list is a list of lists, each inner list is the return value
    of one loader.get_dirs().
    """

    class Fake(DjangoTemplates):
        pass
    backend = object.__new__(Fake)
    loaders = []
    for loader_dirs in loader_dirs_list:

        class MockLoader:

            def __init__(self, dirs):
                self._dirs = dirs

            def get_dirs(self):
                return self._dirs

            def reset(self):
                return None
        loaders.append(MockLoader(loader_dirs))
    backend.engine = SimpleNamespace(dirs=engine_dirs, template_loaders=loaders)
    return backend

@mock.patch('django.template.autoreload.engines.all')
def test_ignore_empty_string_in_engine_dirs(mock_all):
    mock_all.return_value = [make_backend([''], [])]
    assert autoreload.get_template_directories() == set()

@mock.patch('django.template.autoreload.engines.all')
def test_ignore_none_in_engine_dirs(mock_all):
    mock_all.return_value = [make_backend([None], [])]
    assert autoreload.get_template_directories() == set()

@mock.patch('django.template.autoreload.engines.all')
def test_include_relative_engine_dir(mock_all):
    mock_all.return_value = [make_backend(['relative_templates'], [])]
    expected = {Path.cwd() / 'relative_templates'}
    assert autoreload.get_template_directories() == expected

@mock.patch('django.template.autoreload.engines.all')
def test_ignore_empty_string_from_loader_get_dirs(mock_all):
    mock_all.return_value = [make_backend([], [['']])]
    assert autoreload.get_template_directories() == set()

@mock.patch('django.template.autoreload.engines.all')
def test_ignore_none_from_loader_get_dirs(mock_all):
    mock_all.return_value = [make_backend([], [[None]])]
    assert autoreload.get_template_directories() == set()

@mock.patch('django.template.autoreload.engines.all')
def test_include_relative_loader_dir(mock_all):
    mock_all.return_value = [make_backend([], [['loader_templates']])]
    expected = {Path.cwd() / 'loader_templates'}
    assert autoreload.get_template_directories() == expected

@mock.patch('django.template.autoreload.engines.all')
def test_combined_engine_and_loader_dirs(mock_all):
    mock_all.return_value = [make_backend([''], [['loader_only']])]
    expected = {Path.cwd() / 'loader_only'}
    assert autoreload.get_template_directories() == expected

@mock.patch('django.template.autoreload.engines.all')
def test_watch_for_template_changes_with_loader_dirs(mock_all):
    mock_all.return_value = [make_backend([], [['watched_dir']])]
    reloader = mock.MagicMock()
    autoreload.watch_for_template_changes(reloader)
    reloader.watch_dir.assert_called_with(Path.cwd() / 'watched_dir', '**/*')

@mock.patch('django.template.autoreload.engines.all')
@mock.patch('django.template.autoreload.reset_loaders')
def test_template_changed_resets_for_non_py_file_inside_template_dir(mock_reset, mock_all):
    mock_all.return_value = [make_backend([], [['some_templates']])]
    template_dir = Path.cwd() / 'some_templates'
    file_in_template = template_dir / 'subdir' / 'file.txt'
    assert autoreload.template_changed(None, file_in_template) is True
    mock_reset.assert_called_once()

@mock.patch('django.template.autoreload.engines.all')
@mock.patch('django.template.autoreload.reset_loaders')
def test_template_changed_ignores_python_files(mock_reset, mock_all):
    mock_all.return_value = [make_backend([], [['some_templates']])]
    template_dir = Path.cwd() / 'some_templates'
    python_file = template_dir / 'module.py'
    assert autoreload.template_changed(None, python_file) is None
    mock_reset.assert_not_called()

from pathlib import Path
from unittest import mock
from django.template import autoreload, engines
from django.template.backends.django import DjangoTemplates
from django.test import SimpleTestCase, override_settings
try:
    ROOT
except NameError:
    ROOT = Path(__file__).parent.absolute()

class AutoreloadExtraTests(SimpleTestCase):

    def _get_django_backend(self):
        return next((b for b in engines.all() if isinstance(b, DjangoTemplates)))