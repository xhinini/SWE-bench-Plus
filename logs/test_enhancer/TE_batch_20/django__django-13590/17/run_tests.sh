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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 expressions.tests_llm.ResolveLookupValueNamedLikeTests.setUp expressions.tests_llm.ResolveLookupValueNamedLikeTests.test_resolve_fake_named_direct expressions.tests_llm.ResolveLookupValueNamedLikeTests.test_resolve_fake_named_in_tuple_of_tuples expressions.tests_llm.ResolveLookupValueNamedLikeTests.test_resolve_fake_named_inside_list expressions.tests_llm.ResolveLookupValueNamedLikeTests.test_resolve_fake_named_inside_tuple expressions.tests_llm.ResolveLookupValueNamedLikeTests.test_resolve_fake_named_nested_in_list_and_tuple expressions.tests_llm.ResolveLookupValueNamedLikeTests.test_resolve_fake_named_with_F_expression_inside expressions.tests_llm.ResolveLookupValueNamedLikeTests.test_resolve_fake_named_with_Value_elements expressions.tests_llm.ResolveLookupValueNamedLikeTests.test_resolve_list_of_fake_named expressions.tests_llm.ResolveLookupValueNamedLikeTests.test_resolve_mixed_list_with_int_and_fake_named expressions.tests_llm.__repr__'] (expressions.tests_llm.ResolveLookupValueNamedLikeTests.['FakeNamed._make', 'FakeNamed.__new__', 'FakeNamed)
coverage json -o coverage.json
: '>>>>> End Test Output'
