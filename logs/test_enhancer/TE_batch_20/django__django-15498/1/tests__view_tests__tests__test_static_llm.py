from django.utils.http import http_date
from django.views.static import was_modified_since
from os import path
from ..urls import media_dir
from django.http import FileResponse