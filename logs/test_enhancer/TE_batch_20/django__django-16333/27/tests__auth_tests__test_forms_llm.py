from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models.with_many_to_many import CustomUserWithM2M, Organization
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models.with_many_to_many import CustomUserWithM2M, Organization