import os
import tempfile
import unittest
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage