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

from datetime import date, datetime
from django.test import SimpleTestCase
from django.utils import dateformat
from django.utils.dateformat import DateFormat, format as df_format
from datetime import date, datetime
from django.test import SimpleTestCase
from django.utils import dateformat
from django.utils.dateformat import DateFormat, format as df_format

class DateFormatYTests(SimpleTestCase):

    def setUp(self):
        from django.utils import translation
        self._orig_lang = translation.get_language()
        translation.activate('en-us')

    def tearDown(self):
        from django.utils import translation
        translation.activate(self._orig_lang)

from datetime import date, datetime
from django.test import SimpleTestCase, override_settings
from django.utils import translation
from django.utils import dateformat
from django.utils.dateformat import format as df_format

@override_settings(TIME_ZONE='Europe/Copenhagen')
class AdditionalDateFormatYTests(SimpleTestCase):

    def setUp(self):
        self._orig_lang = translation.get_language()
        translation.activate('en-us')

    def tearDown(self):
        translation.activate(self._orig_lang)

def test_Y_format_year_0001_datetime(self):
    self.assertEqual(dateformat.format(datetime(1, 1, 1), 'Y'), '0001')

def test_Y_format_year_0004_datetime(self):
    self.assertEqual(dateformat.format(datetime(4, 1, 1), 'Y'), '0004')

def test_Y_format_year_0042_date(self):
    self.assertEqual(dateformat.format(date(42, 1, 1), 'Y'), '0042')

def test_Y_format_year_0123_datetime(self):
    self.assertEqual(dateformat.format(datetime(123, 1, 1), 'Y'), '0123')

def test_Y_format_year_0999_datetime(self):
    self.assertEqual(dateformat.format(datetime(999, 1, 1), 'Y'), '0999')

def test_Y_format_year_1000_boundary(self):
    self.assertEqual(dateformat.format(datetime(1000, 1, 1), 'Y'), '1000')

def test_Y_format_year_9999_upper_bound(self):
    self.assertEqual(dateformat.format(datetime(9999, 12, 31), 'Y'), '9999')

def test_Y_return_type_is_string(self):
    result = dateformat.format(datetime(2023, 1, 1), 'Y')
    self.assertIsInstance(result, str)
    self.assertEqual(result, '2023')

def test_Y_concatenation_works(self):
    self.assertEqual(dateformat.format(datetime(123, 1, 1), 'Y') + 'year', '0123year')

def test_composite_format_Y_and_y(self):
    dt = datetime(5, 6, 7, 8, 9)
    self.assertEqual(dateformat.format(dt, 'Y y'), '0005 05')