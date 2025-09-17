#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.cm'] (migrations.test_writer_llm.OuterLevel1.['InnerLevel1) migrations.test_writer_llm.cm']"] (migrations.test_writer_llm.OuterLevel2.["InnerA.['InnerB) migrations.test_writer_llm.cm\']"]'] (migrations.test_writer_llm.OuterLevel3.['InnerX.["InnerY.[\'InnerZ) migrations.test_writer_llm.test_serialize_classmethod_nested_level1_result migrations.test_writer_llm.test_serialize_classmethod_nested_level1_roundtrip_bound migrations.test_writer_llm.test_serialize_classmethod_nested_level2_result migrations.test_writer_llm.test_serialize_classmethod_nested_level2_roundtrip_bound migrations.test_writer_llm.test_serialize_classmethod_nested_level3_result migrations.test_writer_llm.test_serialize_classmethod_nested_level3_roundtrip_bound migrations.test_writer_llm.test_serialize_deeply_nested_qualname_in_string migrations.test_writer_llm.test_serializer_factory_returns_function_serializer_level1 migrations.test_writer_llm.test_serializer_factory_returns_function_serializer_level2 migrations.test_writer_llm.test_serializer_factory_returns_function_serializer_level3
coverage json -o coverage.json
: '>>>>> End Test Output'
