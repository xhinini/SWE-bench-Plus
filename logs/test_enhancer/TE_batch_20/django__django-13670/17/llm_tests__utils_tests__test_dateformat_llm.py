def test_y_single_digit_year(self):
    self.assertEqual(dateformat.format(datetime(7, 9, 8, 5, 0), 'y'), '07')

def test_y_year_100_returns_00(self):
    self.assertEqual(dateformat.format(datetime(100, 1, 1, 0, 0), 'y'), '00')

def test_y_year_2000_returns_00(self):
    self.assertEqual(dateformat.format(datetime(2000, 6, 15, 12, 0), 'y'), '00')

def test_y_year_1999_returns_99(self):
    self.assertEqual(dateformat.format(datetime(1999, 12, 31, 23, 59), 'y'), '99')

def test_y_year_123_returns_23(self):
    self.assertEqual(dateformat.format(datetime(123, 4, 5, 6, 7), 'y'), '23')

def test_y_date_object_returns_two_digits(self):
    self.assertEqual(dateformat.format(date(2001, 1, 1), 'y'), '01')

def test_y_using_dateformat_class_directly(self):
    df = dateformat.DateFormat(datetime(9, 2, 3, 4, 5))
    self.assertEqual(df.format('y'), '09')

def test_y_combined_with_Y(self):
    self.assertEqual(dateformat.format(datetime(100, 10, 10, 0, 0), 'Y y'), '100 00')

def test_y_max_year_9999(self):
    self.assertEqual(dateformat.format(datetime(9999, 1, 1, 0, 0), 'y'), '99')

def test_y_two_digit_year_99(self):
    self.assertEqual(dateformat.format(datetime(99, 3, 3, 0, 0), 'y'), '99')

from datetime import datetime
from django.test import SimpleTestCase, override_settings
from django.utils import dateformat, translation

@override_settings(TIME_ZONE='Europe/Copenhagen')
class DateFormatYRegressionTests(SimpleTestCase):

    def setUp(self):
        self._orig_lang = translation.get_language()
        translation.activate('en-us')

    def tearDown(self):
        translation.activate(self._orig_lang)

from datetime import datetime
from django.utils.dateformat import format

def test_year_format_1():
    assert format(datetime(1, 9, 8, 5, 0), 'y') == '01'

def test_year_format_9():
    assert format(datetime(9, 9, 8, 5, 0), 'y') == '09'

def test_year_format_12():
    assert format(datetime(12, 9, 8, 5, 0), 'y') == '12'

def test_year_format_99():
    assert format(datetime(99, 9, 8, 5, 0), 'y') == '99'

def test_year_format_100():
    assert format(datetime(100, 9, 8, 5, 0), 'y') == '00'

def test_year_format_101():
    assert format(datetime(101, 9, 8, 5, 0), 'y') == '01'

def test_year_format_123():
    assert format(datetime(123, 9, 8, 5, 0), 'y') == '23'

def test_year_format_200():
    assert format(datetime(200, 9, 8, 5, 0), 'y') == '00'

def test_year_format_909():
    assert format(datetime(909, 9, 8, 5, 0), 'y') == '09'

def test_year_format_999():
    assert format(datetime(999, 9, 8, 5, 0), 'y') == '99'

from datetime import date, datetime
from django.test import SimpleTestCase
from django.utils import dateformat, translation

class DateFormatYearEdgeCasesTests(SimpleTestCase):

    def setUp(self):
        self._orig_lang = translation.get_language()
        translation.activate('en-us')

    def tearDown(self):
        translation.activate(self._orig_lang)

def test_y_year_10(self):
    self.assertEqual(dateformat.format(datetime(10, 9, 8, 5, 0), 'y'), '10')

def test_y_year_1(self):
    self.assertEqual(dateformat.format(datetime(1, 9, 8, 5, 0), 'y'), '01')

def test_y_year_99(self):
    self.assertEqual(dateformat.format(datetime(99, 9, 8, 5, 0), 'y'), '99')

def test_y_year_100(self):
    self.assertEqual(dateformat.format(datetime(100, 9, 8, 5, 0), 'y'), '00')

def test_y_year_101(self):
    self.assertEqual(dateformat.format(datetime(101, 9, 8, 5, 0), 'y'), '01')

def test_y_year_123(self):
    self.assertEqual(dateformat.format(datetime(123, 9, 8, 5, 0), 'y'), '23')

def test_y_year_999(self):
    self.assertEqual(dateformat.format(datetime(999, 9, 8, 5, 0), 'y'), '99')

def test_y_year_1000(self):
    self.assertEqual(dateformat.format(datetime(1000, 9, 8, 5, 0), 'y'), '00')

def test_y_year_2003(self):
    self.assertEqual(dateformat.format(datetime(2003, 9, 8, 5, 0), 'y'), '03')

def test_y_year_200(self):
    self.assertEqual(dateformat.format(datetime(200, 9, 8, 5, 0), 'y'), '00')

def test_year_two_digit_edge_cases(self):
    """
    Regression tests for two-digit year formatting ('y'). Verify a variety of years,
    including 1-digit, 2-digit, 3-digit, centuries and millennium boundaries, produce
    the expected zero-padded two-digit result.
    """
    cases = [(1, '01'), (10, '10'), (90, '90'), (100, '00'), (123, '23'), (200, '00'), (201, '01'), (999, '99'), (1000, '00'), (1900, '00')]
    for year, expected in cases:
        with self.subTest(year=year):
            self.assertEqual(dateformat.format(datetime(year, 9, 8, 5, 0), 'y'), expected)