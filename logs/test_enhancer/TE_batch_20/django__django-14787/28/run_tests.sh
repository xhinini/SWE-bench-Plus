#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 decorators.tests_llm.MethodDecoratorRegressionTests.test_decorator_on_descriptor_with_wraps decorators.tests_llm.MethodDecoratorRegressionTests.test_wraps_decorator_preserves_name_on_unbound_and_bound decorators.tests_llm.attr_deco decorators.tests_llm.inspect_name_deco decorators.tests_llm.module_inspector_deco decorators.tests_llm.wraps_deco
coverage json -o coverage.json
: '>>>>> End Test Output'
