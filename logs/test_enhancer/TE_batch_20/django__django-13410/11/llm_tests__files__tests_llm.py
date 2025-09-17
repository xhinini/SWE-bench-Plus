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

import os
import tempfile
from unittest import mock
import os
import tempfile
import unittest
from unittest import mock
from django.core.files import locks

@unittest.skipIf(os.name == 'nt', 'fcntl-only tests')
class LocksModuleTests(unittest.TestCase):

    def test_lock_propagates_non_blocking_oserror(self):
        with mock.patch('django.core.files.locks.fcntl.flock', side_effect=PermissionError):
            with tempfile.NamedTemporaryFile() as tf:
                with self.assertRaises(PermissionError):
                    locks.lock(tf, locks.LOCK_EX)

    def test_unlock_propagates_oserror_on_failure(self):
        with mock.patch('django.core.files.locks.fcntl.flock', side_effect=OSError):
            with tempfile.NamedTemporaryFile() as tf:
                with self.assertRaises(OSError):
                    locks.unlock(tf)

    def test_unlock_propagates_blockingioerror_on_failure(self):
        with mock.patch('django.core.files.locks.fcntl.flock', side_effect=BlockingIOError):
            with tempfile.NamedTemporaryFile() as tf:
                with self.assertRaises(BlockingIOError):
                    locks.unlock(tf)

import errno
import tempfile
import unittest
from unittest import mock
from django.core.files import locks
import errno
import tempfile
import unittest
from unittest import mock
from django.core.files import locks

@unittest.skipUnless(hasattr(locks, 'fcntl'), 'fcntl required for these tests')
class LocksExceptionAndReturnBehaviorTests(unittest.TestCase):

    def test_lock_propagates_oserror_from_flock_fileobj(self):
        with mock.patch('django.core.files.locks.fcntl.flock', side_effect=OSError(errno.EINVAL, 'invalid')):
            with tempfile.TemporaryFile() as temp:
                with self.assertRaises(OSError):
                    locks.lock(temp, locks.LOCK_EX)

    def test_lock_propagates_permissionerror_from_flock_fd(self):
        perm_err = PermissionError(errno.EACCES, 'permission denied')
        with mock.patch('django.core.files.locks.fcntl.flock', side_effect=perm_err):
            with tempfile.TemporaryFile() as temp:
                fd = temp.fileno()
                with self.assertRaises(PermissionError):
                    locks.lock(fd, locks.LOCK_EX)

    def test_unlock_propagates_oserror_from_flock_fileobj(self):
        with mock.patch('django.core.files.locks.fcntl.flock', side_effect=OSError(errno.EIO, 'i/o error')):
            with tempfile.TemporaryFile() as temp:
                with self.assertRaises(OSError):
                    locks.unlock(temp)

    def test_unlock_propagates_permissionerror_from_flock_fd(self):
        perm_err = PermissionError(errno.EPERM, 'operation not permitted')
        with mock.patch('django.core.files.locks.fcntl.flock', side_effect=perm_err):
            with tempfile.TemporaryFile() as temp:
                fd = temp.fileno()
                with self.assertRaises(PermissionError):
                    locks.unlock(fd)

import os
import tempfile
import unittest
from unittest import mock
from django.core.files import locks

