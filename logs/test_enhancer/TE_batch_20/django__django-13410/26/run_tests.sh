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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 files.tests_llm.LocksTests.test_lock_nonblocking_blockingioerror_returns_false files.tests_llm.LocksTests.test_lock_other_oserror_propagates files.tests_llm.LocksTests.test_lock_success_returns_true files.tests_llm.LocksTests.test_lock_uses_fileno_for_fileobj files.tests_llm.LocksTests.test_lock_with_fd_integer_input files.tests_llm.LocksTests.test_unlock_other_oserror_propagates files.tests_llm.LocksTests.test_unlock_success_returns_true files.tests_llm.LocksTests.test_unlock_uses_fileno_for_fileobj files.tests_llm.LocksTests.test_unlock_with_fd_integer_input
coverage json -o coverage.json
: '>>>>> End Test Output'
