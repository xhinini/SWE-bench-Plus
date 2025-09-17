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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 file_storage.tests_llm.FileFieldDeconstructCallableTests.test_deconstruct_omits_storage_for_bound_method_returning_default_storage file_storage.tests_llm.FileFieldDeconstructCallableTests.test_deconstruct_omits_storage_for_callable_class_instance_returning_default_storage file_storage.tests_llm.FileFieldDeconstructCallableTests.test_deconstruct_omits_storage_for_callable_instance_returning_default_storage file_storage.tests_llm.FileFieldDeconstructCallableTests.test_deconstruct_omits_storage_for_callable_object_with_state_returning_default_storage file_storage.tests_llm.FileFieldDeconstructCallableTests.test_deconstruct_omits_storage_for_function_returning_default_storage file_storage.tests_llm.FileFieldDeconstructCallableTests.test_deconstruct_omits_storage_for_lambda_returning_default_storage file_storage.tests_llm.FileFieldDeconstructCallableTests.test_deconstruct_omits_storage_for_nested_callable_returning_default_storage file_storage.tests_llm.FileFieldDeconstructCallableTests.test_deconstruct_omits_storage_for_partial_callable_returning_default_storage file_storage.tests_llm.FileFieldDeconstructCallableTests.test_deconstruct_omits_storage_for_staticmethod_returning_default_storage
coverage json -o coverage.json
: '>>>>> End Test Output'
