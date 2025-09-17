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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.GetFieldDisplayOverrideRegressionTests.test_existing_attribute_none_not_overridden model_fields.tests_llm.GetFieldDisplayOverrideRegressionTests.test_inherited_display_not_overridden_on_subclass model_fields.tests_llm.GetFieldDisplayOverrideRegressionTests.test_iterator_choices_preserve_user_defined_display model_fields.tests_llm.GetFieldDisplayOverrideRegressionTests.test_lazy_choices_preserve_user_defined_display model_fields.tests_llm.GetFieldDisplayOverrideRegressionTests.test_non_callable_attribute_display_not_overridden model_fields.tests_llm.GetFieldDisplayOverrideRegressionTests.test_property_display_not_overridden model_fields.tests_llm.GetFieldDisplayOverrideRegressionTests.test_staticmethod_display_not_overridden
coverage json -o coverage.json
: '>>>>> End Test Output'
