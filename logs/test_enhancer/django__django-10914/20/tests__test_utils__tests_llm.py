import os
import shutil
import tempfile
from unittest import mock
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, override_settings
import os
import shutil
import tempfile
from unittest import mock
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, override_settings

class FileUploadPermissionsTests(SimpleTestCase):

    def _make_storage(self, location=None, **kwargs):
        if location is None:
            location = tempfile.mkdtemp()
        storage = FileSystemStorage(location=location, **kwargs)
        self.addCleanup(lambda: shutil.rmtree(location, ignore_errors=True))
        return (storage, location)

import tempfile
import shutil
import os
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.test.utils import override_settings
import os
import tempfile
import shutil
from django.test import SimpleTestCase
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.test.utils import override_settings

class FileUploadPermissionsTests(SimpleTestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmpdir, True)

    def _baseline_file_mode(self):
        path = os.path.join(self.tmpdir, 'baseline.tmp')
        with open(path, 'wb') as f:
            f.write(b'baseline')
        mode = os.stat(path).st_mode & 511
        os.remove(path)
        return mode

    def _baseline_dir_mode(self):
        d = os.path.join(self.tmpdir, 'baseline_dir')
        os.mkdir(d)
        mode = os.stat(d).st_mode & 511
        shutil.rmtree(d)
        return mode

from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import tempfile
import shutil
from unittest import mock
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase

class FileUploadPermissionsTests(SimpleTestCase):

    def _make_temp_dir(self):
        path = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, path, ignore_errors=True)
        return path

import os
import shutil
import tempfile
from io import BytesIO
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from django.conf import settings
import os
import shutil
import tempfile
from io import BytesIO
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from django.conf import settings

class FileUploadPermissionsTests(SimpleTestCase):

    def _make_tempdir(self):
        return tempfile.mkdtemp(prefix='djangotest_upload_')

import tempfile
import shutil
import os
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import shutil
import tempfile
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, override_settings
from django.core.files.storage import default_storage

class FileUploadPermissionsTests(SimpleTestCase):

    def _mkdtemp(self):
        tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmpdir, ignore_errors=True)
        return tmpdir

import tempfile
import shutil
import os
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.test import TestCase, override_settings
from django.conf import settings
from django.core.files.storage import default_storage
from unittest import mock

class FileUploadPermissionsTests(TestCase):

    def _make_temp_media_root(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        return tmp

import os
import shutil
import tempfile
import unittest
from io import BytesIO
from django.conf import settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.test import SimpleTestCase

@unittest.skipIf(os.name == 'nt', 'POSIX file permission bits not reliable on Windows')
class FileUploadPermissionsTests(SimpleTestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp(prefix='djtest_uploads_')

    def tearDown(self):
        try:
            shutil.rmtree(self.tempdir)
        except Exception:
            pass

import tempfile
import shutil
import os
import stat
import tempfile
import shutil
from django.conf import settings, global_settings
from django.test import SimpleTestCase, override_settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile

class FileUploadPermissionsTests(SimpleTestCase):

    def _mkdtemp(self):
        tmpdir = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(tmpdir, ignore_errors=True))
        return tmpdir

import os
import stat
import shutil
import tempfile
from unittest import mock
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.core.files.storage import FileSystemStorage, default_storage
from django.test import SimpleTestCase
from django.conf import settings
import os
import stat
import shutil
import tempfile
from unittest import mock
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.core.files.storage import FileSystemStorage, default_storage
from django.test import SimpleTestCase
from django.conf import settings

class FileUploadPermissionsTests(SimpleTestCase):

    def _make_tmpdir(self):
        tmpdir = tempfile.mkdtemp(prefix='djtest_media_')
        self.addCleanup(shutil.rmtree, tmpdir, ignore_errors=True)
        return tmpdir

import os
import shutil
import tempfile
from unittest import mock
from django.conf import settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.test import SimpleTestCase, override_settings

class FileUploadPermissionsTests(SimpleTestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        try:
            shutil.rmtree(self.tmpdir)
        except Exception:
            pass

import os
import shutil
import tempfile
from unittest import mock
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
import os
import shutil
import tempfile
from unittest import mock
from django.conf import settings
from django.test import SimpleTestCase, override_settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile

class FileUploadPermissionsTests(SimpleTestCase):

    def _make_tempdir(self):
        return tempfile.mkdtemp()

import os
import shutil
import stat
import tempfile
from unittest import mock
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.core.files.storage import default_storage
from django.test import SimpleTestCase, override_settings
from django.conf import settings

class FileUploadPermissionsTests(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        try:
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass

import os
import shutil
import stat
import tempfile
from unittest import mock
from django.conf import settings, global_settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.test import SimpleTestCase
from django.test.utils import override_settings
import os
import shutil
import stat
import tempfile
from unittest import mock
from django.conf import settings, global_settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.test import SimpleTestCase
from django.test.utils import override_settings