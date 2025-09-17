from django.test import RequestFactory, override_settings
from django.urls import reverse_lazy
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.contrib.admin.tests import AdminViewBasicTestCase
import json
from .test_autocomplete_view import site, Question, Employee, WorkHour, Manager, Bonus, PKChild, Toy
from django.test import RequestFactory, override_settings
from django.urls import reverse_lazy
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.contrib.admin.tests import AdminViewBasicTestCase
import json
from .test_autocomplete_view import site, Question, Employee, WorkHour, Manager, Bonus, PKChild, Toy
PAGINATOR_SIZE = AutocompleteJsonView.paginate_by
ExtraSerializeResultTests = override_settings(ROOT_URLCONF='admin_views.urls')(ExtraSerializeResultTests)