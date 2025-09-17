#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 dbshell.test_postgresql_llm.AdditionalPostgresClientTests.test_multiple_parameters_preserve_order_and_no_duplication
coverage json -o coverage.json
: '>>>>> End Test Output'
