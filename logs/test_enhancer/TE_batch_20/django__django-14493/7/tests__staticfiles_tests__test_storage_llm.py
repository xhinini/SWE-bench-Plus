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

from django.core.files.base import ContentFile
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
import os
import shutil
import tempfile
import unittest
from django.core.files.base import ContentFile
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.conf import settings

class PostProcessMaxPassesZeroTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
if __name__ == '__main__':
    unittest.main()

from django.core.files.base import ContentFile
from django.contrib.staticfiles.storage import HashedFilesMixin, ManifestFilesMixin, StaticFilesStorage, ManifestStaticFilesStorage
import os
import tempfile
import shutil
import unittest
from django.core.files.base import ContentFile
from django.contrib.staticfiles.storage import HashedFilesMixin, ManifestFilesMixin, StaticFilesStorage, ManifestStaticFilesStorage

class PostProcessMaxPassesZeroTests(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
if __name__ == '__main__':
    unittest.main()

from django.core.files.base import ContentFile
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage, StaticFilesStorage, HashedFilesMixin
import os
import json
import tempfile
import shutil
import unittest
from django.core.files.base import ContentFile
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage, StaticFilesStorage, HashedFilesMixin
from django.conf import settings

class ZeroPassPostProcessTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

import os
import shutil
import tempfile
import unittest
from django.contrib.staticfiles.storage import HashedFilesMixin, ManifestFilesMixin, StaticFilesStorage

class PostProcessMaxZeroTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()