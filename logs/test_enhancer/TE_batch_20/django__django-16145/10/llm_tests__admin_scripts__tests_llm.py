from io import StringIO
import socket
from unittest import mock, skipUnless
from django.core.management import call_command
from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.management.base import BaseCommand