#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.AddPrimaryKeyFieldTests._cleanup schema.tests_llm.AddPrimaryKeyFieldTests._create_and_remove_id schema.tests_llm.AddPrimaryKeyFieldTests.get_primary_key schema.tests_llm.AddPrimaryKeyFieldTests.test_add_primary_key_after_deleting_id_autofield
coverage json -o coverage.json
: '>>>>> End Test Output'
