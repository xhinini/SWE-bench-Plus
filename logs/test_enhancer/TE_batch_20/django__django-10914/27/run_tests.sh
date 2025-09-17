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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 test_utils.tests_llm.FileUploadPermissionsTests.setUp test_utils.tests_llm.FileUploadPermissionsTests.test_filesystemstorage_respects_explicit_none test_utils.tests_llm.FileUploadPermissionsTests.test_mkdir_uses_directory_permissions_mode_when_set test_utils.tests_llm.FileUploadPermissionsTests.test_saving_file_calls_chmod_with_file_permissions_mode test_utils.tests_llm.FileUploadPermissionsTests.test_saving_file_does_not_call_chmod_when_mode_explicitly_none test_utils.tests_llm.FileUploadPermissionsTests.test_temporary_uploaded_file_triggers_chmod_for_file_mode
coverage json -o coverage.json
: '>>>>> End Test Output'
