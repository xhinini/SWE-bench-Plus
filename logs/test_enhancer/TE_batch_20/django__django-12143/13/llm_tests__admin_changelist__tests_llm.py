from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from .admin import SwallowAdmin, site as custom_site
from .models import Swallow
from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from .admin import SwallowAdmin, site as custom_site
from .models import Swallow