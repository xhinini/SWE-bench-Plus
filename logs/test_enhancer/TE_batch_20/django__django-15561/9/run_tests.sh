#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_custom_non_db_attr_binaryfield_no_queries schema.tests_llm.test_custom_non_db_attr_charfield_no_queries schema.tests_llm.test_custom_non_db_attr_datefield_no_queries schema.tests_llm.test_custom_non_db_attr_datetimefield_no_queries schema.tests_llm.test_custom_non_db_attr_decimalfield_no_queries schema.tests_llm.test_custom_non_db_attr_integerfield_no_queries schema.tests_llm.test_custom_non_db_attr_textfield_no_queries schema.tests_llm.test_custom_non_db_attr_timefield_no_queries schema.tests_llm.test_custom_non_db_attr_uuidfield_no_queries
coverage json -o coverage.json
: '>>>>> End Test Output'
