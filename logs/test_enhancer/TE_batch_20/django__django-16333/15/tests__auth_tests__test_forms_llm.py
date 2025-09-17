from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models.custom_user import CustomUser, CustomUserWithoutIsActiveField, ExtensionUser
from .models.with_many_to_many import CustomUserWithM2M, Organization