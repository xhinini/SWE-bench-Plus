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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.ValueErrorHandlingTests._make_fake_resolve utils_tests.test_autoreload_llm.ValueErrorHandlingTests.setUp utils_tests.test_autoreload_llm.ValueErrorHandlingTests.tearDown utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_ignores_valueerror_for_Path_extra_file utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_ignores_valueerror_for_main_module_file_attribute utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_ignores_valueerror_for_str_extra_file utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_logs_on_valueerror utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_with_mixed_files_some_raise_valueerror utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_ignores_valueerror_for_path_like_entry utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_ignores_valueerror_for_sys_path_entry utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_logs_on_valueerror utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_with_mixed_entries_some_raise_valueerror
coverage json -o coverage.json
: '>>>>> End Test Output'
