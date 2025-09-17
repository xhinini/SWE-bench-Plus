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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 test_utils.tests_llm.FileUploadPermissionsTests._full_path test_utils.tests_llm.FileUploadPermissionsTests.setUp test_utils.tests_llm.FileUploadPermissionsTests.test_directory_permissions_chmod_called_when_setting_provided test_utils.tests_llm.FileUploadPermissionsTests.test_explicit_none_file_permissions_mode_disables_chmod test_utils.tests_llm.FileUploadPermissionsTests.test_multiple_saves_result_in_multiple_chmod_calls test_utils.tests_llm.FileUploadPermissionsTests.test_saving_with_nested_directories_calls_chmod_for_each_created_dir
coverage json -o coverage.json
: '>>>>> End Test Output'
