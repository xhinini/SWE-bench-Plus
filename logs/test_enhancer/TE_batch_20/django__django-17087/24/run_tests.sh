#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.bar']"] (migrations.test_writer_llm.DeepOuter.["Mid.['Inner) migrations.test_writer_llm.baz'] (migrations.test_writer_llm.StaticOuter.['InnerStatic) migrations.test_writer_llm.deep\']"]'] (migrations.test_writer_llm.Deepest.['A.["B.[\'C) migrations.test_writer_llm.foo'] (migrations.test_writer_llm.OuterOne.['InnerOne) migrations.test_writer_llm.foo'] (migrations.test_writer_llm.OuterTwo.['InnerOne) migrations.test_writer_llm.test_serialize_all_nested_cases_unique migrations.test_writer_llm.test_serialize_imports_for_nested_method migrations.test_writer_llm.test_serialize_method_nested_one_level migrations.test_writer_llm.test_serialize_method_nested_three_levels migrations.test_writer_llm.test_serialize_method_nested_two_levels migrations.test_writer_llm.test_serialize_method_roundtrip_call migrations.test_writer_llm.test_serialize_nested_names_contain_writer_class migrations.test_writer_llm.test_serialize_same_inner_name_in_different_outer migrations.test_writer_llm.test_serialize_staticmethod_in_nested_class
coverage json -o coverage.json
: '>>>>> End Test Output'
