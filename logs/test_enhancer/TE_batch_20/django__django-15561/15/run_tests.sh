#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.NonDBAttrsTests.test_binaryfield_custom_non_db_attr_ignored schema.tests_llm.NonDBAttrsTests.test_charfield_custom_non_db_attr_ignored schema.tests_llm.NonDBAttrsTests.test_datefield_custom_non_db_attr_ignored schema.tests_llm.NonDBAttrsTests.test_datetimefield_custom_non_db_attr_ignored schema.tests_llm.NonDBAttrsTests.test_decimalfield_custom_non_db_attr_ignored schema.tests_llm.NonDBAttrsTests.test_durationfield_custom_non_db_attr_ignored schema.tests_llm.NonDBAttrsTests.test_integerfield_custom_non_db_attr_ignored schema.tests_llm.NonDBAttrsTests.test_slugfield_custom_non_db_attr_ignored schema.tests_llm.NonDBAttrsTests.test_textfield_custom_non_db_attr_ignored schema.tests_llm.NonDBAttrsTests.test_uuidfield_custom_non_db_attr_ignored
coverage json -o coverage.json
: '>>>>> End Test Output'
