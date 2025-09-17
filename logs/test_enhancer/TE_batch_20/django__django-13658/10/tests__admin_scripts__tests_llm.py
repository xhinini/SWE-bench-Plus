from django.test.utils import captured_stdout, captured_stderr
from io import StringIO
from unittest import mock
from django.conf import settings
from django.core.management import ManagementUtility, execute_from_command_line
from django.test import SimpleTestCase
from django.test.utils import captured_stdout, captured_stderr