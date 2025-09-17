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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 file_storage.tests_llm.FileFieldStorageCallableTests.test_callable_that_returns_default_storage_sets__storage_callable file_storage.tests_llm.FileFieldStorageCallableTests.test_deconstruct_returns_original_callable_for_function file_storage.tests_llm.FileFieldStorageCallableTests.test_deconstruct_returns_original_class_for_class_storage file_storage.tests_llm.FileFieldStorageCallableTests.test_deconstruct_with_local_callable_includes_callable file_storage.tests_llm.FileFieldStorageCallableTests.test_field_deconstruct_preserves_callable_on_model_field file_storage.tests_llm.FileFieldStorageCallableTests.test_init_sets__storage_callable_for_class file_storage.tests_llm.FileFieldStorageCallableTests.test_init_sets__storage_callable_for_local_function file_storage.tests_llm.FileFieldStorageCallableTests.test_init_sets__storage_callable_for_module_function file_storage.tests_llm.FileFieldStorageCallableTests.test_multiple_callable_types_preserve__storage_callable file_storage.tests_llm.FileFieldStorageCallableTests.test_non_callable_storage_does_not_set__storage_callable
coverage json -o coverage.json
: '>>>>> End Test Output'
