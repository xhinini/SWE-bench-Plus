#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.FunctionTypeSerializerTests.test_imports_for_nested_classmethods migrations.test_writer_llm.FunctionTypeSerializerTests.test_roundtrip_classmethod_top_level_one migrations.test_writer_llm.FunctionTypeSerializerTests.test_roundtrip_classmethod_top_level_two_levels migrations.test_writer_llm.FunctionTypeSerializerTests.test_roundtrip_staticmethod_top_level_nested migrations.test_writer_llm.FunctionTypeSerializerTests.test_serialize_classmethod_top_level_one migrations.test_writer_llm.FunctionTypeSerializerTests.test_serialize_classmethod_top_level_three_levels migrations.test_writer_llm.FunctionTypeSerializerTests.test_serialize_classmethod_top_level_two_levels migrations.test_writer_llm.FunctionTypeSerializerTests.test_serialize_staticmethod_top_level_nested migrations.test_writer_llm.FunctionTypeSerializerTests.test_serialize_writerstest_nestedchoices_method_again migrations.test_writer_llm.FunctionTypeSerializerTests.test_serializer_factory_returns_function_type_serializer_for_bound_method migrations.test_writer_llm.method'] (migrations.test_writer_llm.TopLevelOne.['Inner) migrations.test_writer_llm.method'] (migrations.test_writer_llm.TopLevelTwo.['InnerC) migrations.test_writer_llm.method']"] (migrations.test_writer_llm.TopLevelTwo.["InnerA.['InnerB) migrations.test_writer_llm.method\']"]'] (migrations.test_writer_llm.TopLevelThree.['A.["B.[\'C)
coverage json -o coverage.json
: '>>>>> End Test Output'
