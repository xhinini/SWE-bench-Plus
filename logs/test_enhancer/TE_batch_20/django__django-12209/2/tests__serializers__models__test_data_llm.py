from django.test import TestCase
from unittest.mock import patch
from django.db import transaction, IntegrityError
from tests.serializers.models.data import UUIDDefaultData, BooleanPKData
from django.test import TestCase
from unittest.mock import patch
from django.db import transaction, IntegrityError
from tests.serializers.models.data import UUIDDefaultData, BooleanPKData