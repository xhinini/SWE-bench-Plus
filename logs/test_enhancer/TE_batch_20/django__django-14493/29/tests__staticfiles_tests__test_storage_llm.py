from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.storage import HashedFilesMixin, ManifestFilesMixin
import os
import shutil
import tempfile
import unittest
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.storage import HashedFilesMixin, ManifestFilesMixin