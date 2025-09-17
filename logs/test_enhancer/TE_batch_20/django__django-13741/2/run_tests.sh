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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldIntegrationTests.test_userchangeform_does_not_define_clean_password auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldMethodTests.test_bound_data_is_inherited_from_field auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldMethodTests.test_has_changed_is_inherited_from_field auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldMethodTests.test_no_bound_data_method_in_class auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldMethodTests.test_no_has_changed_method_in_class
coverage json -o coverage.json
: '>>>>> End Test Output'
