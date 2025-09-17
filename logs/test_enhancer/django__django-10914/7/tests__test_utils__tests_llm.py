import os
import shutil
import tempfile
from unittest import mock
from django.test import SimpleTestCase, override_settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.conf import settings