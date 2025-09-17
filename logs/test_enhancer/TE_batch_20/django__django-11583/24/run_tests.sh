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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.ValueErrorHandlingTests._patch_resolve_to_raise utils_tests.test_autoreload_llm.ValueErrorHandlingTests.setUp utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_all_python_module_files_ignores_valueerror_from__error_files utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_ignores_valueerror_for_main_module_file utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_ignores_valueerror_from_extra_file utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_ignores_valueerror_from_module_origin utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_includes_good_and_ignores_bad_extra_file utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_with_module_and_extra_file_combination utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_ignores_valueerror_in_sys_path_entry utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_includes_good_even_if_one_entry_raises_valueerror
coverage json -o coverage.json
: '>>>>> End Test Output'
