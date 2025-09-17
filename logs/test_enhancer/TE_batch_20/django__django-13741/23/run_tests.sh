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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldAPIRegressionTests.test_callable_not_exposed_on_class_for_bound_data auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldAPIRegressionTests.test_callable_not_exposed_on_instance_for_bound_data auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldAPIRegressionTests.test_class_dir_does_not_contain_bound_data auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldAPIRegressionTests.test_class_has_no_bound_data_attribute_via_hasattr auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldAPIRegressionTests.test_getattr_on_class_returns_default_none_for_bound_data auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldAPIRegressionTests.test_getattr_on_instance_returns_default_none_for_bound_data auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldAPIRegressionTests.test_instance_dir_does_not_contain_bound_data auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldAPIRegressionTests.test_instance_has_no_bound_data_attribute_via_hasattr auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldAPIRegressionTests.test_strict_attribute_check_on_class
coverage json -o coverage.json
: '>>>>> End Test Output'
