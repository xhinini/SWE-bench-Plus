#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 decorators.tests_llm.MethodDecoratorUnwrapTests.test_unwrap_class_based_decorator decorators.tests_llm.MethodDecoratorUnwrapTests.test_unwrap_for_callable_object_decorator_returning_wrapped_function decorators.tests_llm.MethodDecoratorUnwrapTests.test_unwrap_for_descriptor_like_wrappers decorators.tests_llm.MethodDecoratorUnwrapTests.test_unwrap_iterable_of_method_decorators_on_class decorators.tests_llm.MethodDecoratorUnwrapTests.test_unwrap_multiple_function_decorators_tuple decorators.tests_llm.MethodDecoratorUnwrapTests.test_unwrap_on_class_decorator_name_argument decorators.tests_llm.MethodDecoratorUnwrapTests.test_unwrap_preserves_original_attribute decorators.tests_llm.MethodDecoratorUnwrapTests.test_unwrap_single_function_decorator decorators.tests_llm.MethodDecoratorUnwrapTests.test_unwrap_with_argumented_decorator_class
coverage json -o coverage.json
: '>>>>> End Test Output'
