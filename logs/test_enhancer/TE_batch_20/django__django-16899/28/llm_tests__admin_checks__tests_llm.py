from django.core import checks
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.test import SimpleTestCase, override_settings
from .models import Album, Book, City, Song, TwoAlbumFKAndAnE