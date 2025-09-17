#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 basic.tests_llm.ManagerWrapsRegressionTests._signature_without_self basic.tests_llm.ManagerWrapsRegressionTests.test_private_methods_are_not_copied
coverage json -o coverage.json
: '>>>>> End Test Output'
