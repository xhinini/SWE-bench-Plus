import socket
from io import StringIO
from unittest import mock
from django.core.management import call_command
from django.core.management.commands.runserver import Command as RunserverCommand
from django.test import SimpleTestCase