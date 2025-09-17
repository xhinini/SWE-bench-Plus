import os
import stat
import shutil
import tempfile
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.test import override_settings, SimpleTestCase