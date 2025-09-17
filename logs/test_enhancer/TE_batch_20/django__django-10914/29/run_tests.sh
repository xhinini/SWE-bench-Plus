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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 test_utils.tests_llm.FileUploadPermissionsTests.test_changing_file_upload_directory_permissions_reflected_in_default_storage test_utils.tests_llm.FileUploadPermissionsTests.test_default_setting_reflected_in_default_storage test_utils.tests_llm.FileUploadPermissionsTests.test_default_storage_save_respects_file_permissions_via_settings test_utils.tests_llm.FileUploadPermissionsTests.test_directory_permissions_not_set_by_default_when_none test_utils.tests_llm.FileUploadPermissionsTests.test_filesystemstorage_explicit_directory_permissions_applied_on_save test_utils.tests_llm.FileUploadPermissionsTests.test_filesystemstorage_explicit_file_permissions_applied_on_save test_utils.tests_llm.FileUploadPermissionsTests.test_filesystemstorage_file_permissions_attribute_can_be_none test_utils.tests_llm.FileUploadPermissionsTests.test_filesystemstorage_respects_explicit_permissions_over_settings test_utils.tests_llm.FileUploadPermissionsTests.test_override_setting_reflected_in_default_storage test_utils.tests_llm.FileUploadPermissionsTests.test_saving_into_nested_new_directory_sets_permissions
coverage json -o coverage.json
: '>>>>> End Test Output'
