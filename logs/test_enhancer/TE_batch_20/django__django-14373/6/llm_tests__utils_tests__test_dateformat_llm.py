from django.test import SimpleTestCase, override_settings
from django.utils import translation, dateformat
from django.utils.dateformat import format as df_format
from datetime import date, datetime

@override_settings(TIME_ZONE='Europe/Copenhagen')
class DateFormatYRegressionTests(SimpleTestCase):

    def setUp(self):
        self._orig_lang = translation.get_language()
        translation.activate('en-us')

    def tearDown(self):
        translation.activate(self._orig_lang)