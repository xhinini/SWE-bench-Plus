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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.ResolveValueErrorTests.fake_resolve_factory utils_tests.test_autoreload_llm.ResolveValueErrorTests.setUp utils_tests.test_autoreload_llm.ResolveValueErrorTests.test_iter_modules_and_files_handles_multiple_bad_paths utils_tests.test_autoreload_llm.ResolveValueErrorTests.test_iter_modules_and_files_ignores_multiple_value_errors_and_returns_good_files utils_tests.test_autoreload_llm.ResolveValueErrorTests.test_iter_modules_and_files_ignores_value_error_for_module_origin_arbitrary_message utils_tests.test_autoreload_llm.ResolveValueErrorTests.test_iter_modules_and_files_ignores_value_error_when_path_object_passed utils_tests.test_autoreload_llm.ResolveValueErrorTests.test_iter_modules_and_files_ignores_value_error_with_arbitrary_message utils_tests.test_autoreload_llm.ResolveValueErrorTests.test_iter_modules_and_files_ignores_value_error_with_embedded_null_variation utils_tests.test_autoreload_llm.ResolveValueErrorTests.test_sys_path_directories_ignores_value_error_embedded_variation utils_tests.test_autoreload_llm.ResolveValueErrorTests.test_sys_path_directories_ignores_value_error_with_arbitrary_message utils_tests.test_autoreload_llm.ResolveValueErrorTests.test_sys_path_directories_returns_other_paths_when_some_entries_fail
coverage json -o coverage.json
: '>>>>> End Test Output'
