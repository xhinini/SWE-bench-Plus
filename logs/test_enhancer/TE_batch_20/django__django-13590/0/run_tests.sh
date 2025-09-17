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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 expressions.tests_llm.FakeNamedIterableTests.setUpTestData expressions.tests_llm.FakeNamedIterableTests.test_in_lookup_accepts_fake_named_iterable_multiple_values_contains_c5 expressions.tests_llm.FakeNamedIterableTests.test_in_lookup_accepts_fake_named_iterable_single_value expressions.tests_llm.FakeNamedIterableTests.test_in_lookup_with_F_expression_and_fake_named_iterable expressions.tests_llm.FakeNamedIterableTests.test_in_lookup_with_mixed_fake_named_iterable_values expressions.tests_llm.FakeNamedIterableTests.test_in_lookup_with_value_and_expression_inside_fake_named_iterable expressions.tests_llm.FakeNamedIterableTests.test_multiple_evaluations_do_not_consume_fake_named_iterable expressions.tests_llm.FakeNamedIterableTests.test_range_lookup_accepts_fake_named_iterable expressions.tests_llm.FakeNamedIterableTests.test_range_lookup_accepts_fake_named_iterable_from_tuple expressions.tests_llm.FakeNamedIterableTests.test_range_lookup_with_F_expressions_in_fake_named_iterable expressions.tests_llm.FakeNamedIterableTests.test_range_lookup_with_value_objects_inside_fake_named_iterable expressions.tests_llm.__new__'] (expressions.tests_llm.FakeNamedIterableTests.['FakeNamed)
coverage json -o coverage.json
: '>>>>> End Test Output'
