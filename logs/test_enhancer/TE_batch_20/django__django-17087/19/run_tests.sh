#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.NestedMethodSerializationTests._assert_serialized_method_equal migrations.test_writer_llm.NestedMethodSerializationTests._assert_serialized_type_equal migrations.test_writer_llm.NestedMethodSerializationTests.test_round_trip_exec_nested_classmethod migrations.test_writer_llm.NestedMethodSerializationTests.test_serialize_class_of_nested_level1 migrations.test_writer_llm.NestedMethodSerializationTests.test_serialize_class_of_nested_level2 migrations.test_writer_llm.NestedMethodSerializationTests.test_serialize_class_of_nested_level3 migrations.test_writer_llm.NestedMethodSerializationTests.test_serialize_classmethod_nested_level1 migrations.test_writer_llm.NestedMethodSerializationTests.test_serialize_classmethod_nested_level2 migrations.test_writer_llm.NestedMethodSerializationTests.test_serialize_classmethod_nested_level3 migrations.test_writer_llm.NestedMethodSerializationTests.test_serialize_staticmethod_nested migrations.test_writer_llm.NestedMethodSerializationTests.test_serialized_string_contains_outer_class_name migrations.test_writer_llm.cm\']"]'] (migrations.test_writer_llm.NestedMethodSerializationTests.['Outer2.["Middle.[\'Inner) migrations.test_writer_llm.cm\\\']"]\']'] (migrations.test_writer_llm.NestedMethodSerializationTests.['Outer3.[\'Middle.["Inner.[\\\'Deep) migrations.test_writer_llm.sm']"] (migrations.test_writer_llm.NestedMethodSerializationTests.["Outer1.['Inner.cm', 'Inner)
coverage json -o coverage.json
: '>>>>> End Test Output'