@unittest.skipIf(os.name == 'nt', 'These tests exercise fcntl-based locking and are POSIX-only')
class LocksRegressionTests(unittest.TestCase):

    def test_unlock_blockingio_propagates_fileobj(self):
        with tempfile.TemporaryFile() as f:
            with mock.patch('django.core.files.locks.fcntl.flock', side_effect=BlockingIOError()):
                with self.assertRaises(BlockingIOError):
                    locks.unlock(f)

    def test_lock_permissionerror_propagates_fileobj(self):
        with tempfile.TemporaryFile() as f:
            with mock.patch('django.core.files.locks.fcntl.flock', side_effect=PermissionError('denied')):
                with self.assertRaises(PermissionError):
                    locks.lock(f, locks.LOCK_EX)

    def test_unlock_permissionerror_propagates_fileobj(self):
        with tempfile.TemporaryFile() as f:
            with mock.patch('django.core.files.locks.fcntl.flock', side_effect=PermissionError('denied')):
                with self.assertRaises(PermissionError):
                    locks.unlock(f)

    def test_lock_permissionerror_propagates_fd(self):
        with tempfile.TemporaryFile() as f:
            fd = f.fileno()
            with mock.patch('django.core.files.locks.fcntl.flock', side_effect=PermissionError('denied')):
                with self.assertRaises(PermissionError):
                    locks.lock(fd, locks.LOCK_SH)

    def test_unlock_permissionerror_propagates_fd(self):
        with tempfile.TemporaryFile() as f:
            fd = f.fileno()
            with mock.patch('django.core.files.locks.fcntl.flock', side_effect=PermissionError('denied')):
                with self.assertRaises(PermissionError):
                    locks.unlock(fd)

import os
import tempfile
import unittest
from unittest import mock
from django.core.files import locks
import os
import tempfile
import unittest
from unittest import mock
from django.core.files import locks

@unittest.skipIf(os.name == 'nt', 'POSIX-only tests')
class LocksRegressionTests(unittest.TestCase):

    def test_lock_propagates_unrelated_OSError_with_fileobj(self):
        with tempfile.TemporaryFile() as tmp:
            err = PermissionError('permission denied')
            with mock.patch('django.core.files.locks.fcntl.flock', side_effect=err):
                with self.assertRaises(PermissionError):
                    locks.lock(tmp, locks.LOCK_EX)

    def test_lock_propagates_unrelated_OSError_with_fd(self):
        with tempfile.TemporaryFile() as tmp:
            fd = tmp.fileno()
            err = PermissionError('permission denied')
            with mock.patch('django.core.files.locks.fcntl.flock', side_effect=err):
                with self.assertRaises(PermissionError):
                    locks.lock(fd, locks.LOCK_EX)

    def test_unlock_propagates_unrelated_OSError_with_fileobj(self):
        with tempfile.TemporaryFile() as tmp:
            err = PermissionError('permission denied')
            with mock.patch('django.core.files.locks.fcntl.flock', side_effect=err):
                with self.assertRaises(PermissionError):
                    locks.unlock(tmp)

    def test_unlock_propagates_unrelated_OSError_with_fd(self):
        with tempfile.TemporaryFile() as tmp:
            fd = tmp.fileno()
            err = PermissionError('permission denied')
            with mock.patch('django.core.files.locks.fcntl.flock', side_effect=err):
                with self.assertRaises(PermissionError):
                    locks.unlock(fd)

import os
import tempfile
import unittest
from unittest import mock
from django.core.files import locks
import fcntl
import os
import tempfile
import unittest
from unittest import mock
from django.core.files import locks
import fcntl

