#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests._make_rel invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_hashable_for_non_empty_through_fields
coverage json -o coverage.json
: '>>>>> End Test Output'
