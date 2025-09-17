from django.core.files.base import ContentFile
import os
import shutil
import tempfile
import unittest
from django.test import override_settings
from django.core.files.base import ContentFile
from django.contrib.staticfiles.storage import HashedFilesMixin, ManifestFilesMixin, StaticFilesStorage, ManifestStaticFilesStorage