from unittest import skipIf
from django.core.files import File as DjangoFile
from django.core.files.images import ImageFile
from django.test import TestCase
try:
    from .models import Image
except Exception:
    Image = None
if Image:
    from .models import Person, PersonTwoImages, temp_storage_dir
else:
    Person = PersonTwoImages = None