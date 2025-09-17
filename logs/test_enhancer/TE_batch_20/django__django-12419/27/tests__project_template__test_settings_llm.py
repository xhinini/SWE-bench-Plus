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

import os
import shutil
import tempfile
from django import conf
from django.conf import global_settings
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
import os
import shutil
import tempfile
from django import conf
from django.conf import global_settings
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path

class ReferrerPolicyTests(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        template_settings_py = os.path.join(os.path.dirname(conf.__file__), 'project_template', 'project_name', 'settings.py-tpl')
        test_settings_py = os.path.join(self.temp_dir.name, 'test_settings.py')
        shutil.copyfile(template_settings_py, test_settings_py)

import os
import shutil
import tempfile
from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path

class TestStartProjectSettings(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        template_settings_py = os.path.join(os.path.dirname(conf.__file__), 'project_template', 'project_name', 'settings.py-tpl')
        test_settings_py = os.path.join(self.temp_dir.name, 'test_settings.py')
        shutil.copyfile(template_settings_py, test_settings_py)

import os
import shutil
import tempfile
import django
from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
from django.conf import global_settings as django_global_settings
import os
import shutil
import tempfile
import django
from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
from django.conf import global_settings as django_global_settings

class TestSecureReferrerPolicy(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        template_settings_py = os.path.join(os.path.dirname(conf.__file__), 'project_template', 'project_name', 'settings.py-tpl')
        test_settings_py = os.path.join(self.temp_dir.name, 'test_settings.py')
        shutil.copyfile(template_settings_py, test_settings_py)
        with extend_sys_path(self.temp_dir.name):
            from test_settings import MIDDLEWARE
        self.template_middleware = list(MIDDLEWARE)

import os
import shutil
import tempfile
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path

class TestReferrerPolicySettings(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        template_settings_py = os.path.join(os.path.dirname(__import__('django.conf').conf.__file__), 'project_template', 'project_name', 'settings.py-tpl')
        test_settings_py = os.path.join(self.temp_dir.name, 'test_settings.py')
        shutil.copyfile(template_settings_py, test_settings_py)

    def _get_headers(self, settings_overrides=None, middleware_override=None):
        """
        Helper to import the copied test_settings, apply settings overrides and return
        sorted response headers as a list of bytes.
        """
        with extend_sys_path(self.temp_dir.name):
            from test_settings import MIDDLEWARE as TEMPLATE_MIDDLEWARE
            from test_settings import MIDDLEWARE as IMPORTED_MIDDLEWARE
        MIDDLEWARE = middleware_override if middleware_override is not None else IMPORTED_MIDDLEWARE
        settings_kwargs = {'MIDDLEWARE': MIDDLEWARE, 'ROOT_URLCONF': 'project_template.urls'}
        if settings_overrides:
            settings_kwargs.update(settings_overrides)
        with self.settings(**settings_kwargs):
            response = self.client.get('/empty/')
        headers = sorted(response.serialize_headers().split(b'\r\n'))
        return headers

import os
import shutil
import tempfile
from django import conf as django_conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
import os
import shutil
import tempfile
from django import conf as django_conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path

class TestReferrerPolicy(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        template_settings_py = os.path.join(os.path.dirname(django_conf.__file__), 'project_template', 'project_name', 'settings.py-tpl')
        test_settings_py = os.path.join(self.temp_dir.name, 'test_settings.py')
        shutil.copyfile(template_settings_py, test_settings_py)

    def _get_headers(self, secure_referrer_policy_sentinel=None):
        """
        Helper to import MIDDLEWARE from the copied template settings and perform
        a GET to /empty/ returning the list of header lines (bytes).

        If secure_referrer_policy_sentinel is the special object _NOT_PROVIDED,
        the SECURE_REFERRER_POLICY setting won't be passed into self.settings(),
        so the system default will be used. Otherwise the provided value will be
        applied to SECURE_REFERRER_POLICY.
        """
        _NOT_PROVIDED = object()
        with extend_sys_path(self.temp_dir.name):
            from test_settings import MIDDLEWARE
        settings_kwargs = dict(MIDDLEWARE=MIDDLEWARE, ROOT_URLCONF='project_template.urls')
        if secure_referrer_policy_sentinel is not _NOT_PROVIDED:
            settings_kwargs['SECURE_REFERRER_POLICY'] = secure_referrer_policy_sentinel
        with self.settings(**settings_kwargs):
            response = self.client.get('/empty/')
        return response.serialize_headers().split(b'\r\n')

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

    def _get_middleware(self):
        with extend_sys_path(self.temp_dir.name):
            from test_settings import MIDDLEWARE
        return MIDDLEWARE

    def _response_headers(self, **override_settings):
        MIDDLEWARE = self._get_middleware()
        with self.settings(MIDDLEWARE=MIDDLEWARE, ROOT_URLCONF='project_template.urls', **override_settings):
            response = self.client.get('/empty/')
            headers = sorted(response.serialize_headers().split(b'\r\n'))
            return headers

from django.conf import global_settings as django_global_settings
import os
import shutil
import tempfile
from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
from django.conf import global_settings as django_global_settings

class TestReferrerPolicySettings(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        template_settings_py = os.path.join(os.path.dirname(conf.__file__), 'project_template', 'project_name', 'settings.py-tpl')
        test_settings_py = os.path.join(self.temp_dir.name, 'test_settings.py')
        shutil.copyfile(template_settings_py, test_settings_py)

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

    def _load_middleware(self):
        with extend_sys_path(self.temp_dir.name):
            from test_settings import MIDDLEWARE
        return MIDDLEWARE

import types
import sys
import os
import shutil
import sys
import tempfile
import types
from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
from django.http import HttpResponse, StreamingHttpResponse
from django.urls import path

class TestReferrerPolicyBehavior(SimpleTestCase):

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

class TestReferrerPolicySettings(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        template_settings_py = os.path.join(os.path.dirname(conf.__file__), 'project_template', 'project_name', 'settings.py-tpl')
        test_settings_py = os.path.join(self.temp_dir.name, 'test_settings.py')
        shutil.copyfile(template_settings_py, test_settings_py)

    def _import_middleware(self):
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
        with extend_sys_path(self.temp_dir.name):
            from test_settings import MIDDLEWARE
            self.MIDDLEWARE = MIDDLEWARE

from django import conf
from django.test import SimpleTestCase

class ReferrerPolicyTests(SimpleTestCase):
    """
    Tests around the Referrer-Policy header produced by
    django.middleware.security.SecurityMiddleware and the
    SECURE_REFERRER_POLICY setting.
    """

    def _get_headers(self, **settings_overrides):
        """
        Make a GET to the test '/empty/' URL using project_template.urls and
        return a dict of header-name -> header-value for the response.
        """
        with self.settings(ROOT_URLCONF='project_template.urls', **settings_overrides):
            response = self.client.get('/empty/')
            lines = response.serialize_headers().split(b'\r\n')
            headers = {}
            for line in lines:
                if not line:
                    continue
                k, v = line.split(b': ', 1)
                headers[k.decode()] = v.decode()
            return headers

import os
import shutil
import tempfile
from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path

class TestReferrerPolicyRegression(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        template_settings_py = os.path.join(os.path.dirname(conf.__file__), 'project_template', 'project_name', 'settings.py-tpl')
        test_settings_py = os.path.join(self.temp_dir.name, 'test_settings.py')
        shutil.copyfile(template_settings_py, test_settings_py)

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

import os
import shutil
import tempfile
from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path

class TestSecureReferrerPolicy(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        template_settings_py = os.path.join(os.path.dirname(conf.__file__), 'project_template', 'project_name', 'settings.py-tpl')
        test_settings_py = os.path.join(self.temp_dir.name, 'test_settings.py')
        shutil.copyfile(template_settings_py, test_settings_py)

import os
import shutil
import tempfile
from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path

from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
import os
import shutil
import tempfile

class TestReferrerPolicySettings(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        template_settings_py = os.path.join(os.path.dirname(conf.__file__), 'project_template', 'project_name', 'settings.py-tpl')
        test_settings_py = os.path.join(self.temp_dir.name, 'test_settings.py')
        shutil.copyfile(template_settings_py, test_settings_py)

    def _default_middleware(self):
        with extend_sys_path(self.temp_dir.name):
            from test_settings import MIDDLEWARE
        return MIDDLEWARE

def test_default_referrer_policy_header_present_by_default(self):
    with extend_sys_path(self.temp_dir.name):
        from test_settings import MIDDLEWARE
    with self.settings(MIDDLEWARE=MIDDLEWARE, ROOT_URLCONF='project_template.urls'):
        response = self.client.get('/empty/')
        headers = response.serialize_headers().split(b'\r\n')
        self.assertIn(b'Referrer-Policy: same-origin', headers)

def test_explicit_none_disables_referrer_policy_header(self):
    with extend_sys_path(self.temp_dir.name):
        from test_settings import MIDDLEWARE
    with self.settings(MIDDLEWARE=MIDDLEWARE, ROOT_URLCONF='project_template.urls', SECURE_REFERRER_POLICY=None):
        response = self.client.get('/empty/')
        headers = response.serialize_headers().split(b'\r\n')
        self.assertFalse(any((h.startswith(b'Referrer-Policy:') for h in headers)))

def test_empty_string_sets_empty_referrer_policy_header(self):
    with extend_sys_path(self.temp_dir.name):
        from test_settings import MIDDLEWARE
    with self.settings(MIDDLEWARE=MIDDLEWARE, ROOT_URLCONF='project_template.urls', SECURE_REFERRER_POLICY=''):
        response = self.client.get('/empty/')
        headers = response.serialize_headers().split(b'\r\n')
        self.assertIn(b'Referrer-Policy: ', headers)

def test_custom_string_referrer_policy_is_used(self):
    with extend_sys_path(self.temp_dir.name):
        from test_settings import MIDDLEWARE
    with self.settings(MIDDLEWARE=MIDDLEWARE, ROOT_URLCONF='project_template.urls', SECURE_REFERRER_POLICY='no-referrer'):
        response = self.client.get('/empty/')
        headers = response.serialize_headers().split(b'\r\n')
        self.assertIn(b'Referrer-Policy: no-referrer', headers)

def test_numeric_referrer_policy_is_coerced_to_string(self):
    with extend_sys_path(self.temp_dir.name):
        from test_settings import MIDDLEWARE
    with self.settings(MIDDLEWARE=MIDDLEWARE, ROOT_URLCONF='project_template.urls', SECURE_REFERRER_POLICY=123):
        response = self.client.get('/empty/')
        headers = response.serialize_headers().split(b'\r\n')
        self.assertIn(b'Referrer-Policy: 123', headers)

def test_no_security_middleware_no_referrer_policy_header_even_if_setting_present(self):
    with extend_sys_path(self.temp_dir.name):
        from test_settings import MIDDLEWARE as TEMPLATE_MIDDLEWARE
    middleware_without_security = [m for m in TEMPLATE_MIDDLEWARE if m != 'django.middleware.security.SecurityMiddleware']
    with self.settings(MIDDLEWARE=middleware_without_security, ROOT_URLCONF='project_template.urls', SECURE_REFERRER_POLICY='same-origin'):
        response = self.client.get('/empty/')
        headers = response.serialize_headers().split(b'\r\n')
        self.assertFalse(any((h.startswith(b'Referrer-Policy:') for h in headers)))

def test_security_middleware_at_end_still_sets_header(self):
    with extend_sys_path(self.temp_dir.name):
        from test_settings import MIDDLEWARE
    mw = list(MIDDLEWARE)
    if 'django.middleware.security.SecurityMiddleware' in mw:
        mw.remove('django.middleware.security.SecurityMiddleware')
    mw.append('django.middleware.security.SecurityMiddleware')
    with self.settings(MIDDLEWARE=mw, ROOT_URLCONF='project_template.urls'):
        response = self.client.get('/empty/')
        headers = response.serialize_headers().split(b'\r\n')
        self.assertIn(b'Referrer-Policy: same-origin', headers)

def test_multiple_requests_consistently_set_referrer_policy(self):
    with extend_sys_path(self.temp_dir.name):
        from test_settings import MIDDLEWARE
    with self.settings(MIDDLEWARE=MIDDLEWARE, ROOT_URLCONF='project_template.urls'):
        resp1 = self.client.get('/empty/')
        resp2 = self.client.get('/empty/')
        headers1 = resp1.serialize_headers().split(b'\r\n')
        headers2 = resp2.serialize_headers().split(b'\r\n')
        self.assertIn(b'Referrer-Policy: same-origin', headers1)
        self.assertIn(b'Referrer-Policy: same-origin', headers2)

def test_project_template_settings_middleware_produces_referrer_policy(self):
    with extend_sys_path(self.temp_dir.name):
        from test_settings import MIDDLEWARE
    with self.settings(MIDDLEWARE=MIDDLEWARE, ROOT_URLCONF='project_template.urls'):
        response = self.client.get('/empty/')
        headers = response.serialize_headers().split(b'\r\n')
        self.assertIn(b'Referrer-Policy: same-origin', headers)