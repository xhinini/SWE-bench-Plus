from django.core.cache import caches, cache
from django.core.cache.backends.filebased import FileBasedCache
import builtins
import pickle
import os
import tempfile
from unittest import mock