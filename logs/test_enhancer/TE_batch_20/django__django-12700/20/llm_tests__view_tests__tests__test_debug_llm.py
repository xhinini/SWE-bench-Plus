from django.test import SimpleTestCase, override_settings
from django.views.debug import SafeExceptionReporterFilter, CallableSettingWrapper
from django.utils.encoding import force_str