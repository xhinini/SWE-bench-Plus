from os import path
from django.utils.http import http_date
from django.views.static import was_modified_since
from ..urls import media_dir