import tempfile
import shutil
import uuid
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import FileSystemStorage
from django.test.utils import override_settings
from django.conf import settings