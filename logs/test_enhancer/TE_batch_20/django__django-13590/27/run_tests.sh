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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 expressions.tests_llm.IterableLookupInnerExpressionsTests.setUpTestData expressions.tests_llm.IterableLookupInnerExpressionsTests.test_namedtuple_behavior_control expressions.tests_llm.IterableLookupInnerExpressionsTests.test_tuple_subclass_with_fields_and_duplicates expressions.tests_llm.IterableLookupInnerExpressionsTests.test_tuple_subclass_with_fields_and_mixed_types expressions.tests_llm.IterableLookupInnerExpressionsTests.test_tuple_subclass_with_fields_in_lookup_ints expressions.tests_llm.IterableLookupInnerExpressionsTests.test_tuple_subclass_with_fields_in_lookup_single_F_expression expressions.tests_llm.IterableLookupInnerExpressionsTests.test_tuple_subclass_with_fields_in_lookup_two_F_expressions expressions.tests_llm.IterableLookupInnerExpressionsTests.test_tuple_subclass_with_fields_range_lookup_ints expressions.tests_llm.IterableLookupInnerExpressionsTests.test_tuple_subclass_with_fields_range_with_F_expressions expressions.tests_llm.IterableLookupInnerExpressionsTests.test_tuple_subclass_with_fields_used_in_multiple_lookups
coverage json -o coverage.json
: '>>>>> End Test Output'
