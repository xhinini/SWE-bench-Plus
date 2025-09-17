import socket
import unittest
from io import StringIO
from unittest import mock
import socket
import unittest
from io import StringIO
from unittest import mock
from django.core.management import call_command
from django.core.management.base import BaseCommand
try:
    from django.core.management.commands.runserver import Command as RunserverCommand
except Exception:
    RunserverCommand = None