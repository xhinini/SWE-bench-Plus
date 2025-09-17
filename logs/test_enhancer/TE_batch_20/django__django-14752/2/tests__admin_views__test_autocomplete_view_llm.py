import json
from collections import OrderedDict
from django.contrib import admin
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.test import RequestFactory, TestCase
from .test_autocomplete_view import site, model_admin, PAGINATOR_SIZE
from .models import Question
from django.contrib.auth.models import User