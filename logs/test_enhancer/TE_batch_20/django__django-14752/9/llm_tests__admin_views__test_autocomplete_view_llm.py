from django.urls import reverse_lazy
from django.test import RequestFactory
import json
from django.urls import reverse_lazy
from django.test import RequestFactory
import json
from .test_autocomplete_view import site, PAGINATOR_SIZE
from .tests import AdminViewBasicTestCase
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from .models import Question, Employee, WorkHour, Manager, Bonus, PKChild, Toy