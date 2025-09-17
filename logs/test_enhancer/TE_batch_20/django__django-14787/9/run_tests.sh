#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 decorators.tests_llm.MethodDecoratorRegressionTests.test_bound_method_preserves_docstring decorators.tests_llm.MethodDecoratorRegressionTests.test_chained_wrappers_introspectable_via_inspect_unwrap decorators.tests_llm.MethodDecoratorRegressionTests.test_custom_attribute_set_by_decorator_present_on_class_and_bound decorators.tests_llm.MethodDecoratorRegressionTests.test_method_decorator_with_descriptor_wrapper decorators.tests_llm.attribute_setting_decorator decorators.tests_llm.capturing_decorator decorators.tests_llm.simple_wraps_decorator
coverage json -o coverage.json
: '>>>>> End Test Output'
