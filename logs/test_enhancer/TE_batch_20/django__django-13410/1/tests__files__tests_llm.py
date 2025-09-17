import os
import errno
from unittest import mock
import errno
import os
import unittest
from unittest import mock
from django.core.files import locks

@unittest.skipIf(os.name == 'nt', 'fcntl-based locking tests are POSIX only')
class LockingRegressionTests(unittest.TestCase):

    def test_lock_propagates_permission_error(self):
        err = PermissionError(errno.EACCES, 'Permission denied')
        with mock.patch('django.core.files.locks.fcntl.flock', side_effect=err):
            with self.assertRaises(PermissionError):
                locks.lock(4, locks.LOCK_EX)

    def test_lock_propagates_generic_oserror(self):
        err = OSError(errno.EACCES, 'Access error')
        with mock.patch('django.core.files.locks.fcntl.flock', side_effect=err):
            with self.assertRaises(OSError) as cm:
                locks.lock(6, locks.LOCK_EX)
            self.assertEqual(cm.exception.errno, errno.EACCES)

    def test_unlock_propagates_blockingio(self):
        with mock.patch('django.core.files.locks.fcntl.flock', side_effect=BlockingIOError):
            with self.assertRaises(BlockingIOError):
                locks.unlock(8)

    def test_unlock_propagates_permission_error(self):
        err = PermissionError(errno.EACCES, 'Permission denied')
        with mock.patch('django.core.files.locks.fcntl.flock', side_effect=err):
            with self.assertRaises(PermissionError):
                locks.unlock(9)