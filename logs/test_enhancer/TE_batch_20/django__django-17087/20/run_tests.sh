#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.FunctionTypeSerializerTests.test_classmethod_and_instance_methods_different migrations.test_writer_llm.FunctionTypeSerializerTests.test_plain_instance_method_serialization_qualname migrations.test_writer_llm.FunctionTypeSerializerTests.test_same_method_name_in_different_nested_classes migrations.test_writer_llm.FunctionTypeSerializerTests.test_serialize_classmethod_in_list_and_imports migrations.test_writer_llm.FunctionTypeSerializerTests.test_serialize_classmethod_nested_one_level migrations.test_writer_llm.FunctionTypeSerializerTests.test_serialize_classmethod_nested_three_diff_class migrations.test_writer_llm.FunctionTypeSerializerTests.test_serialize_classmethod_nested_two_levels migrations.test_writer_llm.FunctionTypeSerializerTests.test_serialize_classmethod_roundtrip_exec migrations.test_writer_llm.FunctionTypeSerializerTests.test_serialize_classmethod_used_as_field_default migrations.test_writer_llm.FunctionTypeSerializerTests.test_serializing_classmethod_deep_qualname_not_locals migrations.test_writer_llm.class_method'] (migrations.test_writer_llm.OuterFive.['InnerFive.instance_method', 'InnerFive) migrations.test_writer_llm.cm'] (migrations.test_writer_llm.OuterThree.['InnerThree) migrations.test_writer_llm.deep_method']"] (migrations.test_writer_llm.OuterTwo.["InnerTwo.['Deep) migrations.test_writer_llm.my_method'] (migrations.test_writer_llm.OuterOne.['Inner) migrations.test_writer_llm.same_name'] (migrations.test_writer_llm.OuterFour.['InnerFour)
coverage json -o coverage.json
: '>>>>> End Test Output'
