#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.TestNestedClassMethodSerialization._assert_serialized_member migrations.test_writer_llm.TestNestedClassMethodSerialization.test_double_nested_classmethod migrations.test_writer_llm.TestNestedClassMethodSerialization.test_double_nested_instance_method migrations.test_writer_llm.TestNestedClassMethodSerialization.test_mixed_regular_and_classmethod migrations.test_writer_llm.TestNestedClassMethodSerialization.test_same_named_inner_classes_different_outers migrations.test_writer_llm.TestNestedClassMethodSerialization.test_single_level_classmethod migrations.test_writer_llm.TestNestedClassMethodSerialization.test_single_level_regular_method migrations.test_writer_llm.TestNestedClassMethodSerialization.test_single_level_staticmethod migrations.test_writer_llm.TestNestedClassMethodSerialization.test_staticmethod_in_different_outer migrations.test_writer_llm.TestNestedClassMethodSerialization.test_triple_nested_classmethod migrations.test_writer_llm.deep_method']"] (migrations.test_writer_llm.OuterTwo.["Mid.['InnerMost.deep_clsmethod', 'InnerMost) migrations.test_writer_llm.inner_static'] (migrations.test_writer_llm.OuterFour.['InnerA) migrations.test_writer_llm.level1_cls'] (migrations.test_writer_llm.NestedMixed.['Level1.regular_method', 'Level1) migrations.test_writer_llm.same_name_cm'] (migrations.test_writer_llm.AnotherOuter.['InnerSameName) migrations.test_writer_llm.same_name_cm'] (migrations.test_writer_llm.NestedDifferentOuter.['InnerSameName) migrations.test_writer_llm.stmethod'] (migrations.test_writer_llm.OuterOne.['Inner.method', 'Inner.clsmethod', 'Inner) migrations.test_writer_llm.triple_clsmethod\']"]'] (migrations.test_writer_llm.OuterThree.['MidA.["MidB.[\'InnerC)
coverage json -o coverage.json
: '>>>>> End Test Output'
