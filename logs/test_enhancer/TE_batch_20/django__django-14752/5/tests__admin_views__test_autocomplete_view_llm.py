import json
from django.test import RequestFactory
from django.contrib import admin
import json
from contextlib import contextmanager
from django.contrib import admin
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.test import RequestFactory
from django.urls import reverse_lazy
from .admin import QuestionAdmin
from .models import Answer, Question, Employee, WorkHour, Manager, Bonus
from .tests import AdminViewBasicTestCase
ANSWER_OPTS = {'app_label': Answer._meta.app_label, 'model_name': Answer._meta.model_name, 'field_name': 'question'}