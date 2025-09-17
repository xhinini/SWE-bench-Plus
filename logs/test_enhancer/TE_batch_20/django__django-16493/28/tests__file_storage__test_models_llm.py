import unittest
import tempfile
from pathlib import Path
import unittest
import tempfile
from pathlib import Path
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models.fields.files import FileField
temp_storage_location = tempfile.mkdtemp()
temp_storage = FileSystemStorage(location=temp_storage_location)
if __name__ == '__main__':
    unittest.main()