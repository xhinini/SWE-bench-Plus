#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.FunctionTypeSerializerNestedTests._exec_serialized migrations.test_writer_llm.FunctionTypeSerializerNestedTests.test_classmethod_in_nested_choices_serialization migrations.test_writer_llm.FunctionTypeSerializerNestedTests.test_classmethod_nested_one_level_roundtrip migrations.test_writer_llm.FunctionTypeSerializerNestedTests.test_classmethod_nested_one_level_serialization migrations.test_writer_llm.FunctionTypeSerializerNestedTests.test_classmethod_nested_three_levels_roundtrip migrations.test_writer_llm.FunctionTypeSerializerNestedTests.test_classmethod_nested_three_levels_serialization migrations.test_writer_llm.FunctionTypeSerializerNestedTests.test_classmethod_nested_two_levels_roundtrip migrations.test_writer_llm.FunctionTypeSerializerNestedTests.test_classmethod_nested_two_levels_serialization migrations.test_writer_llm.FunctionTypeSerializerNestedTests.test_distinct_strings_for_same_inner_name_under_different_outers migrations.test_writer_llm.FunctionTypeSerializerNestedTests.test_staticmethod_nested_one_level_serialization migrations.test_writer_llm.cm']"] (migrations.test_writer_llm.FunctionTypeSerializerNestedTests.["A1.['Inner) migrations.test_writer_llm.cm']"] (migrations.test_writer_llm.FunctionTypeSerializerNestedTests.["A2.['Inner) migrations.test_writer_llm.cm\']"]'] (migrations.test_writer_llm.FunctionTypeSerializerNestedTests.['Outer2.["InnerA.[\'InnerB) migrations.test_writer_llm.cm\\\']"]\']'] (migrations.test_writer_llm.FunctionTypeSerializerNestedTests.['Outer3.[\'A.["B.[\\\'C) migrations.test_writer_llm.sm']"] (migrations.test_writer_llm.FunctionTypeSerializerNestedTests.["Outer1.['Inner1.cm', 'Inner1) migrations.test_writer_llm.what']"] (migrations.test_writer_llm.FunctionTypeSerializerNestedTests.["OuterChoices.['InnerChoices)
coverage json -o coverage.json
: '>>>>> End Test Output'
