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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 test_utils.tests_llm.FileUploadPermissionsTests.test_default_setting_default_storage_attribute test_utils.tests_llm.FileUploadPermissionsTests.test_default_storage_changes_when_overriding_then_restored test_utils.tests_llm.FileUploadPermissionsTests.test_directory_created_with_permissions test_utils.tests_llm.FileUploadPermissionsTests.test_filesystemstorage_init_with_explicit_param_overrides_setting test_utils.tests_llm.FileUploadPermissionsTests.test_filesystemstorage_init_with_none_respects_none test_utils.tests_llm.FileUploadPermissionsTests.test_filesystemstorage_reads_setting_on_init test_utils.tests_llm.FileUploadPermissionsTests.test_override_file_upload_directory_permissions_attribute test_utils.tests_llm.FileUploadPermissionsTests.test_override_settings_changes_default_storage_attribute test_utils.tests_llm.FileUploadPermissionsTests.test_saving_file_sets_permissions_default test_utils.tests_llm.FileUploadPermissionsTests.test_saving_file_with_custom_permissions
coverage json -o coverage.json
: '>>>>> End Test Output'
