#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.AlterModelManagersRegressionTests.assertDoesNotOptimize migrations.test_optimizer_llm.AlterModelManagersRegressionTests.assertOptimizesTo migrations.test_optimizer_llm.AlterModelManagersRegressionTests.optimize migrations.test_optimizer_llm.AlterModelManagersRegressionTests.serialize migrations.test_optimizer_llm.AlterModelManagersRegressionTests.test_create_alter_options_and_managers
coverage json -o coverage.json
: '>>>>> End Test Output'
