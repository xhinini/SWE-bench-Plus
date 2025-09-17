#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.TestNestedClassMethodSerialization.test_bound_method_round_trip_exec migrations.test_writer_llm.TestNestedClassMethodSerialization.test_classmethod_imports_set migrations.test_writer_llm.TestNestedClassMethodSerialization.test_four_level_classmethod_serialization migrations.test_writer_llm.TestNestedClassMethodSerialization.test_local_class_method_raises migrations.test_writer_llm.TestNestedClassMethodSerialization.test_method_name_clash_serialization migrations.test_writer_llm.TestNestedClassMethodSerialization.test_staticmethod_imports_set migrations.test_writer_llm.TestNestedClassMethodSerialization.test_staticmethod_serialization migrations.test_writer_llm.TestNestedClassMethodSerialization.test_three_level_classmethod_serialization migrations.test_writer_llm.TestNestedClassMethodSerialization.test_two_level_classmethod_serialization migrations.test_writer_llm.cm\']"]'] (migrations.test_writer_llm.TestNestedClassMethodSerialization.['ThreeLevel.["Mid.[\'Inner) migrations.test_writer_llm.cm\\\']"]\']'] (migrations.test_writer_llm.TestNestedClassMethodSerialization.['FourLevel.[\'A.["B.[\\\'C) migrations.test_writer_llm.method']"] (migrations.test_writer_llm.TestNestedClassMethodSerialization.["Clash.['Inner) migrations.test_writer_llm.st']"] (migrations.test_writer_llm.TestNestedClassMethodSerialization.["MultiLevel.['Inner.cm', 'Inner)
coverage json -o coverage.json
: '>>>>> End Test Output'
