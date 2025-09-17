#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_autodetector_llm.NoToForeignKey.deconstruct migrations.test_autodetector_llm.NoToManyToMany.deconstruct migrations.test_autodetector_llm.OnlyRelationAgnosticFieldsRegressionTests.setUp migrations.test_autodetector_llm.OnlyRelationAgnosticFieldsRegressionTests.test_only_relation_agnostic_fields_preserves_to_when_remote_model_falsey
coverage json -o coverage.json
: '>>>>> End Test Output'
