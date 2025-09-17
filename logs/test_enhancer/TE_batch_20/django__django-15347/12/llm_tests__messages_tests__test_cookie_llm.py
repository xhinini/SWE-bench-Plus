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

from django.contrib.messages.storage.cookie import MessageSerializer

def test_regression_empty_extra_tags_json(self):
    """
    A Message with extra_tags == '' must be preserved by MessageEncoder/MessageDecoder.
    """
    encoder = MessageEncoder()
    msg = Message(constants.INFO, 'hello', extra_tags='')
    value = encoder.encode(msg)
    decoded = json.loads(value, cls=MessageDecoder)
    self.assertEqual(decoded.extra_tags, '')

def test_regression_empty_extra_tags_nested_structure(self):
    """
    An empty-string extra_tags inside a nested structure must be preserved.
    """
    nested = {'level1': [Message(constants.INFO, 'one', extra_tags=''), {'inner': Message(constants.WARNING, 'warn', extra_tags=None)}]}
    encoder = MessageEncoder()
    value = encoder.encode(nested)
    decoded = json.loads(value, cls=MessageDecoder)
    self.assertEqual(decoded['level1'][0].extra_tags, '')
    self.assertIsNone(decoded['level1'][1]['inner'].extra_tags)

def test_regression_serializer_preserves_empty_extra_tags(self):
    """
    MessageSerializer.dumps/loads should preserve empty-string extra_tags.
    """
    serializer = MessageSerializer()
    msgs = [Message(constants.INFO, 'a', extra_tags='')]
    data = serializer.dumps(msgs)
    result = serializer.loads(data)
    self.assertEqual(result[0].extra_tags, '')

def test_regression_cookie_roundtrip_preserves_empty_extra_tags(self):
    """
    Storing a message with extra_tags == '' in CookieStorage must preserve it.
    """
    storage = self.get_storage()
    response = self.get_response()
    storage.add(constants.INFO, 'cookie-test', extra_tags='')
    storage.update(response)
    cookie_value = response.cookies['messages'].value
    decoded = storage._decode(cookie_value)
    self.assertEqual(decoded[0].extra_tags, '')

def test_regression_zero_extra_tags_json(self):
    """
    An extra_tags value of 0 (numeric zero) must be preserved by the encoder/decoder.
    """
    encoder = MessageEncoder()
    msg = Message(constants.INFO, 'num', extra_tags=0)
    value = encoder.encode(msg)
    decoded = json.loads(value, cls=MessageDecoder)
    self.assertEqual(decoded.extra_tags, 0)

def test_regression_false_extra_tags_json(self):
    """
    An extra_tags value of False must be preserved by the encoder/decoder.
    """
    encoder = MessageEncoder()
    msg = Message(constants.INFO, 'bool', extra_tags=False)
    value = encoder.encode(msg)
    decoded = json.loads(value, cls=MessageDecoder)
    self.assertIs(decoded.extra_tags, False)

def test_regression_nested_false_extra_tags(self):
    """
    A nested False extra_tags value should be preserved in complex structures.
    """
    structure = [Message(constants.INFO, 'm', extra_tags=False), {'m2': Message(constants.ERROR, 'e', extra_tags='')}]
    encoder = MessageEncoder()
    value = encoder.encode(structure)
    decoded = json.loads(value, cls=MessageDecoder)
    self.assertIs(decoded[0].extra_tags, False)
    self.assertEqual(decoded[1]['m2'].extra_tags, '')

def test_regression_serializer_preserves_mixed_extra_tags(self):
    """
    MessageSerializer should preserve a variety of extra_tags values including '', None, False, 0 and strings.
    """
    serializer = MessageSerializer()
    msgs = [Message(constants.INFO, 'a', extra_tags=''), Message(constants.INFO, 'b', extra_tags=None), Message(constants.INFO, 'c', extra_tags=False), Message(constants.INFO, 'd', extra_tags=0), Message(constants.INFO, 'e', extra_tags='tags')]
    data = serializer.dumps(msgs)
    result = serializer.loads(data)
    expected = ['', None, False, 0, 'tags']
    self.assertEqual([m.extra_tags for m in result], expected)

def test_regression_cookie_store_restore_various_extra_tags(self):
    """
    CookieStorage must preserve mixed extra_tags values when multiple messages are stored.
    """
    storage = self.get_storage()
    response = self.get_response()
    storage.add(constants.INFO, 'a', extra_tags='')
    storage.add(constants.INFO, 'b', extra_tags=None)
    storage.add(constants.INFO, 'c', extra_tags=False)
    storage.add(constants.INFO, 'd', extra_tags=0)
    storage.add(constants.INFO, 'e', extra_tags='tags')
    storage.update(response)
    cookie_value = response.cookies['messages'].value
    decoded = storage._decode(cookie_value)
    expected = ['', None, False, 0, 'tags']
    self.assertEqual([m.extra_tags for m in decoded], expected)

