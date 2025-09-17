#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.test_local_class_classmethod_raises_value_error migrations.test_writer_llm.test_local_class_method_raises_value_error migrations.test_writer_llm.test_nested_class_method_in_testcase_style migrations.test_writer_llm.test_serialize_classmethod_three_levels migrations.test_writer_llm.test_serialize_nested_class_classmethod migrations.test_writer_llm.test_serialize_nested_class_method_four_levels migrations.test_writer_llm.test_serialize_nested_class_method_three_levels migrations.test_writer_llm.test_serialize_nested_class_method_two_levels migrations.test_writer_llm.test_serialize_nested_class_staticmethod migrations.test_writer_llm.test_serialize_staticmethod_three_levels
coverage json -o coverage.json
: '>>>>> End Test Output'
