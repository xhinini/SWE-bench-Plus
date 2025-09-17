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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.RegressionAutoreloadValueErrorTests._make_bad_path utils_tests.test_autoreload_llm.RegressionAutoreloadValueErrorTests.setUp utils_tests.test_autoreload_llm.RegressionAutoreloadValueErrorTests.test_iter_modules_and_files_ignores_value_error_from_extra_files_pathobj utils_tests.test_autoreload_llm.RegressionAutoreloadValueErrorTests.test_iter_modules_and_files_ignores_value_error_from_extra_files_str utils_tests.test_autoreload_llm.RegressionAutoreloadValueErrorTests.test_iter_modules_and_files_ignores_value_error_from_main_module_file utils_tests.test_autoreload_llm.RegressionAutoreloadValueErrorTests.test_iter_modules_and_files_ignores_value_error_from_module_origin utils_tests.test_autoreload_llm.RegressionAutoreloadValueErrorTests.test_iter_modules_and_files_mixed_inputs_with_value_error utils_tests.test_autoreload_llm.RegressionAutoreloadValueErrorTests.test_sys_path_directories_and_iter_modules_combined_handling utils_tests.test_autoreload_llm.RegressionAutoreloadValueErrorTests.test_sys_path_directories_ignores_value_error_entry utils_tests.test_autoreload_llm.RegressionAutoreloadValueErrorTests.test_sys_path_directories_ignores_value_error_for_file_entry utils_tests.test_autoreload_llm.RegressionAutoreloadValueErrorTests.test_sys_path_directories_skips_bad_but_includes_good
coverage json -o coverage.json
: '>>>>> End Test Output'
