from django.test import RequestFactory
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
import json
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.contrib import admin
from .test_autocomplete_view import site
from .admin import QuestionAdmin
from .models import Question, Answer, Employee, WorkHour, Manager, Bonus, PKChild, Toy
from .tests import AdminViewBasicTestCase
PAGINATOR_SIZE = AutocompleteJsonView.paginate_by