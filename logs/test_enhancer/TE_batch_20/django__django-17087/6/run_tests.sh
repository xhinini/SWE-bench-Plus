#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.FunctionTypeSerializerRegressionTests._assert_classmethod_serialized migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_exec_round_trip_four_level migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_exec_round_trip_three_level migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_exec_round_trip_two_level migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_four_level_nested_classmethod migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_multiple_nested_classmethods_serialization_consistency migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_three_level_nested_classmethod migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_three_level_nested_classmethod_variation migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_two_level_nested_classmethod migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_two_level_nested_classmethod_variation migrations.test_writer_llm.deep\\\']"]\']'] (migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.['D.[\'E.["F.[\\\'G) migrations.test_writer_llm.m\']"]'] (migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.['A.["B.[\'C) migrations.test_writer_llm.method']"] (migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.["Outer.['Inner) migrations.test_writer_llm.pqr\']"]'] (migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.['P.["Q.[\'R) migrations.test_writer_llm.xy']"] (migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.["X.['Y)
coverage json -o coverage.json
: '>>>>> End Test Output'
