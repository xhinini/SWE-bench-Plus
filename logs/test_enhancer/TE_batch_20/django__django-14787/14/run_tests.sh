#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 decorators.tests_llm.DecoratorsRegressionTests.test_class_level_method_decorator_preserves_signature decorators.tests_llm.DecoratorsRegressionTests.test_decorated_call_method_preserves_signature decorators.tests_llm.DecoratorsRegressionTests.test_decorator_using_wraps_preserves_signature decorators.tests_llm.DecoratorsRegressionTests.test_decorator_without_wraps_preserves_signature decorators.tests_llm.DecoratorsRegressionTests.test_descriptor_wrapper_preserves_signature decorators.tests_llm.DecoratorsRegressionTests.test_identity_decorator_preserves_wrapped_and_signature decorators.tests_llm.DecoratorsRegressionTests.test_multiple_wrapped_chain_points_to_original decorators.tests_llm.DecoratorsRegressionTests.test_signature_with_keyword_only_and_varargs decorators.tests_llm.DecoratorsRegressionTests.test_tuple_of_decorators_preserves_signature
coverage json -o coverage.json
: '>>>>> End Test Output'
