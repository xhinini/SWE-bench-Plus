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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.tearDown utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_handles_value_error_with_nonstandard_message utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_logs_debug_on_value_error utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_swallow_value_error_for_extra_files_pathobj utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_swallow_value_error_for_extra_files_string utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_swallow_value_error_for_main_module_file_attr utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_iter_modules_and_files_swallow_value_error_for_spec_origin utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_mix_of_good_and_bad_paths_returns_only_good utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_sys_path_directories_does_not_yield_on_value_error_for_file_entry utils_tests.test_autoreload_llm.ValueErrorPathHandlingTests.test_sys_path_directories_swallow_value_error
coverage json -o coverage.json
: '>>>>> End Test Output'
