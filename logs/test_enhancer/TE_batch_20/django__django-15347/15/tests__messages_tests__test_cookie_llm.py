from django.contrib.messages.storage.cookie import MessageSerializer
from django.contrib.messages import constants
from django.contrib.messages.storage.base import Message
from django.contrib.messages.storage.cookie import CookieStorage, MessageDecoder, MessageEncoder
from django.test import SimpleTestCase, override_settings
import json