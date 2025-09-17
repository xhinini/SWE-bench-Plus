import os
import tempfile
from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, override_settings