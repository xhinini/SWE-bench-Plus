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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.AdminPasswordChangeFormChangedDataTests.test_changed_data_returns_empty_when_a_password_field_missing auth_tests.test_forms_llm.AdminPasswordChangeFormChangedDataTests.test_changed_data_returns_password_when_all_fields_present auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldExtraTests.test_disabled_by_default auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldExtraTests.test_has_changed_none_vs_empty_returns_false auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldExtraTests.test_has_changed_with_different_values_returns_false auth_tests.test_forms_llm.ReadOnlyPasswordInFormTests.test_bound_password_field_value_equals_initial_even_if_posted auth_tests.test_forms_llm.ReadOnlyPasswordInFormTests.test_changed_data_does_not_include_password_when_posting_new_value auth_tests.test_forms_llm.ReadOnlyPasswordInFormTests.test_preserve_empty_initial_password_when_submitted_value_differs auth_tests.test_forms_llm.ReadOnlyPasswordInFormTests.test_preserve_initial_hashed_password_when_submitted_value_differs
coverage json -o coverage.json
: '>>>>> End Test Output'
