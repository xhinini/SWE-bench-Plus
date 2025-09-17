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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldRegressionTests.setUpTestData auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldRegressionTests.test_no_bound_data_method_on_class auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldRegressionTests.test_no_bound_data_method_on_instance auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldRegressionTests.test_no_has_changed_method_on_class auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldRegressionTests.test_no_has_changed_method_on_instance auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldRegressionTests.test_password_not_in_changed_data_when_not_submitted auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldRegressionTests.test_userchange_form_ignores_posted_password_and_preserves_hashed_value auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldRegressionTests.test_userchangeform_no_clean_password_method_on_class auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldRegressionTests.test_userchangeform_no_clean_password_method_on_instance
coverage json -o coverage.json
: '>>>>> End Test Output'
