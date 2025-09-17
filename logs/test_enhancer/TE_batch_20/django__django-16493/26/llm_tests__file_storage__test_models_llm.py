from django.test import SimpleTestCase
import tempfile
import shutil
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models.fields.files import FileField