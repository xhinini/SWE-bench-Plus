#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.SchemaTests_AddPrimaryKeyFieldMixin._add_primary_key_and_assert schema.tests_llm._attach_tests schema.tests_llm._make_test
coverage json -o coverage.json
: '>>>>> End Test Output'
