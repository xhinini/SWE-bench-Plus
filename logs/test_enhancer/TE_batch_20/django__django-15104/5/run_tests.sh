#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_autodetector_llm.OnlyRelationAgnosticFieldsTests.setUp migrations.test_autodetector_llm.OnlyRelationAgnosticFieldsTests.test_custom_field_with_remote_field_and_deconstruct_with_to_removed migrations.test_autodetector_llm.OnlyRelationAgnosticFieldsTests.test_custom_many_to_many_deconstruct_omits_to_safe
coverage json -o coverage.json
: '>>>>> End Test Output'
