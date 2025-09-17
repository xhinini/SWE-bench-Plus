from django.utils.translation import gettext_lazy as gettext_lazy
from django.utils.functional import Promise
from django.contrib.admin import TabularInline
from django.test import TestCase
from django.utils.translation import gettext_lazy as gettext_lazy, format_lazy
from django.utils.functional import Promise
from .admin import site as admin_site
from .models import Profile, ProfileCollection