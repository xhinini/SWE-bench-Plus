#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.NestedClassMethodSerializationTests.test_imports_are_correct_for_nested_methods migrations.test_writer_llm.NestedClassMethodSerializationTests.test_method_name_preserved migrations.test_writer_llm.NestedClassMethodSerializationTests.test_module_level_one_level migrations.test_writer_llm.NestedClassMethodSerializationTests.test_module_level_same_inner_name_different_outers migrations.test_writer_llm.NestedClassMethodSerializationTests.test_module_level_three_levels migrations.test_writer_llm.NestedClassMethodSerializationTests.test_module_level_two_levels migrations.test_writer_llm.NestedClassMethodSerializationTests.test_multiple_nested_classes_differentiation migrations.test_writer_llm.NestedClassMethodSerializationTests.test_testclass_deep_nesting migrations.test_writer_llm.NestedClassMethodSerializationTests.test_testclass_level_one_level migrations.test_writer_llm.action']"] (migrations.test_writer_llm.NestedClassMethodSerializationTests.["Level1.['Level2) migrations.test_writer_llm.cm'] (migrations.test_writer_llm.OuterModule.['Inner) migrations.test_writer_llm.cm'] (migrations.test_writer_llm.OuterModuleSameNameA.['Inner) migrations.test_writer_llm.cm'] (migrations.test_writer_llm.OuterModuleSameNameB.['Inner) migrations.test_writer_llm.cm']"] (migrations.test_writer_llm.OuterModule2.["Inner1.['Inner2) migrations.test_writer_llm.do_it\']"]'] (migrations.test_writer_llm.OuterModule3.['A.["B.[\'C) migrations.test_writer_llm.nested\']"]'] (migrations.test_writer_llm.NestedClassMethodSerializationTests.['LevelA.["LevelB.[\'LevelC)
coverage json -o coverage.json
: '>>>>> End Test Output'
