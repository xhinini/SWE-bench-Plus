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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 file_storage.tests_llm.FileFieldStorageCallableAttrTests.setUp file_storage.tests_llm.FileFieldStorageCallableAttrTests.tearDown file_storage.tests_llm.FileFieldStorageCallableAttrTests.test__storage_callable_persists_after_deconstruct_called file_storage.tests_llm.FileFieldStorageCallableAttrTests.test_callable_class_sets__storage_callable file_storage.tests_llm.FileFieldStorageCallableAttrTests.test_callable_function_sets__storage_callable file_storage.tests_llm.FileFieldStorageCallableAttrTests.test_callable_that_returns_custom_subclass_sets__storage_callable file_storage.tests_llm.FileFieldStorageCallableAttrTests.test_storage_callable_attribute_is_callable_class file_storage.tests_llm.FileFieldStorageCallableAttrTests.test_storage_callable_attribute_is_callable_function
coverage json -o coverage.json
: '>>>>> End Test Output'
