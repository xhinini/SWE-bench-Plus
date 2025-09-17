import os
import re
import shutil
import tempfile
import unittest
from hashlib import md5
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.storage import HashedFilesMixin, ManifestFilesMixin