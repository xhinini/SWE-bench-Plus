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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 file_storage.tests_llm.FileFieldStorageCallableAttributesTests.test_callable_instance_sets_storage_callable_attribute file_storage.tests_llm.FileFieldStorageCallableAttributesTests.test_class_callable_sets_storage_callable_attribute file_storage.tests_llm.FileFieldStorageCallableAttributesTests.test_function_callable_sets_storage_callable_attribute file_storage.tests_llm.FileFieldStorageCallableAttributesTests.test_lambda_callable_sets_storage_callable_attribute file_storage.tests_llm.FileFieldStorageCallableAttributesTests.test_partial_callable_sets_storage_callable_attribute
coverage json -o coverage.json
: '>>>>> End Test Output'
