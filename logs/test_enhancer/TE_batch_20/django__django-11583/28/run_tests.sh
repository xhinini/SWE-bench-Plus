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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.ValueErrorHandlingTests._make_temp_file utils_tests.test_autoreload_llm.ValueErrorHandlingTests.setUp utils_tests.test_autoreload_llm.ValueErrorHandlingTests.tearDown utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_all_python_module_files_ignores_value_error utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_handles_unexpected_value_error_message_with_null_byte_string utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_ignores_value_error_from_extra_files utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_ignores_value_error_from_modules utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_keeps_valid_files_and_skips_bad utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_multiple_extra_files_some_bad_some_good utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_handles_unexpected_value_error_message_with_null_byte utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_ignores_value_error utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_keeps_valid_and_skips_bad
coverage json -o coverage.json
: '>>>>> End Test Output'