@unittest.skipIf(os.name == 'nt', 'POSIX fcntl tests')
class LocksRegressionTests(unittest.TestCase):

    def test_lock_propagates_permission_error(self):
        with tempfile.TemporaryFile() as f:
            with mock.patch('fcntl.flock', side_effect=PermissionError('perm')):
                with self.assertRaises(PermissionError):
                    locks.lock(f, locks.LOCK_EX)

    def test_unlock_propagates_permission_error(self):
        with tempfile.TemporaryFile() as f:
            with mock.patch('fcntl.flock', side_effect=PermissionError('perm')):
                with self.assertRaises(PermissionError):
                    locks.unlock(f)

    def test_lock_propagates_generic_os_error(self):
        with tempfile.TemporaryFile() as f:
            with mock.patch('fcntl.flock', side_effect=OSError('boom')):
                with self.assertRaises(OSError):
                    locks.lock(f, locks.LOCK_EX)

    def test_unlock_propagates_generic_os_error(self):
        with tempfile.TemporaryFile() as f:
            with mock.patch('fcntl.flock', side_effect=OSError('boom')):
                with self.assertRaises(OSError):
                    locks.unlock(f)

    def test_unlock_propagates_blockingioerror(self):
        with tempfile.TemporaryFile() as f:
            with mock.patch('fcntl.flock', side_effect=BlockingIOError):
                with self.assertRaises(BlockingIOError):
                    locks.unlock(f)

    def test_lock_propagates_filenotfounderror(self):
        with tempfile.TemporaryFile() as f:
            with mock.patch('fcntl.flock', side_effect=FileNotFoundError('no')):
                with self.assertRaises(FileNotFoundError):
                    locks.lock(f, locks.LOCK_EX)

    def test_unlock_propagates_filenotfounderror(self):
        with tempfile.TemporaryFile() as f:
            with mock.patch('fcntl.flock', side_effect=FileNotFoundError('no')):
                with self.assertRaises(FileNotFoundError):
                    locks.unlock(f)

    def test_lock_with_fd_int_propagates_permission_error(self):
        with tempfile.TemporaryFile() as f:
            fd = f.fileno()
            with mock.patch('fcntl.flock', side_effect=PermissionError('perm')):
                with self.assertRaises(PermissionError):
                    locks.lock(fd, locks.LOCK_EX)

    def test_unlock_with_fd_int_propagates_permission_error(self):
        with tempfile.TemporaryFile() as f:
            fd = f.fileno()
            with mock.patch('fcntl.flock', side_effect=PermissionError('perm')):
                with self.assertRaises(PermissionError):
                    locks.unlock(fd)

import os
import errno
import unittest
from unittest import mock
from django.core.files import locks

@unittest.skipIf(os.name == 'nt', 'POSIX fcntl tests only')
class FileLocksRegressionTests(unittest.TestCase):

    def test_lock_propagates_other_oserror(self):
        err = OSError(errno.EPERM, 'permission denied')
        with mock.patch('django.core.files.locks.fcntl.flock', side_effect=err):
            with self.assertRaises(OSError):
                locks.lock(3, locks.LOCK_EX)

    def test_unlock_propagates_other_oserror(self):
        err = OSError(errno.EPERM, 'permission denied')
        with mock.patch('django.core.files.locks.fcntl.flock', side_effect=err):
            with self.assertRaises(OSError):
                locks.unlock(3)

    def test_unlock_propagates_blockingioerror(self):
        with mock.patch('django.core.files.locks.fcntl.flock', side_effect=BlockingIOError):
            with self.assertRaises(BlockingIOError):
                locks.unlock(3)

import os
import tempfile
import unittest
from unittest import mock
from django.core.files import locks

@unittest.skipIf(os.name == 'nt', 'fcntl-based locking tests are skipped on Windows')
class LocksFcntlTests(unittest.TestCase):

    def test_lock_propagates_permissionerror(self):
        with tempfile.TemporaryFile() as f:
            with mock.patch('django.core.files.locks.fcntl.flock', side_effect=PermissionError):
                with self.assertRaises(PermissionError):
                    locks.lock(f, locks.LOCK_EX)

    def test_unlock_propagates_permissionerror(self):
        with tempfile.TemporaryFile() as f:
            with mock.patch('django.core.files.locks.fcntl.flock', side_effect=PermissionError):
                with self.assertRaises(PermissionError):
                    locks.unlock(f)

    def test_lock_does_not_swallow_generic_oserror(self):
        with tempfile.TemporaryFile() as f:
            with mock.patch('django.core.files.locks.fcntl.flock', side_effect=OSError):
                with self.assertRaises(OSError):
                    locks.lock(f, locks.LOCK_EX)

    def test_unlock_does_not_swallow_generic_oserror(self):
        with tempfile.TemporaryFile() as f:
            with mock.patch('django.core.files.locks.fcntl.flock', side_effect=OSError):
                with self.assertRaises(OSError):
                    locks.unlock(f)

