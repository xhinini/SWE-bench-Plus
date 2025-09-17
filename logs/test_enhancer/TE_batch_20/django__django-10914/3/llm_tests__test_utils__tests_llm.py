import os
import tempfile
import shutil
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import shutil
import tempfile
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.test import override_settings, SimpleTestCase

class FileUploadPermissionsTests(SimpleTestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(self.tmpdir, ignore_errors=True))

import tempfile
import shutil
import os
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.conf import settings
from django.test import SimpleTestCase, override_settings

class FileUploadPermissionsTests(SimpleTestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix='test_upload_perms_')
        self.addCleanup(shutil.rmtree, self.tmpdir, True)