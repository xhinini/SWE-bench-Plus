#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 files.tests_llm.LocksFcntlBehaviorTests.test_lock_handles_blockingioerror_and_returns_false files.tests_llm.LocksFcntlBehaviorTests.test_lock_propagates_permission_error files.tests_llm.LocksFcntlBehaviorTests.test_lock_propagates_subclass_of_oserror_other_than_blocking files.tests_llm.LocksFcntlBehaviorTests.test_lock_raises_on_generic_oserror files.tests_llm.LocksFcntlBehaviorTests.test_lock_returns_true_on_success files.tests_llm.LocksFcntlBehaviorTests.test_lock_uses_integer_fd_directly files.tests_llm.LocksFcntlBehaviorTests.test_unlock_propagates_permission_error files.tests_llm.LocksFcntlBehaviorTests.test_unlock_raises_on_generic_oserror files.tests_llm.LocksFcntlBehaviorTests.test_unlock_returns_true_on_success files.tests_llm.LocksFcntlBehaviorTests.test_unlock_uses_fileobj_fd
coverage json -o coverage.json
: '>>>>> End Test Output'
