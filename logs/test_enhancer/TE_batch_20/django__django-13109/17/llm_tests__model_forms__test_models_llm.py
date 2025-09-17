from django.test import TestCase
from django.db.models import Q
from django.core.exceptions import ValidationError
from tests.model_forms.models import Writer, Article, ImprovedArticleWithParentLink, Inventory