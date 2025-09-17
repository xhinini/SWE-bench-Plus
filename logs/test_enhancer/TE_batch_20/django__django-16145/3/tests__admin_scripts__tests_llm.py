@mock.patch('django.core.management.commands.runserver.run')
@mock.patch('django.core.management.base.BaseCommand.check_migrations')
def test_starting_server_ipv4_address_print(self, *mocked_objects):
    self.output.truncate(0)
    self.output.seek(0)
    call_command('runserver', addrport='1.2.3.4:9000', use_reloader=False, skip_checks=True, stdout=self.output)
    self.assertIn('Starting development server at http://1.2.3.4:9000/', self.output.getvalue())

@mock.patch('django.core.management.commands.runserver.run')
@mock.patch('django.core.management.base.BaseCommand.check_migrations')
def test_starting_server_hostname_print(self, *mocked_objects):
    self.output.truncate(0)
    self.output.seek(0)
    call_command('runserver', addrport='test.domain.local:7000', use_reloader=False, skip_checks=True, stdout=self.output)
    self.assertIn('Starting development server at http://test.domain.local:7000/', self.output.getvalue())

@unittest.skipUnless(socket.has_ipv6, "platform doesn't support IPv6")
@mock.patch('django.core.management.commands.runserver.run')
@mock.patch('django.core.management.base.BaseCommand.check_migrations')
def test_starting_server_ipv6_bracketed_print(self, *mocked_objects):
    self.output.truncate(0)
    self.output.seek(0)
    call_command('runserver', addrport='[2001:0db8:1234:5678::9]:7000', use_reloader=False, skip_checks=True, stdout=self.output)
    self.assertIn('Starting development server at http://[2001:0db8:1234:5678::9]:7000/', self.output.getvalue())

@unittest.skipUnless(socket.has_ipv6, "platform doesn't support IPv6")
@mock.patch('django.core.management.commands.runserver.run')
@mock.patch('django.core.management.base.BaseCommand.check_migrations')
def test_use_ipv6_with_port_only_print(self, *mocked_objects):
    self.output.truncate(0)
    self.output.seek(0)
    call_command('runserver', addrport='7000', use_reloader=False, skip_checks=True, use_ipv6=True, stdout=self.output)
    self.assertIn('Starting development server at http://[::1]:7000/', self.output.getvalue())

@mock.patch('django.core.management.commands.runserver.run')
@mock.patch('django.core.management.base.BaseCommand.check_migrations')
def test_default_addr_override_print(self, *mocked_objects):
    self.output.truncate(0)
    self.output.seek(0)
    with mock.patch.object(RunserverCommand, 'default_addr', '0.0.0.0'):
        call_command('runserver', use_reloader=False, skip_checks=True, stdout=self.output)
    self.assertIn('Starting development server at http://0.0.0.0:8000/', self.output.getvalue())

@mock.patch('django.core.management.commands.runserver.run')
@mock.patch('django.core.management.base.BaseCommand.check_migrations')
def test_zero_addr_with_custom_port_print(self, *mocked_objects):
    self.output.truncate(0)
    self.output.seek(0)
    call_command('runserver', addrport='0:9001', use_reloader=False, skip_checks=True, stdout=self.output)
    self.assertIn('Starting development server at http://0.0.0.0:9001/', self.output.getvalue())

@unittest.skipUnless(socket.has_ipv6, "platform doesn't support IPv6")
@mock.patch('django.core.management.commands.runserver.run')
@mock.patch('django.core.management.base.BaseCommand.check_migrations')
def test_default_addr_ipv6_override_print(self, *mocked_objects):
    self.output.truncate(0)
    self.output.seek(0)
    with mock.patch.object(RunserverCommand, 'default_addr_ipv6', '::'):
        call_command('runserver', use_reloader=False, skip_checks=True, use_ipv6=True, stdout=self.output)
    self.assertIn('Starting development server at http://[::]:8000/', self.output.getvalue())

def test_invalid_ipv6_without_brackets_raises(self):
    msg = '"2001:0db8:1234:5678::9:7000" is not a valid port number or address:port pair.'
    with self.assertRaisesMessage(CommandError, msg):
        call_command('runserver', addrport='2001:0db8:1234:5678::9:7000', use_reloader=False, skip_checks=True)

def test_ipv4_with_use_ipv6_flag_raises(self):
    msg = '"1.2.3.4" is not a valid IPv6 address.'
    with self.assertRaisesMessage(CommandError, msg):
        call_command('runserver', addrport='1.2.3.4:8000', use_reloader=False, skip_checks=True, use_ipv6=True)

@unittest.skipUnless(socket.has_ipv6, "platform doesn't support IPv6")
@mock.patch('django.core.management.commands.runserver.run')
@mock.patch('django.core.management.base.BaseCommand.check_migrations')
def test_bracketed_ipv6_with_explicit_port_print(self, *mocked_objects):
    self.output.truncate(0)
    self.output.seek(0)
    call_command('runserver', addrport='[fe80::1]:8080', use_reloader=False, skip_checks=True, stdout=self.output)
    self.assertIn('Starting development server at http://[fe80::1]:8080/', self.output.getvalue())

from io import StringIO
from unittest import mock
import socket
import unittest
from django.core.management import call_command
from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.management.base import BaseCommand

class RunserverAddressFormattingTests(unittest.TestCase):

    def setUp(self):
        self.stdout = StringIO()