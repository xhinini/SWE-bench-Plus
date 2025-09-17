import re
from datetime import datetime
from operator import attrgetter
import re
from django.db.models import Count, Max, Value
from django.db.models.functions import Upper
from django.test import TestCase
from .models import Article, Author, ChildArticle