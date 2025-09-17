import re
from datetime import datetime
from django.db.models import Count, Max, Value, CharField
from django.db.models.functions import Upper
from datetime import datetime
import re
from django.db.models import Count, Max, Value, CharField
from django.db.models.functions import Upper
from django.test import TestCase
from .models import Article, Author