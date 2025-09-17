#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_custom_non_db_attr_noop_a schema.tests_llm.test_custom_non_db_attr_noop_b schema.tests_llm.test_custom_non_db_attr_noop_c schema.tests_llm.test_custom_non_db_attr_noop_d schema.tests_llm.test_custom_non_db_attr_noop_e schema.tests_llm.test_custom_non_db_attr_noop_f schema.tests_llm.test_custom_non_db_attr_noop_g schema.tests_llm.test_custom_non_db_attr_noop_h schema.tests_llm.test_custom_non_db_attr_noop_i schema.tests_llm.test_custom_non_db_attr_noop_j
coverage json -o coverage.json
: '>>>>> End Test Output'
