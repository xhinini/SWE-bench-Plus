from django.test.utils import captured_stdout, captured_stderr
from io import StringIO
import os
from unittest import mock
from django.test import SimpleTestCase
from django.test.utils import captured_stdout, captured_stderr
from django.core.management import ManagementUtility, execute_from_command_line