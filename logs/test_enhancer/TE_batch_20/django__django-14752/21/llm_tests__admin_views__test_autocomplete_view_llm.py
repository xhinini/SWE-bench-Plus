import json
from django.contrib import admin
from django.test import RequestFactory
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from .models import Question, Employee, WorkHour, Manager, Bonus, PKChild, Toy
from .admin import QuestionAdmin
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType