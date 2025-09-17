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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.TestValueErrorHandling.fake_resolve_factory utils_tests.test_autoreload_llm.TestValueErrorHandling.setUp utils_tests.test_autoreload_llm.TestValueErrorHandling.test_iter_all_python_module_files_ignores_valueerror_for_sys_modules utils_tests.test_autoreload_llm.TestValueErrorHandling.test_iter_modules_and_files_continues_after_valueerror_with_other_files utils_tests.test_autoreload_llm.TestValueErrorHandling.test_iter_modules_and_files_ignores_valueerror_in_extra_files utils_tests.test_autoreload_llm.TestValueErrorHandling.test_iter_modules_and_files_ignores_valueerror_in_main_module_file utils_tests.test_autoreload_llm.TestValueErrorHandling.test_iter_modules_and_files_ignores_valueerror_in_module_origin utils_tests.test_autoreload_llm.TestValueErrorHandling.test_iter_modules_and_files_ignores_valueerror_with_empty_message utils_tests.test_autoreload_llm.TestValueErrorHandling.test_sys_path_directories_continues_with_other_entries utils_tests.test_autoreload_llm.TestValueErrorHandling.test_sys_path_directories_ignores_valueerror_for_entries utils_tests.test_autoreload_llm.TestValueErrorHandling.test_sys_path_directories_ignores_valueerror_with_unexpected_message
coverage json -o coverage.json
: '>>>>> End Test Output'
