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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 test_utils.tests_llm.FileUploadPermissionsTests._mode test_utils.tests_llm.FileUploadPermissionsTests.setUp test_utils.tests_llm.FileUploadPermissionsTests.tearDown test_utils.tests_llm.FileUploadPermissionsTests.test_explicit_file_permissions_mode_none_does_not_force_default_on_instance test_utils.tests_llm.load_tests
coverage json -o coverage.json
: '>>>>> End Test Output'
