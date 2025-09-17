from django.contrib.messages.storage.cookie import MessageSerializer
import json
from django.contrib.messages import constants
from django.contrib.messages.storage.base import Message
from django.contrib.messages.storage.cookie import CookieStorage, MessageDecoder, MessageEncoder, MessageSerializer
from django.test import SimpleTestCase
from django.utils.safestring import SafeData, mark_safe
from .base import BaseTests