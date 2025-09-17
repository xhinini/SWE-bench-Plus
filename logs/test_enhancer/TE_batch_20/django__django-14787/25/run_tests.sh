#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 decorators.tests_llm._unwrap decorators.tests_llm.wraps_and_attr decorators.tests_llm.wraps_deco decorators.tests_llm.wraps_deco_b
coverage json -o coverage.json
: '>>>>> End Test Output'
