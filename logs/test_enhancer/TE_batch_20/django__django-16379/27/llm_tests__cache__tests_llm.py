from django.test.signals import setting_changed
from django.conf import settings
from unittest import mock
import os
import tempfile
import shutil
from django.test import TestCase, override_settings
from django.test.signals import setting_changed
from django.conf import settings
from django.core.cache import cache
from django.core.cache.tests import caches_setting_for_tests