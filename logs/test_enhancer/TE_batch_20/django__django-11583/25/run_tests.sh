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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.TestIterModulesValueErrorHandling._patch_resolve_raising utils_tests.test_autoreload_llm.TestIterModulesValueErrorHandling.setUp utils_tests.test_autoreload_llm.TestIterModulesValueErrorHandling.test_iter_modules_and_files_handles_valueerror_from_main_module_file utils_tests.test_autoreload_llm.TestIterModulesValueErrorHandling.test_iter_modules_and_files_handles_valueerror_from_spec_origin utils_tests.test_autoreload_llm.TestIterModulesValueErrorHandling.test_iter_modules_and_files_mixed_good_and_bad_files utils_tests.test_autoreload_llm.TestIterModulesValueErrorHandling.test_iter_modules_and_files_swallow_empty_valueerror_message utils_tests.test_autoreload_llm.TestIterModulesValueErrorHandling.test_iter_modules_and_files_swallow_generic_valueerror_from_extra_files utils_tests.test_autoreload_llm.TestIterModulesValueErrorHandling.test_iter_modules_and_files_swallow_null_phrase_message utils_tests.test_autoreload_llm.TestIterModulesValueErrorHandling.test_iter_modules_and_files_swallow_unicode_valueerror_message utils_tests.test_autoreload_llm.TestIterModulesValueErrorHandling.test_iter_modules_and_files_swallow_various_valueerror_messages_repeated
coverage json -o coverage.json
: '>>>>> End Test Output'