from django.test import SimpleTestCase, override_settings
from django.contrib.messages.storage.cookie import CookieStorage, MessageDecoder, MessageEncoder
from django.contrib.messages.storage.base import Message
from django.contrib.messages import constants
from django.utils.safestring import mark_safe
import json

@override_settings(SESSION_COOKIE_DOMAIN='.example.com', SESSION_COOKIE_SECURE=True, SESSION_COOKIE_HTTPONLY=True)
class ExtraTagsRegressionTests(SimpleTestCase):
    storage_class = CookieStorage

    def get_storage(self):
        return self.storage_class(self._get_request())

    def _get_request(self):

        class DummyRequest:
            COOKIES = {}
        return DummyRequest()

    def _get_response(self):
        from django.http import HttpResponse
        return HttpResponse()

def test_serializer_preserves_empty_string_extra_tags(self):
    """MessageSerializer should preserve empty-string extra_tags"""
    storage = self.get_storage()
    msg = Message(constants.INFO, 'hello', extra_tags='')
    serializer = MessageSerializer()
    encoded = serializer.dumps([msg])
    decoded = serializer.loads(encoded)
    self.assertEqual(len(decoded), 1)
    self.assertEqual(decoded[0].extra_tags, '')

def test_json_encoder_decoder_preserves_empty_string_extra_tags(self):
    """json.dumps/loads with MessageEncoder/MessageDecoder should preserve empty-string extra_tags"""
    msg = Message(constants.INFO, 'hello', extra_tags='')
    value = json.dumps([msg], cls=MessageEncoder)
    decoded = json.loads(value, cls=MessageDecoder)
    self.assertEqual(len(decoded), 1)
    self.assertEqual(decoded[0].extra_tags, '')

def test_serializer_preserves_false_extra_tags(self):
    """MessageSerializer should preserve False extra_tags"""
    msg = Message(constants.INFO, 'hello', extra_tags=False)
    serializer = MessageSerializer()
    decoded = serializer.loads(serializer.dumps([msg]))
    self.assertEqual(decoded[0].extra_tags, False)
    self.assertIs(decoded[0].extra_tags, False)

def test_serializer_preserves_zero_extra_tags(self):
    """MessageSerializer should preserve 0 extra_tags"""
    msg = Message(constants.INFO, 'num', extra_tags=0)
    serializer = MessageSerializer()
    decoded = serializer.loads(serializer.dumps([msg]))
    self.assertEqual(decoded[0].extra_tags, 0)
    self.assertIsInstance(decoded[0].extra_tags, int)

def test_serializer_preserves_empty_list_extra_tags(self):
    """MessageSerializer should preserve [] extra_tags"""
    msg = Message(constants.INFO, 'list', extra_tags=[])
    serializer = MessageSerializer()
    decoded = serializer.loads(serializer.dumps([msg]))
    self.assertEqual(decoded[0].extra_tags, [])
    self.assertIsInstance(decoded[0].extra_tags, list)

def test_serializer_preserves_empty_dict_extra_tags(self):
    """MessageSerializer should preserve {} extra_tags"""
    msg = Message(constants.INFO, 'dict', extra_tags={})
    serializer = MessageSerializer()
    decoded = serializer.loads(serializer.dumps([msg]))
    self.assertEqual(decoded[0].extra_tags, {})
    self.assertIsInstance(decoded[0].extra_tags, dict)

def test_cookie_storage_roundtrip_preserves_empty_string_extra_tags(self):
    """CookieStorage._encode/_decode roundtrip should preserve empty-string extra_tags"""
    storage = self.get_storage()
    msg = Message(constants.INFO, 'cookie', extra_tags='')
    encoded = storage._encode([msg])
    decoded = storage._decode(encoded)
    self.assertEqual(decoded[0].extra_tags, '')

def test_cookie_storage_roundtrip_preserves_various_falsey_extra_tags(self):
    """CookieStorage roundtrip preserves multiple falsey extra_tags values and types"""
    storage = self.get_storage()
    messages = [Message(constants.INFO, 'a', extra_tags=''), Message(constants.INFO, 'b', extra_tags=0), Message(constants.INFO, 'c', extra_tags=False), Message(constants.INFO, 'd', extra_tags=[]), Message(constants.INFO, 'e', extra_tags={})]
    encoded = storage._encode(messages)
    decoded = storage._decode(encoded)
    self.assertEqual(len(decoded), 5)
    self.assertEqual(decoded[0].extra_tags, '')
    self.assertEqual(decoded[1].extra_tags, 0)
    self.assertEqual(decoded[2].extra_tags, False)
    self.assertEqual(decoded[3].extra_tags, [])
    self.assertEqual(decoded[4].extra_tags, {})

