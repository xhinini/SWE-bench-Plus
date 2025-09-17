import errno
import os
import socket
import sys
from io import StringIO
from unittest import mock
import unittest
from django.core.management import call_command
from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.management.base import BaseCommand