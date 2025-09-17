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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.ValueErrorResolveTests._make_temp_file utils_tests.test_autoreload_llm.ValueErrorResolveTests.setUp utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_handles_embedded_null_byte_message utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_ignores_value_error_for_path_object utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_ignores_value_error_for_string_extra_file utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_logs_debug_on_value_error utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_with_good_and_bad_files_returns_only_good utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_sys_path_directories_ignores_value_error_for_specific_sys_path utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_sys_path_directories_logs_debug_on_value_error utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_sys_path_directories_with_file_returns_parent_and_ignores_other_errors
coverage json -o coverage.json
: '>>>>> End Test Output'
