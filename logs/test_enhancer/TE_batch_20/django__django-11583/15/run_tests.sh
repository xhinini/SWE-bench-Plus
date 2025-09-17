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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.ValueErrorHandlingTests._make_bad_resolve utils_tests.test_autoreload_llm.ValueErrorHandlingTests.setUp utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_does_not_propagate_valueerror_when_multiple_files utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_ignores_valueerror_from_extra_files utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_ignores_valueerror_from_module_origin utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_skips_bad_zip_loader_origin utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_iter_modules_and_files_swallows_various_valueerror_messages utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_ignores_valueerror_and_includes_good utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_swallows_various_valueerror_messages utils_tests.test_autoreload_llm.ValueErrorHandlingTests.test_sys_path_directories_with_mixed_entries_only_yields_valid
coverage json -o coverage.json
: '>>>>> End Test Output'
