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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.ReadOnlyPasswordFieldAndUserChangeFormRegressionTests.test_readonlyfield_dir_has_no_bound_data auth_tests.test_forms_llm.ReadOnlyPasswordFieldAndUserChangeFormRegressionTests.test_readonlyfield_has_no_bound_data_method auth_tests.test_forms_llm.ReadOnlyPasswordFieldAndUserChangeFormRegressionTests.test_readonlyfield_has_no_has_changed_method auth_tests.test_forms_llm.ReadOnlyPasswordFieldAndUserChangeFormRegressionTests.test_readonlyfield_instance_has_no_has_changed auth_tests.test_forms_llm.ReadOnlyPasswordFieldAndUserChangeFormRegressionTests.test_subclass_does_not_inherit_clean_password auth_tests.test_forms_llm.ReadOnlyPasswordFieldAndUserChangeFormRegressionTests.test_userchangeform_has_no_clean_password_method auth_tests.test_forms_llm.ReadOnlyPasswordFieldAndUserChangeFormRegressionTests.test_userchangeform_instance_has_no_clean_password_method
coverage json -o coverage.json
: '>>>>> End Test Output'
