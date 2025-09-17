#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 expressions.tests_llm.CustomTupleSubclassTests._create_company expressions.tests_llm.CustomTupleSubclassTests._make_weird expressions.tests_llm.CustomTupleSubclassTests.test_in_lookup_with_custom_tuple_subclass_and_F_expressions expressions.tests_llm.CustomTupleSubclassTests.test_in_lookup_with_custom_tuple_subclass_and_namedtuple_like_classmethod expressions.tests_llm.CustomTupleSubclassTests.test_in_lookup_with_custom_tuple_subclass_mixed_int_and_F expressions.tests_llm.CustomTupleSubclassTests.test_in_lookup_with_custom_tuple_subclass_plain_ints expressions.tests_llm.CustomTupleSubclassTests.test_range_lookup_with_custom_tuple_subclass_and_F_expressions expressions.tests_llm.CustomTupleSubclassTests.test_range_lookup_with_custom_tuple_subclass_and_namedtuple_like_classmethod expressions.tests_llm.CustomTupleSubclassTests.test_range_lookup_with_custom_tuple_subclass_mixed_int_and_F expressions.tests_llm.CustomTupleSubclassTests.test_range_lookup_with_custom_tuple_subclass_plain_ints
coverage json -o coverage.json
: '>>>>> End Test Output'
