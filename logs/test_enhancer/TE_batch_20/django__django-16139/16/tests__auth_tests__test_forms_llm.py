from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
import re
import urllib.parse
from django.urls import reverse
from django.test import override_settings
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.test import override_settings
import re
import urllib.parse
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.test import TestCase