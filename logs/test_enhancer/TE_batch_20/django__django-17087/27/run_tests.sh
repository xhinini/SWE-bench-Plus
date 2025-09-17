#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.FunctionTypeSerializerRegressionTests._expected migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_alias_reference migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_getattr_access migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_method_import_includes_module migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_multi_nested migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_multiple_references migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_nested_one_level migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_nested_three_levels migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_nested_two_levels migrations.test_writer_llm.FunctionTypeSerializerRegressionTests.test_subclass_method_serialization migrations.test_writer_llm.action']"] (migrations.test_writer_llm.TwoLevelA.["TwoLevelB.['InnerMost) migrations.test_writer_llm.cm'] (migrations.test_writer_llm.LevelOne.['Inner) migrations.test_writer_llm.do_it']"] (migrations.test_writer_llm.ThreeA.["B.['C) migrations.test_writer_llm.foo']"] (migrations.test_writer_llm.Multi.["X.['Y)
coverage json -o coverage.json
: '>>>>> End Test Output'
