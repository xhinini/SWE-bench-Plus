#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 decorators.tests_llm.MethodDecoratorWrapsTests.test_custom_attribute_from_wraps_decorator_preserved_on_bound_and_unbound decorators.tests_llm.MethodDecoratorWrapsTests.test_descriptor_with_wraps_based_decorator_preserves_name decorators.tests_llm.MethodDecoratorWrapsTests.test_multiple_wraps_based_decorators_preserve_name_and_order decorators.tests_llm.MethodDecoratorWrapsTests.test_wrapped_chain_preserved_on_unbound_function decorators.tests_llm.MethodDecoratorWrapsTests.test_wraps_decorator_from_factory_preserves_name decorators.tests_llm.MethodDecoratorWrapsTests.test_wraps_decorator_preserves_name_on_instance_method decorators.tests_llm.record_name_dec decorators.tests_llm.wraps_with_attr
coverage json -o coverage.json
: '>>>>> End Test Output'
