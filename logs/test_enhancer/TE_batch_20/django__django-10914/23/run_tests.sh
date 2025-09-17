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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 test_utils.tests_llm.FileUploadPermissionsTests.test_default_file_upload_permissions_attribute test_utils.tests_llm.FileUploadPermissionsTests.test_directory_permissions_applied_on_save test_utils.tests_llm.FileUploadPermissionsTests.test_file_permissions_none_and_override_behavior test_utils.tests_llm.FileUploadPermissionsTests.test_filesystemstorage_explicit_none_uses_settings test_utils.tests_llm.FileUploadPermissionsTests.test_filesystemstorage_override_numeric test_utils.tests_llm.FileUploadPermissionsTests.test_filesystemstorage_uses_settings_by_default test_utils.tests_llm.FileUploadPermissionsTests.test_saving_file_sets_os_permissions test_utils.tests_llm.FileUploadPermissionsTests.test_settings_override_reflects_default_storage test_utils.tests_llm.FileUploadPermissionsTests.test_settings_set_to_none_reflects_default_storage test_utils.tests_llm.FileUploadPermissionsTests.test_zero_file_permissions_preserved
coverage json -o coverage.json
: '>>>>> End Test Output'
