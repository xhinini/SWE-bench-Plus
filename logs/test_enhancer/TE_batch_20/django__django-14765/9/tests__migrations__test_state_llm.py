from django.db.migrations.state import ModelState
from django.apps import apps as global_apps
from django.apps.registry import Apps
from django.test import SimpleTestCase
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.migrations.state import ProjectState, ModelState, StateApps
import types