#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_add_autofield_pk_with_existing_rows_remakes_table schema.tests_llm.test_add_autofield_primary_key_remakes_table schema.tests_llm.test_add_bigautofield_primary_key_remakes_table schema.tests_llm.test_add_char_pk_preserves_uniques_and_indexes schema.tests_llm.test_add_charfield_primary_key_remakes_table schema.tests_llm.test_add_integer_pk_without_default_does_remake schema.tests_llm.test_add_integerfield_primary_key_remakes_table schema.tests_llm.test_add_primary_key_updates_foreign_key_references schema.tests_llm.test_add_smallautofield_primary_key_remakes_table
coverage json -o coverage.json
: '>>>>> End Test Output'
