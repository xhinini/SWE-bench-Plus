from unittest import skipIf
from django.test import TestCase
try:
    from .models import Image
except Exception:
    Image = None
if Image:
    from .models import Person, PersonTwoImages, temp_storage_dir
else:
    Person = PersonTwoImages = None