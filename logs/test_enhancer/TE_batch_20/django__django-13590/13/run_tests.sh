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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 expressions.tests_llm.ResolveLookupValueCustomTupleTests._get_query expressions.tests_llm.ResolveLookupValueCustomTupleTests.setUpTestData expressions.tests_llm.ResolveLookupValueCustomTupleTests.test_deeply_nested_list_and_tuple_subclass_resolution expressions.tests_llm.ResolveLookupValueCustomTupleTests.test_direct_custom_tuple_subclass_resolution expressions.tests_llm.ResolveLookupValueCustomTupleTests.test_in_lookup_using_custom_tuple_subclass_as_iterable expressions.tests_llm.ResolveLookupValueCustomTupleTests.test_instance_level__fields_attribute_does_not_force_namedtuple_construction expressions.tests_llm.ResolveLookupValueCustomTupleTests.test_list_containing_custom_tuple_subclass_resolution expressions.tests_llm.ResolveLookupValueCustomTupleTests.test_multiple_lengths_custom_tuple_subclass expressions.tests_llm.ResolveLookupValueCustomTupleTests.test_nested_structures_resolution expressions.tests_llm.ResolveLookupValueCustomTupleTests.test_range_lookup_with_custom_tuple_subclass expressions.tests_llm.ResolveLookupValueCustomTupleTests.test_tuple_containing_custom_tuple_subclass_resolution
coverage json -o coverage.json
: '>>>>> End Test Output'
