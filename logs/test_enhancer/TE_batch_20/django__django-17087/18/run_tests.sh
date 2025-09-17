#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.FunctionTypeSerializerTests.test_classmethod_deep_nested_level3 migrations.test_writer_llm.FunctionTypeSerializerTests.test_classmethod_nested_level1 migrations.test_writer_llm.FunctionTypeSerializerTests.test_classmethod_nested_level2 migrations.test_writer_llm.FunctionTypeSerializerTests.test_distinct_inner_classes_with_same_name migrations.test_writer_llm.FunctionTypeSerializerTests.test_instance_bound_method_nested_level1 migrations.test_writer_llm.FunctionTypeSerializerTests.test_instance_bound_method_nested_level2 migrations.test_writer_llm.FunctionTypeSerializerTests.test_subclass_of_nested_class_serializes_to_its_own_qualname migrations.test_writer_llm.FunctionTypeSerializerTests.test_unbound_method_nested_level1 migrations.test_writer_llm.FunctionTypeSerializerTests.test_unbound_method_nested_level2 migrations.test_writer_llm.cm']"] (migrations.test_writer_llm.FunctionTypeSerializerTests.["OuterA.['Inner) migrations.test_writer_llm.cm']"] (migrations.test_writer_llm.FunctionTypeSerializerTests.["OuterB.['Inner) migrations.test_writer_llm.deep\\\']"]\']'] (migrations.test_writer_llm.FunctionTypeSerializerTests.['OuterLevel3.[\'InnerA.["InnerB.[\\\'InnerC) migrations.test_writer_llm.im']"] (migrations.test_writer_llm.FunctionTypeSerializerTests.["OuterLevel1.['InnerLevel1.cm', 'InnerLevel1) migrations.test_writer_llm.im2\']"]'] (migrations.test_writer_llm.FunctionTypeSerializerTests.['OuterLevel2.["InnerLevel2.[\'InnerMost.cm2\', \'InnerMost) migrations.test_writer_llm.subcm'] (migrations.test_writer_llm.FunctionTypeSerializerTests.['SubclassOfInner)
coverage json -o coverage.json
: '>>>>> End Test Output'
