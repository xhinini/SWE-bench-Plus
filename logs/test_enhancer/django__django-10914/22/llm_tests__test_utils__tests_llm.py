import tempfile
import os
from unittest import mock
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.conf import settings
from django.test import SimpleTestCase, override_settings
import os
import tempfile
from unittest import mock
from django.conf import settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.test import SimpleTestCase, override_settings