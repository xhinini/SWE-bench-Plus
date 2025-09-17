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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.ValueErrorResolveTests._patch_resolve_to_raise utils_tests.test_autoreload_llm.ValueErrorResolveTests.setUp utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_ignores_embedded_null_byte_valueerror utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_ignores_filenotfounderror utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_ignores_valueerror_for_extra_files_path utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_ignores_valueerror_for_extra_files_string utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_ignores_valueerror_from_main_module_file utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_ignores_valueerror_from_module_spec_origin utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_iter_modules_and_files_keeps_valid_and_skips_errored utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_sys_path_directories_ignores_embedded_null_byte_valueerror utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_sys_path_directories_ignores_filenotfounderror utils_tests.test_autoreload_llm.ValueErrorResolveTests.test_sys_path_directories_ignores_valueerror
coverage json -o coverage.json
: '>>>>> End Test Output'
