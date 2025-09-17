from django.test import SimpleTestCase
from django.db import models
from django.core.files.storage import default_storage
from pathlib import Path
from tests.file_storage.models import Storage, temp_storage, callable_storage, callable_default_storage, CallableStorage