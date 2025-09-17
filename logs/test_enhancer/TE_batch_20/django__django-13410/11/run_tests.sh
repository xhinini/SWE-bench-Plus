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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 files.tests_llm.LocksRegressionTests.test_lock_raises_on_generic_oserror files.tests_llm.LocksRegressionTests.test_lock_raises_on_permissionerror files.tests_llm.LocksRegressionTests.test_lock_with_fd_non_blocking_oserror files.tests_llm.LocksRegressionTests.test_unlock_raises_on_oserror files.tests_llm.LocksRegressionTests.test_unlock_with_fd_oserror
coverage json -o coverage.json
: '>>>>> End Test Output'
