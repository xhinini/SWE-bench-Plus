import json
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, override_settings
from django.contrib import admin
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.contrib.admin.tests import AdminSeleniumTestCase
from .admin import QuestionAdmin
from .models import Question
PAGINATOR_SIZE = AutocompleteJsonView.paginate_by