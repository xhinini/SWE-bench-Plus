#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 decorators.tests_llm.WrappedBindingTests.test_bound_method_has___wrapped__single_decorator decorators.tests_llm.WrappedBindingTests.test_class_and_method_decorator_both_see_wrapped decorators.tests_llm.WrappedBindingTests.test_class_based_decorator_sees_wrapped decorators.tests_llm.WrappedBindingTests.test_class_level_decorator_sees___wrapped__ decorators.tests_llm.WrappedBindingTests.test_decorating___call___method_preserves_wrapped decorators.tests_llm.WrappedBindingTests.test_decorators_order_and_wrapped_presence_with_chaining decorators.tests_llm.WrappedBindingTests.test_descriptor_wrapper_preserves___wrapped__ decorators.tests_llm.WrappedBindingTests.test_iterable_of_method_decorators_preserves_wrapped decorators.tests_llm.WrappedBindingTests.test_multiple_decorators_see___wrapped__tuple
coverage json -o coverage.json
: '>>>>> End Test Output'
