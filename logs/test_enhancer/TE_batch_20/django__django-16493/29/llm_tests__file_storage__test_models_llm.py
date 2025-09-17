from django.test import SimpleTestCase
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models.fields.files import FileField
from pathlib import Path
import tempfile
import types
from django.test import SimpleTestCase
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models.fields.files import FileField
from pathlib import Path
import tempfile
import types
temp_storage_location = tempfile.mkdtemp()
temp_storage = FileSystemStorage(location=temp_storage_location)