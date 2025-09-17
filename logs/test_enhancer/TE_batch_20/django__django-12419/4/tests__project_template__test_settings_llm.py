import os
import shutil
import tempfile
from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path

def _parse_headers(response):
    """
    Parse response.serialize_headers() into a dict of header -> value.
    """
    headers = {}
    for line in response.serialize_headers().split(b'\r\n'):
        if not line:
            continue
        try:
            name, value = line.split(b': ', 1)
        except ValueError:
            continue
        headers[name.decode('ascii')] = value.decode('ascii')
    return headers

import os
import shutil
import tempfile
from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
import os
import shutil
import tempfile
from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path

class TestReferrerPolicySettings(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        template_settings_py = os.path.join(os.path.dirname(conf.__file__), 'project_template', 'project_name', 'settings.py-tpl')
        test_settings_py = os.path.join(self.temp_dir.name, 'test_settings.py')
        shutil.copyfile(template_settings_py, test_settings_py)

    def _load_middleware_from_template(self):
        with extend_sys_path(self.temp_dir.name):
            from test_settings import MIDDLEWARE
            return MIDDLEWARE

import os
import shutil
import tempfile
from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path

class TestReferrerPolicy(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        template_settings_py = os.path.join(os.path.dirname(conf.__file__), 'project_template', 'project_name', 'settings.py-tpl')
        test_settings_py = os.path.join(self.temp_dir.name, 'test_settings.py')
        shutil.copyfile(template_settings_py, test_settings_py)

    def _import_template_middleware(self):
        with extend_sys_path(self.temp_dir.name):
            from test_settings import MIDDLEWARE
            return MIDDLEWARE

import os
import shutil
import tempfile
from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
import os
import shutil
import tempfile
from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path

class TestReferrerPolicyHeader(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        template_settings_py = os.path.join(os.path.dirname(conf.__file__), 'project_template', 'project_name', 'settings.py-tpl')
        test_settings_py = os.path.join(self.temp_dir.name, 'test_settings.py')
        shutil.copyfile(template_settings_py, test_settings_py)

import os
import shutil
import tempfile
import importlib
from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path

class TestReferrerPolicySettings(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        template_settings_py = os.path.join(os.path.dirname(conf.__file__), 'project_template', 'project_name', 'settings.py-tpl')
        self.test_settings_path = os.path.join(self.temp_dir.name, 'test_settings.py')
        shutil.copyfile(template_settings_py, self.test_settings_path)

    def _load_template_middleware(self):
        with extend_sys_path(self.temp_dir.name):
            if 'test_settings' in globals():
                importlib.reload(importlib.import_module('test_settings'))
            from test_settings import MIDDLEWARE
            return MIDDLEWARE