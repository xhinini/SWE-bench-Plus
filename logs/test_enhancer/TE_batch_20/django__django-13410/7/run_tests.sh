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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 files.tests_llm.LocksRegressionTests.test_lock_propagates_filenotfounderror files.tests_llm.LocksRegressionTests.test_lock_propagates_generic_os_error files.tests_llm.LocksRegressionTests.test_lock_propagates_permission_error files.tests_llm.LocksRegressionTests.test_lock_with_fd_int_propagates_permission_error files.tests_llm.LocksRegressionTests.test_unlock_propagates_blockingioerror files.tests_llm.LocksRegressionTests.test_unlock_propagates_filenotfounderror files.tests_llm.LocksRegressionTests.test_unlock_propagates_generic_os_error files.tests_llm.LocksRegressionTests.test_unlock_propagates_permission_error files.tests_llm.LocksRegressionTests.test_unlock_with_fd_int_propagates_permission_error
coverage json -o coverage.json
: '>>>>> End Test Output'
