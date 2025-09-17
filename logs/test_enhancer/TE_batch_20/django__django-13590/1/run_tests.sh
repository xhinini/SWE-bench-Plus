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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 expressions.tests_llm.IterableLookupInnerExpressionsTests.test_exclude_range_custom_tuple_subclass expressions.tests_llm.IterableLookupInnerExpressionsTests.test_exclude_with_list_of_weird_inside_Q expressions.tests_llm.IterableLookupInnerExpressionsTests.test_filter_list_containing_custom_tuple_subclass expressions.tests_llm.IterableLookupInnerExpressionsTests.test_in_lookup_custom_tuple_subclass expressions.tests_llm.IterableLookupInnerExpressionsTests.test_in_with_F_inside_custom_tuple expressions.tests_llm.IterableLookupInnerExpressionsTests.test_mixed_elements_in_custom_tuple expressions.tests_llm.IterableLookupInnerExpressionsTests.test_multiple_filters_with_weird expressions.tests_llm.IterableLookupInnerExpressionsTests.test_range_lookup_custom_tuple_subclass expressions.tests_llm.IterableLookupInnerExpressionsTests.test_range_with_F_inside_custom_tuple expressions.tests_llm.IterableLookupInnerExpressionsTests.test_typing_namedtuple_range
coverage json -o coverage.json
: '>>>>> End Test Output'
