import os
import tempfile
import shutil
from unittest import mock
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.core.files.storage import default_storage
from django.test import SimpleTestCase
from django.conf import settings