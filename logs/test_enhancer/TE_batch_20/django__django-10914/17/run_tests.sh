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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 test_utils.tests_llm.FileUploadPermissionsTests._file_mode test_utils.tests_llm.FileUploadPermissionsTests._make_tempdir test_utils.tests_llm.FileUploadPermissionsTests.setUp test_utils.tests_llm.FileUploadPermissionsTests.test_constructor_argument_overrides_setting test_utils.tests_llm.FileUploadPermissionsTests.test_default_setting_value_is_0644 test_utils.tests_llm.FileUploadPermissionsTests.test_directory_permissions_reflect_setting test_utils.tests_llm.FileUploadPermissionsTests.test_files_saved_respect_permissions test_utils.tests_llm.FileUploadPermissionsTests.test_filesystemstorage_reflects_setting_on_instantiation test_utils.tests_llm.FileUploadPermissionsTests.test_multiple_saves_preserve_permissions test_utils.tests_llm.FileUploadPermissionsTests.test_none_setting_results_in_none_attribute test_utils.tests_llm.FileUploadPermissionsTests.test_save_with_subdirectories_applies_directory_permissions test_utils.tests_llm.FileUploadPermissionsTests.test_setting_changes_affect_new_instances_only
coverage json -o coverage.json
: '>>>>> End Test Output'
