from django.conf import settings
from django.test import override_settings
import os
import shutil
import tempfile
import unittest
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage, HashedFilesMixin
from django.core.files.storage import FileSystemStorage

class PostProcessTests(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def _make_storage(self, storage_cls=ManifestStaticFilesStorage, **kwargs):
        kwargs.setdefault('location', self.tempdir)
        kwargs.setdefault('base_url', '/static/')
        return storage_cls(**kwargs)
if __name__ == '__main__':
    unittest.main()