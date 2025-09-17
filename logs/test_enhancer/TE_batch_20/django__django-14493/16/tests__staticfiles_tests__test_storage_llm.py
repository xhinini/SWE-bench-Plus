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

import os
import tempfile
import unittest
from pathlib import Path
from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage, HashedFilesMixin, StaticFilesStorage

def _call_post_process_and_collect(storage_instance, paths):
    """
    Helper to exhaust the generator returned by post_process and return all
    yielded items as a list. Any exception will propagate to the caller.
    """
    return list(storage_instance.post_process(paths, dry_run=False))
if __name__ == '__main__':
    unittest.main()

from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
import os
import shutil
import tempfile
import unittest
from io import BytesIO
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.core.files.base import ContentFile

from django.core.files.base import ContentFile
import os
import shutil
import tempfile
import unittest
from django.contrib.staticfiles.storage import HashedFilesMixin, StaticFilesStorage, ManifestStaticFilesStorage
from django.core.files.base import ContentFile

class PostProcessZeroPassesTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
if __name__ == '__main__':
    unittest.main()

import tempfile
import shutil
import os
import unittest
from django.core.files.base import ContentFile
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage, HashedFilesMixin, StaticFilesStorage
import os
import shutil
import tempfile
import unittest
from django.core.files.base import ContentFile
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage, HashedFilesMixin, StaticFilesStorage

class PostProcessZeroPassesTests(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
if __name__ == '__main__':
    unittest.main()

import os
import shutil
import tempfile
import hashlib
import unittest
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

class PostProcessMaxPassesZeroTests(unittest.TestCase):

    def setUp(self):
        self.src_dir = tempfile.mkdtemp()
        self.dst_dir = tempfile.mkdtemp()
        self._orig_static_url = getattr(settings, 'STATIC_URL', '/static/')
        settings.STATIC_URL = '/static/'

from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.contrib.staticfiles.storage import HashedFilesMixin, ManifestStaticFilesStorage
import os
import shutil
import tempfile
import unittest
import json
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.contrib.staticfiles.storage import HashedFilesMixin, ManifestStaticFilesStorage

class PostProcessZeroPassesTests(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
if __name__ == '__main__':
    unittest.main()