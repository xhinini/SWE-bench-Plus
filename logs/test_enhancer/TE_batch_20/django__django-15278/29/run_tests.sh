#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm._assert_add_primary_key_remakes_table schema.tests_llm.test_add_primary_key_after_removal_sets_pk schema.tests_llm.test_add_primary_key_autofield_remakes_table schema.tests_llm.test_add_primary_key_bigautofield_remakes_table schema.tests_llm.test_add_primary_key_bigintegerfield_remakes_table schema.tests_llm.test_add_primary_key_charfield_non_null_remakes_table schema.tests_llm.test_add_primary_key_charfield_remakes_table schema.tests_llm.test_add_primary_key_integerfield_remakes_table schema.tests_llm.test_add_primary_key_slugfield_remakes_table schema.tests_llm.test_add_primary_key_smallautofield_remakes_table schema.tests_llm.test_add_primary_key_uuidfield_remakes_table
coverage json -o coverage.json
: '>>>>> End Test Output'
