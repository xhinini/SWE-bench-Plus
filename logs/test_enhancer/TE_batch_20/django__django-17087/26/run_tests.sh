#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_another_level1_variant migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_level1_nested_classmethod_serialization migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_level2_nested_classmethod_serialization migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_level2_variant migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_level3_nested_classmethod_serialization migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_level3_variant migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_level4_nested_classmethod_serialization migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_level4_variant migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_level5_nested_classmethod_serialization migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_level5_variant migrations.test_writer_llm.cm'] (migrations.test_writer_llm.Outer1.['Inner1) migrations.test_writer_llm.cm'] (migrations.test_writer_llm.Outer6.['Inner6) migrations.test_writer_llm.cm']"] (migrations.test_writer_llm.Outer2.["Mid.['Inner2) migrations.test_writer_llm.cm']"] (migrations.test_writer_llm.Outer7.["A.['Inner7) migrations.test_writer_llm.cm\']"]'] (migrations.test_writer_llm.Outer3.['A.["B.[\'Inner3) migrations.test_writer_llm.cm\']"]'] (migrations.test_writer_llm.Outer8.['A.["B.[\'Inner8) migrations.test_writer_llm.cm\\\']"]\']'] (migrations.test_writer_llm.Outer4.['A.[\'B.["C.[\\\'Inner4) migrations.test_writer_llm.cm\\\']"]\']'] (migrations.test_writer_llm.Outer9.['A.[\'B.["C.[\\\'Inner9) migrations.test_writer_llm.cm\\\\\\\']"]\\\']\']'] (migrations.test_writer_llm.Outer10.['A.[\'B.[\\\'C.["D.[\\\\\\\'Inner10) migrations.test_writer_llm.cm\\\\\\\']"]\\\']\']'] (migrations.test_writer_llm.Outer5.['A.[\'B.[\\\'C.["D.[\\\\\\\'Inner5)
coverage json -o coverage.json
: '>>>>> End Test Output'
