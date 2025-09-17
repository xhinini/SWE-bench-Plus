#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 template_tests.filter_tests.test_join_llm.JoinAdditionalTests.test_escape_joiner_and_items_autoescape_on template_tests.filter_tests.test_join_llm.JoinAdditionalTests.test_generator_input_autoescape_on template_tests.filter_tests.test_join_llm.JoinAdditionalTests.test_integer_elements template_tests.filter_tests.test_join_llm.JoinAdditionalTests.test_mark_safe_elements_preserved template_tests.filter_tests.test_join_llm.JoinAdditionalTests.test_mark_safe_joiner_autoescape_on template_tests.filter_tests.test_join_llm.JoinAdditionalTests.test_no_escape_joiner_autoescape_off template_tests.filter_tests.test_join_llm.JoinAdditionalTests.test_noniterable_value_returns_input_autoescape_off template_tests.filter_tests.test_join_llm.JoinAdditionalTests.test_noniterable_value_returns_input_autoescape_on template_tests.filter_tests.test_join_llm.JoinAdditionalTests.test_unicode_and_ampersand template_tests.filter_tests.test_join_llm.JoinAdditionalTests.test_variable_joiner_with_entity_in_context
coverage json -o coverage.json
: '>>>>> End Test Output'
