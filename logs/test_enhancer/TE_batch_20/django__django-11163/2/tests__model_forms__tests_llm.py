from django.test import TestCase
from django.forms.models import model_to_dict
from .models import Category, Colour, ColourfulItem, BetterWriter, Writer
from django.test import TestCase
from django.forms.models import model_to_dict
from .models import Category, Colour, ColourfulItem, BetterWriter, Writer

class ModelToDictRegressionTests(TestCase):

    def setUp(self):
        self.cat = Category.objects.create(name='Alpha', slug='alpha', url='alpha-url')
        self.blue = Colour.objects.create(name='blue')
        self.red = Colour.objects.create(name='red')
        self.item = ColourfulItem.objects.create()
        self.item.colours.set([self.blue, self.red])
        self.writer = Writer.objects.create(name='Writer Name')
        self.better = BetterWriter.objects.create(name='Better', score=5)