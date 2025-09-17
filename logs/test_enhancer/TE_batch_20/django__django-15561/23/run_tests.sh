#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.NonDbAttrTests.test_custom_base_field_non_db_attr_noop schema.tests_llm.NonDbAttrTests.test_custom_binaryfield_non_db_attr_noop schema.tests_llm.NonDbAttrTests.test_custom_charfield_non_db_attr_noop schema.tests_llm.NonDbAttrTests.test_custom_datetimefield_non_db_attr_noop schema.tests_llm.NonDbAttrTests.test_custom_durationfield_non_db_attr_noop schema.tests_llm.NonDbAttrTests.test_custom_floatfield_non_db_attr_noop schema.tests_llm.NonDbAttrTests.test_custom_integerfield_non_db_attr_noop schema.tests_llm.NonDbAttrTests.test_custom_slugfield_non_db_attr_noop schema.tests_llm.NonDbAttrTests.test_custom_textfield_non_db_attr_noop schema.tests_llm.NonDbAttrTests.test_custom_uuidfield_non_db_attr_noop
coverage json -o coverage.json
: '>>>>> End Test Output'
