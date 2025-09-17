from django.test import TestCase
from django.core.exceptions import ValidationError
import datetime
from django.test import TestCase
from django.core.exceptions import ValidationError
from tests.model_forms import models as mf_models
Writer = mf_models.Writer
Article = mf_models.Article
WriterProfile = mf_models.WriterProfile