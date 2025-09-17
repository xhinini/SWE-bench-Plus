from django.contrib import admin
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.test import RequestFactory
from .tests import AdminViewBasicTestCase
from django.contrib import admin
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.test import RequestFactory, override_settings
from django.urls import reverse_lazy
from django.core import serializers
import json
import datetime
from .admin import QuestionAdmin
from .models import Question
from .tests import AdminViewBasicTestCase
PAGINATOR_SIZE = AutocompleteJsonView.paginate_by
url = reverse_lazy('autocomplete_admin:autocomplete')
factory = RequestFactory()