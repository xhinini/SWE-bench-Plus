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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.TestValueErrorPathHandling._make_side_effect utils_tests.test_autoreload_llm.TestValueErrorPathHandling.setUp utils_tests.test_autoreload_llm.TestValueErrorPathHandling.test_iter_all_python_module_files_ignores_value_error_from_sys_modules utils_tests.test_autoreload_llm.TestValueErrorPathHandling.test_iter_modules_and_files_handles_mixed_module_and_extra_files utils_tests.test_autoreload_llm.TestValueErrorPathHandling.test_iter_modules_and_files_ignores_value_error_for_extra_file_path utils_tests.test_autoreload_llm.TestValueErrorPathHandling.test_iter_modules_and_files_ignores_value_error_for_extra_file_string utils_tests.test_autoreload_llm.TestValueErrorPathHandling.test_iter_modules_and_files_ignores_value_error_for_main_module_file utils_tests.test_autoreload_llm.TestValueErrorPathHandling.test_iter_modules_and_files_ignores_value_error_for_module_origin utils_tests.test_autoreload_llm.TestValueErrorPathHandling.test_iter_modules_and_files_keeps_good_and_skips_bad utils_tests.test_autoreload_llm.TestValueErrorPathHandling.test_sys_path_directories_ignores_value_error_for_sys_path_entry utils_tests.test_autoreload_llm.TestValueErrorPathHandling.test_sys_path_directories_with_mixed_entries
coverage json -o coverage.json
: '>>>>> End Test Output'
