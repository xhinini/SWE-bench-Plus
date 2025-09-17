import builtins
import os
import tempfile
import shutil
from django.test import override_settings, TestCase
from django.conf import settings
from django.test import setting_changed
from django.core.cache import cache, caches
from unittest import mock