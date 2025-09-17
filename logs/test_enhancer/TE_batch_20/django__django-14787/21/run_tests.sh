#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 decorators.tests_llm.WrappedInspectionTests.test_wrapped_available_to_decorator_that_uses_update_wrapper_behaviour decorators.tests_llm.WrappedInspectionTests.test_wrapped_present_for_call_method decorators.tests_llm.WrappedInspectionTests.test_wrapped_present_for_descriptor_wrapped_method decorators.tests_llm.WrappedInspectionTests.test_wrapped_present_on_method_decorated_function decorators.tests_llm.WrappedInspectionTests.test_wrapped_present_when_decorating_via_class_name_argument decorators.tests_llm.WrappedInspectionTests.test_wrapped_present_with_decorator_instance decorators.tests_llm.WrappedInspectionTests.test_wrapped_present_with_tuple_decorators_on_method decorators.tests_llm.WrappedInspectionTests.test_wrapped_preserved_with_method_and_class_decorators
coverage json -o coverage.json
: '>>>>> End Test Output'