import tempfile
import unittest
from unittest import mock
from django.core.files import locks
import tempfile
import unittest
from unittest import mock
from django.core.files import locks

@unittest.skipUnless(hasattr(locks, 'fcntl'), 'fcntl not available')
class LocksBehaviorTests(unittest.TestCase):

    def test_lock_propagates_permissionerror(self):
        with tempfile.TemporaryFile() as f:
            with mock.patch.object(locks.fcntl, 'flock', side_effect=PermissionError()):
                with self.assertRaises(PermissionError):
                    locks.lock(f, locks.LOCK_EX)

    def test_lock_propagates_permissionerror_for_fd(self):
        with tempfile.TemporaryFile() as tf:
            fd = tf.fileno()
            with mock.patch.object(locks.fcntl, 'flock', side_effect=PermissionError()):
                with self.assertRaises(PermissionError):
                    locks.lock(fd, locks.LOCK_EX)

    def test_unlock_propagates_blockingioerror(self):
        with tempfile.TemporaryFile() as f:
            with mock.patch.object(locks.fcntl, 'flock', side_effect=BlockingIOError()):
                with self.assertRaises(BlockingIOError):
                    locks.unlock(f)

    def test_unlock_propagates_permissionerror(self):
        with tempfile.TemporaryFile() as f:
            with mock.patch.object(locks.fcntl, 'flock', side_effect=PermissionError()):
                with self.assertRaises(PermissionError):
                    locks.unlock(f)

    def test_lock_only_returns_false_for_blockingioerror(self):
        with tempfile.TemporaryFile() as f:
            other_error = OSError(1, 'some os error')
            with mock.patch.object(locks.fcntl, 'flock', side_effect=other_error):
                with self.assertRaises(OSError):
                    locks.lock(f, locks.LOCK_EX)

import os
import errno
import tempfile
import unittest
from unittest import mock
from django.core.files import locks

@unittest.skipIf(os.name == 'nt', 'Tests require fcntl-based implementation (Unix)')
class LocksRegressionTests(unittest.TestCase):

    def test_lock_raises_on_permissionerror(self):
        with tempfile.NamedTemporaryFile() as f:
            with mock.patch.object(locks.fcntl, 'flock', side_effect=PermissionError(errno.EPERM, 'perm')):
                with self.assertRaises(PermissionError):
                    locks.lock(f, locks.LOCK_EX | locks.LOCK_NB)

    def test_unlock_raises_on_oserror(self):
        with tempfile.NamedTemporaryFile() as f:
            with mock.patch.object(locks.fcntl, 'flock', side_effect=OSError(errno.EIO, 'ioerr')):
                with self.assertRaises(OSError):
                    locks.unlock(f)

    def test_lock_with_fd_non_blocking_oserror(self):
        with tempfile.NamedTemporaryFile() as f:
            fd = f.fileno()
            with mock.patch.object(locks.fcntl, 'flock', side_effect=PermissionError(errno.EPERM, 'perm')):
                with self.assertRaises(PermissionError):
                    locks.lock(fd, locks.LOCK_EX | locks.LOCK_NB)

    def test_unlock_with_fd_oserror(self):
        with tempfile.NamedTemporaryFile() as f:
            fd = f.fileno()
            with mock.patch.object(locks.fcntl, 'flock', side_effect=OSError(errno.EIO, 'ioerr')):
                with self.assertRaises(OSError):
                    locks.unlock(fd)

    def test_lock_raises_on_generic_oserror(self):
        with tempfile.NamedTemporaryFile() as f:
            with mock.patch.object(locks.fcntl, 'flock', side_effect=OSError(errno.EINVAL, 'invalid')):
                with self.assertRaises(OSError):
                    locks.lock(f, locks.LOCK_EX | locks.LOCK_NB)