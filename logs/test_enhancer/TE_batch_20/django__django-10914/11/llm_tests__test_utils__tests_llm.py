import os
import stat
import tempfile
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.conf import settings
from django.test import SimpleTestCase