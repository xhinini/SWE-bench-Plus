#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 decorators.tests_llm.MethodDecoratorRegressionTests.test_annotations_preserved_on_method_object decorators.tests_llm.MethodDecoratorRegressionTests.test_class_decoration_preserves_name_and_wrapped decorators.tests_llm.MethodDecoratorRegressionTests.test_decorating_dunder_call_preserves_name decorators.tests_llm.MethodDecoratorRegressionTests.test_descriptor_wrapper_preserves_name decorators.tests_llm.MethodDecoratorRegressionTests.test_iterable_of_decorators_preserves_name_and_wrapped decorators.tests_llm.MethodDecoratorRegressionTests.test_multiple_wrappers_and_wrapped_chain decorators.tests_llm.MethodDecoratorRegressionTests.test_preserve_name_and_wrapped_on_method
coverage json -o coverage.json
: '>>>>> End Test Output'
