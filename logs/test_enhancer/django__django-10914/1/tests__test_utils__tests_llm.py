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