from django.db import router
from django.test import TestCase
from django.urls import reverse
from django.db import DatabaseError
from unittest import mock
from admin_changelist.models import Swallow
from admin_changelist.admin import SwallowAdmin
from django.db import router