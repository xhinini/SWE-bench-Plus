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