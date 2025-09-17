import django
from django.forms import models as forms_models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.test import TestCase
from .models.custom_user import CustomUser, CustomUserWithoutIsActiveField, ExtensionUser
from .models.with_custom_email_field import CustomEmailField
from .models.with_integer_username import IntegerUsernameUser
from .models.with_many_to_many import CustomUserWithM2M, Organization