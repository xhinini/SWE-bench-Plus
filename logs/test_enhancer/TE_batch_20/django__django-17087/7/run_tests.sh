#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.NestedClassMethodSerializationTests._assert_method_in_field_default migrations.test_writer_llm.NestedClassMethodSerializationTests._assert_method_serializes_to migrations.test_writer_llm.NestedClassMethodSerializationTests._expected_method_tuple migrations.test_writer_llm.NestedClassMethodSerializationTests.test_direct_name_clash migrations.test_writer_llm.NestedClassMethodSerializationTests.test_direct_nested_a migrations.test_writer_llm.NestedClassMethodSerializationTests.test_direct_nested_b migrations.test_writer_llm.NestedClassMethodSerializationTests.test_direct_nested_c migrations.test_writer_llm.NestedClassMethodSerializationTests.test_direct_nested_d migrations.test_writer_llm.NestedClassMethodSerializationTests.test_field_default_name_clash migrations.test_writer_llm.NestedClassMethodSerializationTests.test_field_default_nested_a migrations.test_writer_llm.NestedClassMethodSerializationTests.test_field_default_nested_b migrations.test_writer_llm.NestedClassMethodSerializationTests.test_field_default_nested_c migrations.test_writer_llm.NestedClassMethodSerializationTests.test_field_default_nested_d migrations.test_writer_llm.cm_a'] (migrations.test_writer_llm.NestedA.['InnerA) migrations.test_writer_llm.cm_b']"] (migrations.test_writer_llm.NestedB.["InnerB.['InnerB2) migrations.test_writer_llm.cm_c\']"]'] (migrations.test_writer_llm.NestedC.['InnerC.["InnerC2.[\'InnerC3) migrations.test_writer_llm.cm_d'] (migrations.test_writer_llm.NestedD.['InnerD) migrations.test_writer_llm.cm_nc'] (migrations.test_writer_llm.NameClash.['NameClash)
coverage json -o coverage.json
: '>>>>> End Test Output'
