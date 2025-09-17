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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 test_utils.tests_llm.FileUploadPermissionsTests.test_default_storage_has_file_permissions_mode_644 test_utils.tests_llm.FileUploadPermissionsTests.test_default_storage_reflects_none_setting test_utils.tests_llm.FileUploadPermissionsTests.test_default_storage_reflects_settings_context_manager test_utils.tests_llm.FileUploadPermissionsTests.test_existing_storage_instances_not_mutated_by_setting_change test_utils.tests_llm.FileUploadPermissionsTests.test_filesystemstorage_inherits_setting_when_not_provided test_utils.tests_llm.FileUploadPermissionsTests.test_filesystemstorage_reflects_changed_setting_for_new_instances test_utils.tests_llm.FileUploadPermissionsTests.test_filesystemstorage_respects_explicit_none_argument test_utils.tests_llm.FileUploadPermissionsTests.test_filesystemstorage_respects_explicit_value_argument test_utils.tests_llm.FileUploadPermissionsTests.test_new_instances_after_setting_change_reflect_new_value test_utils.tests_llm.FileUploadPermissionsTests.test_settings_default_file_upload_permissions_is_644
coverage json -o coverage.json
: '>>>>> End Test Output'
