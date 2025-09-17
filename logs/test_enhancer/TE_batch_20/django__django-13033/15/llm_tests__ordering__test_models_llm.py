from django.test import SimpleTestCase
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.expressions import OrderBy, Value
from django.core.exceptions import FieldError