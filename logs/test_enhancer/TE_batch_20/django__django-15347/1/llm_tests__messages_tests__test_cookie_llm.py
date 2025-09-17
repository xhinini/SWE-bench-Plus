import binascii
import json
import json
import binascii
from django.contrib.messages import constants
from django.contrib.messages.storage.base import Message
from django.contrib.messages.storage.cookie import CookieStorage, MessageSerializer, MessageEncoder, MessageDecoder
from django.test import override_settings
from django.test import SimpleTestCase
from django.test.client import RequestFactory
from django.http import HttpResponse
from django.utils.safestring import mark_safe, SafeData

class CookieExtraTagsTests(SimpleTestCase):

    def setUp(self):
        self.rf = RequestFactory()

    def get_request(self):
        return self.rf.get('/')

    def get_storage(self):
        return CookieStorage(self.get_request())

    def get_response(self):
        return HttpResponse()