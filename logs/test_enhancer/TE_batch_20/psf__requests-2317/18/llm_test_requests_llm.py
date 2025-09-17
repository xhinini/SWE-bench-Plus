import io
import pytest
import requests
from requests import Request, Session, Response
'\nRegression tests for requests.sessions method conversion bug.\n\nThese tests ensure that bytes-like method inputs (bytes, bytearray)\nare converted to native str and uppercased correctly and that the\nliteral "b\'...\'" does not appear in the method (which would indicate\nbuiltin_str was used on a bytes object).\n'
import io
import pytest
import requests
from requests import Request, Session, Response