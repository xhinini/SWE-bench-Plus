import uuid
from django.test import override_settings
from .tests import ChangeListTests as BaseChangeListTests
from .admin import SwallowAdmin, site as custom_site
from .models import Swallow