#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.NestedMethodSerializationTests.test_classmethod_serialization_single_level migrations.test_writer_llm.NestedMethodSerializationTests.test_deeply_nested_classmethod_serialization migrations.test_writer_llm.NestedMethodSerializationTests.test_import_set_contains_module_for_deep_classmethod migrations.test_writer_llm.NestedMethodSerializationTests.test_import_set_contains_module_for_staticmethod migrations.test_writer_llm.NestedMethodSerializationTests.test_instance_bound_method_serialization migrations.test_writer_llm.NestedMethodSerializationTests.test_local_class_classmethod_raises migrations.test_writer_llm.NestedMethodSerializationTests.test_serialized_string_executes_for_classmethod migrations.test_writer_llm.NestedMethodSerializationTests.test_serialized_string_executes_for_instance_method_reference migrations.test_writer_llm.NestedMethodSerializationTests.test_serialized_string_executes_for_staticmethod migrations.test_writer_llm.NestedMethodSerializationTests.test_staticmethod_serialization_nested migrations.test_writer_llm.deep_class_meth']"] (migrations.test_writer_llm.OuterTwo.["InnerA.['InnerB) migrations.test_writer_llm.inst_meth'] (migrations.test_writer_llm.OuterOne.['Inner.class_meth', 'Inner.static_meth', 'Inner)
coverage json -o coverage.json
: '>>>>> End Test Output'
