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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.ValueErrorHandlingTests._patch_resolve_raising_for utils_tests.test_autoreload_llm.ValueErrorHandlingTests.setUp utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_handles_value_error_from_main_module_file utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_handles_value_error_from_module_spec_origin utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_ignores_bad_path_object utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_ignores_bad_string_path utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_ignores_value_error_with_nonembedded_message utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_includes_good_and_ignores_bad utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_multiple_bad_sys_path_entries_do_not_raise utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_ignores_bad_entry_in_sys_path utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_includes_good_and_ignores_bad
coverage json -o coverage.json
: '>>>>> End Test Output'
