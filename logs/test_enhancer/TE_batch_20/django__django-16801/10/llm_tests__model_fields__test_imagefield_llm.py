import io
import os
from unittest import skipIf
from django.core.exceptions import ImproperlyConfigured
from django.core.files import File
from django.core.files.images import ImageFile
from django.test import TestCase
try:
    from .models import Image
except ImproperlyConfigured:
    Image = None
if Image:
    from .models import Person, TestImageFieldFile, temp_storage_dir
else:
    Person = None
    TestImageFieldFile = None