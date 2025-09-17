from unittest import mock
from django.db import connection
from django.db.utils import IntegrityError
from ..models import Object, ObjectReference