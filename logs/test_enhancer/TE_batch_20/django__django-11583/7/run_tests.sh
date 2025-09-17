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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.ValueErrorResolveTests._patch_resolve_raise_on_bad utils_tests.test_autoreload_llm.ValueErrorResolveTests.setUp utils_tests.test_autoreload_llm.ValueErrorResolveTests.tearDown utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_all_python_module_files_handles_valueerror_from_error_files utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_continues_on_valueerror_and_includes_other_files utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_handles_valueerror_from_main_module_with_file utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_ignores_other_valueerror_messages utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_ignores_valueerror_for_extra_path_object utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_ignores_valueerror_for_extra_str_filename utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_ignores_valueerror_for_module_origin utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_sys_path_directories_continues_on_valueerror_and_includes_good_parent utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_sys_path_directories_ignores_valueerror_for_sys_path_entry
coverage json -o coverage.json
: '>>>>> End Test Output'
