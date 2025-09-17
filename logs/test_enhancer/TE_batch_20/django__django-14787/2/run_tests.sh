#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 decorators.tests_llm.MethodDecoratorWrappedTests.test_class_based_decorator_sees_wrapped decorators.tests_llm.MethodDecoratorWrappedTests.test_class_level_decoration_sets_wrapped decorators.tests_llm.MethodDecoratorWrappedTests.test_decorating_dunder_call_sees_wrapped decorators.tests_llm.MethodDecoratorWrappedTests.test_descriptor_wrapper_decorator_sees_wrapped decorators.tests_llm.MethodDecoratorWrappedTests.test_inspect_unwrap_returns_original_method decorators.tests_llm.MethodDecoratorWrappedTests.test_iterable_of_decorators_each_sees_wrapped decorators.tests_llm.MethodDecoratorWrappedTests.test_method_decorator_on_callable_attribute_preserves_wrapped decorators.tests_llm.MethodDecoratorWrappedTests.test_nested_wraps_and_unwrap_chain decorators.tests_llm.MethodDecoratorWrappedTests.test_single_decorator_bound_method_has_wrapped decorators.tests_llm.make_check_decorator
coverage json -o coverage.json
: '>>>>> End Test Output'
