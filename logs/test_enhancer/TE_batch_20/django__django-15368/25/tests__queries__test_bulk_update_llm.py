from django.db.models import Value, F, Case, When, Cast, IntegerField
from django.db.models.functions import Lower
from django.test import TestCase
from django.db.models import F, Value, Case, When, Cast, IntegerField
from django.db.models.functions import Lower
from .models import Note, Number, CustomDbColumn, Tag