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