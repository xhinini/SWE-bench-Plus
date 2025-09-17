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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldRegressionTests.test_bound_data_not_overridden_on_field_class auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldRegressionTests.test_custom_modelform_with_readonly_password_field_excludes_field_from_cleaned_data auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldRegressionTests.test_readonly_field_excluded_from_cleaned_data_on_plain_form auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldRegressionTests.test_readonly_field_excluded_from_cleaned_data_when_missing_initial auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldRegressionTests.test_readonly_field_not_in_cleaned_data_when_posted_empty_string auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldRegressionTests.test_readonly_field_not_in_cleaned_data_when_unusable_password auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldRegressionTests.test_userchangeform_posting_password_is_not_in_cleaned_data
coverage json -o coverage.json
: '>>>>> End Test Output'
