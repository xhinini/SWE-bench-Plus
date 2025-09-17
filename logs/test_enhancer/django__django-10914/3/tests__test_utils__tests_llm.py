import os
import tempfile
import shutil
from io import BytesIO
from django.test import SimpleTestCase, TestCase
from django.test.utils import override_settings
from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile