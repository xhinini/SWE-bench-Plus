from unittest.mock import patch
import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase
from tests.model_forms import models as mf_models
from tests.model_forms.models import Article, Writer, WriterProfile, ImprovedArticleWithParentLink