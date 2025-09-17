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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 test_utils.tests_llm.FileUploadPermissionsTests._make_file test_utils.tests_llm.FileUploadPermissionsTests.test_chmod_calls_include_expected_file_and_directory_with_both_settings_set test_utils.tests_llm.FileUploadPermissionsTests.test_directory_permissions_applied_on_save test_utils.tests_llm.FileUploadPermissionsTests.test_override_setting_changes_chmod_mode test_utils.tests_llm.FileUploadPermissionsTests.test_storage_arg_overrides_setting_for_file_permissions test_utils.tests_llm.FileUploadPermissionsTests.test_storage_directory_arg_overrides_setting test_utils.tests_llm.FileUploadPermissionsTests.test_storage_uses_setting_and_calls_chmod_default
coverage json -o coverage.json
: '>>>>> End Test Output'
