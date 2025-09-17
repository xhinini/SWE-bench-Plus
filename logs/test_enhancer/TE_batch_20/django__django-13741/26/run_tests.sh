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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldUnitTests.test_bound_data_does_not_force_initial_value auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldUnitTests.test_bound_data_returns_empty_string_when_submitted_is_empty auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldUnitTests.test_bound_data_returns_none_when_submitted_is_none auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldUnitTests.test_bound_data_returns_submitted_value auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldUnitTests.test_class_does_not_override_bound_data auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldUnitTests.test_class_does_not_override_has_changed auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldUnitTests.test_has_changed_true_for_different_values auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldUnitTests.test_has_changed_true_when_initial_none_and_data_present
coverage json -o coverage.json
: '>>>>> End Test Output'
