from django.test import TestCase
from django.core.exceptions import ValidationError
from django import forms
import datetime
from .models import Writer, Article

class ForeignKeyValidateBaseManagerTests(TestCase):

    def setUp(self):
        self.archived_writer = Writer._base_manager.create(name='Archived Writer', archived=True)
        self.visible_writer = Writer.objects.create(name='Visible Writer')