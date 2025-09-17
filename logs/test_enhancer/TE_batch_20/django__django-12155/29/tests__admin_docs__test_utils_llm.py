from unittest.mock import patch
from types import SimpleNamespace
from inspect import cleandoc
from django.test import RequestFactory
from django.apps import apps
import unittest
from types import SimpleNamespace
from inspect import cleandoc
from unittest.mock import patch
from django.test import RequestFactory
from django.apps import apps
from django.contrib.admindocs import views, utils
from .tests import AdminDocsSimpleTestCase
from django.contrib.admindocs.utils import docutils_is_available