#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 decorators.tests_llm.RegressionMethodDecoratorWrapsTests.test_multiple_wraps_decorators_preserve_func_name_order_independent
coverage json -o coverage.json
: '>>>>> End Test Output'
