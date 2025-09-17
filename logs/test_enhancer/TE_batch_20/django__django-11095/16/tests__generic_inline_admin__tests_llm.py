from django.contrib import admin
from django.test import TestCase, RequestFactory, override_settings
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from generic_inline_admin.admin import MediaInline, MediaPermanentInline, site as admin_site
from generic_inline_admin.models import Episode, Media