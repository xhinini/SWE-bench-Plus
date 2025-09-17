from django.test import SimpleTestCase
from django.contrib.messages.storage.base import Message
from django.contrib.messages.storage.cookie import MessageEncoder, MessageDecoder, CookieStorage
from django.contrib.messages import constants
from .base import BaseTests
import json