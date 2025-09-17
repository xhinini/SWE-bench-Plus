import json
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory
from django.urls import reverse_lazy
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
import json
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory
from django.urls import reverse_lazy
from .test_autocomplete_view import AdminViewBasicTestCase, site, Question, Answer, Employee, WorkHour, PAGINATOR_SIZE
from django.contrib.admin.views.autocomplete import AutocompleteJsonView