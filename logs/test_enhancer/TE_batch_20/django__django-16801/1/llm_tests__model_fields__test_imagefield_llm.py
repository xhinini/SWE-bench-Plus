from unittest import skipIf
from django.db.models import signals
from django.test import TestCase
try:
    from .models import Image
except Exception:
    Image = None
if Image:
    from .models import Person, PersonDimensionsFirst, PersonTwoImages, PersonWithHeight, PersonWithHeightAndWidth
else:
    Person = PersonDimensionsFirst = PersonTwoImages = PersonWithHeight = PersonWithHeightAndWidth = type('Dummy', (), {})