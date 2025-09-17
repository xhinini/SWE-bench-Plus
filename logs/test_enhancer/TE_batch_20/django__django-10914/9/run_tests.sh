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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 test_utils.tests_llm.FileUploadPermissionsTests._write_and_save test_utils.tests_llm.FileUploadPermissionsTests.setUp test_utils.tests_llm.FileUploadPermissionsTests.test_directory_permissions_mode_is_applied_on_create test_utils.tests_llm.FileUploadPermissionsTests.test_file_permissions_mode_property_behavior test_utils.tests_llm.FileUploadPermissionsTests.test_filesystemstorage_init_explicit_none_no_chmod test_utils.tests_llm.FileUploadPermissionsTests.test_no_chmod_when_both_modes_none
coverage json -o coverage.json
: '>>>>> End Test Output'
