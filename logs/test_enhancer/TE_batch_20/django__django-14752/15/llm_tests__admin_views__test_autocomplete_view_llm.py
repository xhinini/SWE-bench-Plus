import inspect
import json
from types import SimpleNamespace
from django.test import SimpleTestCase, RequestFactory
from django.contrib.admin.views import autocomplete
from django.contrib.admin.views.autocomplete import AutocompleteJsonView