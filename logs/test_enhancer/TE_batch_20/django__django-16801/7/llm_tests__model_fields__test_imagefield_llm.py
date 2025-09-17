from django.core.files.images import ImageFile
from unittest import skipIf
import os
import shutil
from django.core.exceptions import ImproperlyConfigured
from django.core.files.images import ImageFile
from django.test import TestCase
try:
    from .models import Image
except ImproperlyConfigured:
    Image = None
if Image:
    from .models import Person, PersonTwoImages, temp_storage_dir
else:
    PersonTwoImages = Person
    temp_storage_dir = None