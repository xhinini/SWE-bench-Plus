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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 file_storage.tests_llm.FileFieldStorageCallableRegressionTests._tmpdir file_storage.tests_llm.FileFieldStorageCallableRegressionTests.setUp file_storage.tests_llm.FileFieldStorageCallableRegressionTests.tearDown file_storage.tests_llm.FileFieldStorageCallableRegressionTests.test_deconstruct_omits_storage_when_callable_returns_default_storage file_storage.tests_llm.FileFieldStorageCallableRegressionTests.test_deconstruct_omits_when_callable_returns_default_storage_but_stores_callable_attribute file_storage.tests_llm.FileFieldStorageCallableRegressionTests.test_field__storage_callable_is_callable_for_partial file_storage.tests_llm.FileFieldStorageCallableRegressionTests.test_sets__storage_callable_attribute_for_callable_instance file_storage.tests_llm.FileFieldStorageCallableRegressionTests.test_sets__storage_callable_attribute_for_function file_storage.tests_llm.FileFieldStorageCallableRegressionTests.test_sets__storage_callable_attribute_for_lambda
coverage json -o coverage.json
: '>>>>> End Test Output'
