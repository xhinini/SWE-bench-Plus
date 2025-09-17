#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.FunctionTypeSerializerTests.test_imports_included_for_nested_class_method migrations.test_writer_llm.FunctionTypeSerializerTests.test_multiple_nested_serializations_are_distinct migrations.test_writer_llm.FunctionTypeSerializerTests.test_serialization_of_different_nested_structures migrations.test_writer_llm.FunctionTypeSerializerTests.test_serialize_module_level_nested_class_method migrations.test_writer_llm.FunctionTypeSerializerTests.test_serialize_same_named_nested_classes_method migrations.test_writer_llm.FunctionTypeSerializerTests.test_serialize_single_level_nested_class_method migrations.test_writer_llm.FunctionTypeSerializerTests.test_serialize_three_level_nested_class_method migrations.test_writer_llm.FunctionTypeSerializerTests.test_serialized_strings_contain_all_outer_class_names migrations.test_writer_llm.method'] (migrations.test_writer_llm.ModuleOuter.['Inner) migrations.test_writer_llm.method']"] (migrations.test_writer_llm.FunctionTypeSerializerTests.["Outer.['Inner) migrations.test_writer_llm.method']"] (migrations.test_writer_llm.FunctionTypeSerializerTests.["OuterSameName.['OuterSameName) migrations.test_writer_llm.method\']"]'] (migrations.test_writer_llm.FunctionTypeSerializerTests.['Outer2.["Inner2.[\'Inner3)
coverage json -o coverage.json
: '>>>>> End Test Output'
