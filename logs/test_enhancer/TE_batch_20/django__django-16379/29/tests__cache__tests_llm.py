from unittest import mock
import os
import tempfile
import time
from pathlib import Path
from django.test import override_settings
from django.core.cache import caches, cache, DEFAULT_CACHE_ALIAS