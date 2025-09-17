import json
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory
from django.urls import reverse_lazy
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.contrib import admin
from .test_autocomplete_view import site
from .models import Question
from .tests import AdminViewBasicTestCase
import json
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory
from django.urls import reverse_lazy
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.contrib import admin
from .test_autocomplete_view import site
from .models import Question
from .tests import AdminViewBasicTestCase