def test_nested_structure_preserves_empty_string_extra_tags(self):
    """Nested structures containing Message with empty-string extra_tags are preserved"""
    nested = {'level1': [{'msg': Message(constants.INFO, 'nested', extra_tags='')}]}
    value = json.dumps(nested, cls=MessageEncoder)
    decoded = json.loads(value, cls=MessageDecoder)
    self.assertIn('level1', decoded)
    self.assertEqual(decoded['level1'][0]['msg'].extra_tags, '')

def test_signer_roundtrip_preserves_falsey_extra_tags(self):
    """Signing via CookieStorage._encode/_decode should preserve falsey-but-not-None extra_tags"""
    storage = self.get_storage()
    messages = [Message(constants.INFO, 'x', extra_tags=''), Message(constants.INFO, 'y', extra_tags=0)]
    signed = storage._encode(messages)
    unsigned = storage._decode(signed)
    self.assertEqual(unsigned[0].extra_tags, '')
    self.assertEqual(unsigned[1].extra_tags, 0)

def test_encoder_preserves_zero_extra_tags(self):
    encoder = MessageEncoder()
    msg = Message(constants.DEBUG, 'hello', extra_tags=0)
    value = encoder.encode(msg)
    decoded = json.loads(value, cls=MessageDecoder)
    self.assertEqual(decoded.extra_tags, 0)

def test_encoder_preserves_false_extra_tags(self):
    encoder = MessageEncoder()
    msg = Message(constants.DEBUG, 'hello', extra_tags=False)
    value = encoder.encode(msg)
    decoded = json.loads(value, cls=MessageDecoder)
    self.assertIs(decoded.extra_tags, False)

def test_encoder_preserves_empty_list_extra_tags(self):
    encoder = MessageEncoder()
    msg = Message(constants.DEBUG, 'hello', extra_tags=[])
    value = encoder.encode(msg)
    decoded = json.loads(value, cls=MessageDecoder)
    self.assertEqual(decoded.extra_tags, [])

def test_encoder_preserves_empty_string_in_nested_structure(self):
    messages = {'a': [Message(constants.INFO, 'x', extra_tags='')]}
    encoded = json.dumps(messages, cls=MessageEncoder)
    decoded = json.loads(encoded, cls=MessageDecoder)
    self.assertIn('a', decoded)
    self.assertEqual(decoded['a'][0].extra_tags, '')

def test_encoder_preserves_zero_in_nested_structure(self):
    messages = {'a': {'b': Message(constants.INFO, 'x', extra_tags=0)}}
    encoded = json.dumps(messages, cls=MessageEncoder)
    decoded = json.loads(encoded, cls=MessageDecoder)
    self.assertEqual(decoded['a']['b'].extra_tags, 0)

def test_storage_encode_decode_empty_string_extra_tags(self):
    storage = self.get_storage()
    msg = Message(constants.DEBUG, 'm', extra_tags='')
    encoded = storage._encode(msg)
    decoded = storage._decode(encoded)
    self.assertEqual(decoded.extra_tags, '')

def test_storage_encode_decode_false_extra_tags(self):
    storage = self.get_storage()
    msg = Message(constants.DEBUG, 'm', extra_tags=False)
    encoded = storage._encode(msg)
    decoded = storage._decode(encoded)
    self.assertIs(decoded.extra_tags, False)

def test_serializer_roundtrip_empty_string_extra_tags(self):
    serializer = MessageSerializer()
    msg = Message(constants.DEBUG, 'm', extra_tags='')
    data = serializer.dumps(msg)
    loaded = serializer.loads(data)
    self.assertEqual(loaded.extra_tags, '')

def test_serializer_roundtrip_false_extra_tags(self):
    serializer = MessageSerializer()
    msg = Message(constants.DEBUG, 'm', extra_tags=False)
    data = serializer.dumps(msg)
    loaded = serializer.loads(data)
    self.assertIs(loaded.extra_tags, False)

def test_encode_decode_multiple_messages_mixed_extra_tags(self):
    encoder = MessageEncoder()
    messages = [Message(constants.INFO, 'a', extra_tags=''), Message(constants.INFO, 'b', extra_tags=0), Message(constants.INFO, 'c', extra_tags=None), Message(constants.INFO, 'd', extra_tags='tags')]
    encoded = encoder.encode(messages)
    decoded = json.loads(encoded, cls=MessageDecoder)
    self.assertEqual(decoded[0].extra_tags, '')
    self.assertEqual(decoded[1].extra_tags, 0)
    self.assertIs(decoded[2].extra_tags, None)
    self.assertEqual(decoded[3].extra_tags, 'tags')