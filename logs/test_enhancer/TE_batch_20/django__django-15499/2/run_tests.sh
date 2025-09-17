#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.ManagerOptimizerTests.assertOptimizesTo migrations.test_optimizer_llm.ManagerOptimizerTests.optimize migrations.test_optimizer_llm.serialize
coverage json -o coverage.json
: '>>>>> End Test Output'
