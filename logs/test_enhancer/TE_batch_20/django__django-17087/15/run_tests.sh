#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.FunctionSerializerNestedTests.assert_serialized_matches_qualname migrations.test_writer_llm.FunctionSerializerNestedTests.test_class_and_instance_method_serialization_consistency migrations.test_writer_llm.FunctionSerializerNestedTests.test_serialize_deeply_nested_class_classmethod migrations.test_writer_llm.FunctionSerializerNestedTests.test_serialize_deeply_nested_class_method migrations.test_writer_llm.FunctionSerializerNestedTests.test_serialize_deeply_nested_class_staticmethod migrations.test_writer_llm.FunctionSerializerNestedTests.test_serialize_instance_bound_method migrations.test_writer_llm.FunctionSerializerNestedTests.test_serialize_local_class_method_raises migrations.test_writer_llm.FunctionSerializerNestedTests.test_serialize_nested_class_classmethod migrations.test_writer_llm.FunctionSerializerNestedTests.test_serialize_nested_class_method migrations.test_writer_llm.FunctionSerializerNestedTests.test_serialize_nested_class_staticmethod migrations.test_writer_llm.smethod']"] (migrations.test_writer_llm.FunctionSerializerNestedTests.["OuterOne.['Inner.method', 'Inner.cmethod', 'Inner) migrations.test_writer_llm.smethod\']"]'] (migrations.test_writer_llm.FunctionSerializerNestedTests.['OuterTwo.["Middle.[\'Inner.method\', \'Inner.cmethod\', \'Inner)
coverage json -o coverage.json
: '>>>>> End Test Output'
