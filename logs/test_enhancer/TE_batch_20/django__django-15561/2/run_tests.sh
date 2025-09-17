#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.FieldNonDBAttrsTests.test_non_db_attrs_contains_choices schema.tests_llm.FieldNonDBAttrsTests.test_non_db_attrs_contains_db_column schema.tests_llm.FieldNonDBAttrsTests.test_non_db_attrs_contains_on_delete schema.tests_llm.FieldNonDBAttrsTests.test_non_db_attrs_contains_validators schema.tests_llm.FieldNonDBAttrsTests.test_non_db_attrs_contains_verbose_name schema.tests_llm.FieldNonDBAttrsTests.test_non_db_attrs_exists_on_field schema.tests_llm.FieldNonDBAttrsTests.test_non_db_attrs_expected_contents schema.tests_llm.FieldNonDBAttrsTests.test_non_db_attrs_immutable_type schema.tests_llm.FieldNonDBAttrsTests.test_non_db_attrs_inherited_by_subclass schema.tests_llm.FieldNonDBAttrsTests.test_non_db_attrs_is_tuple
coverage json -o coverage.json
: '>>>>> End Test Output'
