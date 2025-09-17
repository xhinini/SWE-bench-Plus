#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.HashStabilityTests.test_abstract_model_assignment_hash_stability model_fields.tests_llm.HashStabilityTests.test_app_label_model_assignment_hash_stability
coverage json -o coverage.json
: '>>>>> End Test Output'
