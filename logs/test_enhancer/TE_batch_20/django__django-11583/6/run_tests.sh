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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.setUp utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.tearDown utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_all_python_module_files_ignores_value_error_from_error_files utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_handles_mixed_module_origins utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_ignores_value_error_for_extra_files_path_object utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_ignores_value_error_for_extra_files_string utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_ignores_value_error_from_module_origin utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_skips_only_problematic_path_when_mixed utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_with_path_objects_and_mixed_behavior utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_sys_path_directories_ignores_value_error_entries utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_sys_path_directories_skips_only_problematic_entry_when_mixed
coverage json -o coverage.json
: '>>>>> End Test Output'
