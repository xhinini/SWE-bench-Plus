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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_grandparent_method_not_overwritten model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_multiple_parent_level_attributes_preserved model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_parent_class_method_not_overwritten model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_plain_attribute_on_parent_not_overwritten model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_property_on_parent_not_overwritten model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_staticmethod_on_parent_not_overwritten
coverage json -o coverage.json
: '>>>>> End Test Output'
