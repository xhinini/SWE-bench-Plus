#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_autodetector_llm.HardcodedForeignKey.__init__ migrations.test_autodetector_llm.HardcodedForeignKey.deconstruct migrations.test_autodetector_llm.HardcodedManyToMany.__init__ migrations.test_autodetector_llm.HardcodedManyToMany.deconstruct migrations.test_autodetector_llm.OnlyRelationAgnosticFieldsTests._assert_no_to_in_result migrations.test_autodetector_llm.OnlyRelationAgnosticFieldsTests.setUp
coverage json -o coverage.json
: '>>>>> End Test Output'
