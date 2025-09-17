#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm._add_nested_function_tests migrations.test_writer_llm.test_classmethod_via_alias migrations.test_writer_llm.test_multiple_aliasing_and_access migrations.test_writer_llm.test_nested_four_level_classmethod migrations.test_writer_llm.test_nested_three_level_classmethod migrations.test_writer_llm.test_nested_three_level_staticmethod migrations.test_writer_llm.test_nested_two_level_classmethod migrations.test_writer_llm.test_nested_two_level_staticmethod migrations.test_writer_llm.test_repeated_access_on_class migrations.test_writer_llm.test_staticmethod_and_classmethod_different_results migrations.test_writer_llm.test_staticmethod_via_alias
coverage json -o coverage.json
: '>>>>> End Test Output'
