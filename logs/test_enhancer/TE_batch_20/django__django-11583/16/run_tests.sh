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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.ValueErrorHandlingTests._make_fake_resolve utils_tests.test_autoreload_llm.ValueErrorHandlingTests.setUp utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_handles_value_error_with_empty_message utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_ignores_value_error_for_extra_files_path_obj utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_ignores_value_error_for_extra_files_string utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_ignores_value_error_from_module_origin utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_ignores_value_error_from_zip_loader_origin utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_mixed_extra_files_one_bad_one_good utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_handles_value_error_with_empty_message utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_ignores_value_error_for_directory_entry utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_ignores_value_error_for_file_entry utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_mixed_good_and_bad_entries_returns_only_good
coverage json -o coverage.json
: '>>>>> End Test Output'
