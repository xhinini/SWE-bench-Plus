import os
import tempfile
from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.test import SimpleTestCase
import os
import tempfile
from io import BytesIO
from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.test import SimpleTestCase