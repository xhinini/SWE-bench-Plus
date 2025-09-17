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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 file_storage.tests_llm.FileFieldStorageCallableAttributeTests.test_callable_class_deconstruct_returns_callable_and_attr_matches file_storage.tests_llm.FileFieldStorageCallableAttributeTests.test_callable_class_sets__storage_callable_attribute file_storage.tests_llm.FileFieldStorageCallableAttributeTests.test_callable_class_storage_attr_and_deconstruct_persist file_storage.tests_llm.FileFieldStorageCallableAttributeTests.test_callable_function_deconstruct_returns_callable_and_attr_matches file_storage.tests_llm.FileFieldStorageCallableAttributeTests.test_callable_function_sets__storage_callable_attribute file_storage.tests_llm.FileFieldStorageCallableAttributeTests.test_deconstruct_does_not_remove__storage_callable_attribute file_storage.tests_llm.FileFieldStorageCallableAttributeTests.test_model_field_callable_storage_deconstruct_preserves_callable file_storage.tests_llm.FileFieldStorageCallableAttributeTests.test_model_field_callable_storage_sets__storage_callable
coverage json -o coverage.json
: '>>>>> End Test Output'
