import os
from tempfile import TemporaryDirectory
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import global_settings
from unittest import mock
from tempfile import TemporaryDirectory
from django.test import SimpleTestCase, override_settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.conf import global_settings
import os
from unittest import mock