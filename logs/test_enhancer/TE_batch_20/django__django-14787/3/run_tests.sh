#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 decorators.tests_llm.MethodDecoratorRegressionTests.test_callable_descriptor_with_wraps_based_decorator_preserves_unwrap decorators.tests_llm.MethodDecoratorRegressionTests.test_decorator_introspects_original_via___wrapped__ decorators.tests_llm.MethodDecoratorRegressionTests.test_inspect_signature_matches_original_after_method_decorator decorators.tests_llm.MethodDecoratorRegressionTests.test_inspect_unwrap_returns_original_for_descriptor_wrapper decorators.tests_llm.introspecting_decorator decorators.tests_llm.wraps_decorator
coverage json -o coverage.json
: '>>>>> End Test Output'
