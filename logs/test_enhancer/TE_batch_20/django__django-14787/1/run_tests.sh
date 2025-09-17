#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 decorators.tests_llm.RegressionMethodDecoratorTests.test_capture_name_on_call_special_method decorators.tests_llm.RegressionMethodDecoratorTests.test_capture_name_on_class_decoration decorators.tests_llm.RegressionMethodDecoratorTests.test_capture_name_on_method_level decorators.tests_llm.RegressionMethodDecoratorTests.test_class_based_decorator_preserves_name decorators.tests_llm.RegressionMethodDecoratorTests.test_descriptor_interaction_capture_name decorators.tests_llm.RegressionMethodDecoratorTests.test_iterable_of_decorators_capture_attributes decorators.tests_llm.RegressionMethodDecoratorTests.test_multiple_decorators_one_uses_wraps_and_other_inspects_name decorators.tests_llm.capture_name decorators.tests_llm.capture_qualname decorators.tests_llm.uses_wraps
coverage json -o coverage.json
: '>>>>> End Test Output'
