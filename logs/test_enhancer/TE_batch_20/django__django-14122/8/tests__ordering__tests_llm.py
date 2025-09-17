from django.db.models import CharField
from datetime import datetime
import re
from django.db.models import Count, F, Max, Value, CharField
from django.db.models.functions import Upper
from django.test import TestCase
from .models import Article, Author