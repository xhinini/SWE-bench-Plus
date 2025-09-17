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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests._patch_resolve_to_raise_for_null utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.setUp utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.tearDown utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_ignores_value_error_for_path_extra utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_ignores_value_error_for_string_extra utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_ignores_value_error_from_module_origin utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_ignores_value_error_with_embedded_null_byte_message utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_keeps_good_paths_when_others_raise utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_returns_nonempty_when_some_paths_ok utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_sys_path_directories_ignores_value_error_for_string_entry utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_sys_path_directories_ignores_value_error_with_different_message utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_sys_path_directories_swallows_embedded_null_byte_message
coverage json -o coverage.json
: '>>>>> End Test Output'
