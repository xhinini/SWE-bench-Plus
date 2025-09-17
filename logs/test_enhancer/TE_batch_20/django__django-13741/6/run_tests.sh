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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldEnabledTests.test_bound_data_returns_data_when_enabled auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldEnabledTests.test_bound_data_returns_none_when_enabled_and_data_none auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldEnabledTests.test_field_has_changed_reflects_data_when_enabled auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldEnabledTests.test_form_accepts_posted_password_when_field_enabled auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldEnabledTests.test_form_binding_unicode_values_when_enabled auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldEnabledTests.test_form_enabled_with_empty_string_uses_posted_empty_string auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldEnabledTests.test_userchangeform_allows_password_override_when_enabled
coverage json -o coverage.json
: '>>>>> End Test Output'
