import os
import tempfile
from django.conf import global_settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings, global_settings
from django.test import SimpleTestCase, override_settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage, default_storage
import os
import tempfile