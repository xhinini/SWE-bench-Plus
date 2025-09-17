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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_autoreload_llm.ValueErrorPathResolveTests._patch_resolve_for utils_tests.test_autoreload_llm.ValueErrorPathResolveTests.setUp utils_tests.test_autoreload_llm.ValueErrorPathResolveTests.test_iter_modules_and_files_cache_is_cleared_and_ignores_valueerror utils_tests.test_autoreload_llm.ValueErrorPathResolveTests.test_iter_modules_and_files_handles_mixed_paths utils_tests.test_autoreload_llm.ValueErrorPathResolveTests.test_iter_modules_and_files_ignores_valueerror_on_module_origin utils_tests.test_autoreload_llm.ValueErrorPathResolveTests.test_iter_modules_and_files_ignores_valueerror_with_custom_message utils_tests.test_autoreload_llm.ValueErrorPathResolveTests.test_iter_modules_and_files_with_path_objects_raises_no_exception utils_tests.test_autoreload_llm.ValueErrorPathResolveTests.test_sys_path_directories_handles_mixed_paths utils_tests.test_autoreload_llm.ValueErrorPathResolveTests.test_sys_path_directories_ignores_valueerror_with_custom_message
coverage json -o coverage.json
: '>>>>> End Test Output'
