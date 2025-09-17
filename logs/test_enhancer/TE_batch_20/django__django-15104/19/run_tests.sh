#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_autodetector_llm.OnlyRelationAgnosticFieldsTests.test_create_model_with_custom_fk_no_to_does_not_error migrations.test_autodetector_llm.OnlyRelationAgnosticFieldsTests.test_remote_field_model_none_keeps_to
coverage json -o coverage.json
: '>>>>> End Test Output'
