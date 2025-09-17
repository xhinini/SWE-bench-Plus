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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.PreserveDisplayMethodTests.test_preserve_inherited_display_attribute_none model_fields.tests_llm.PreserveDisplayMethodTests.test_preserve_inherited_display_from_grandparent model_fields.tests_llm.PreserveDisplayMethodTests.test_preserve_inherited_display_from_mixin model_fields.tests_llm.PreserveDisplayMethodTests.test_preserve_inherited_display_method_assigned_function model_fields.tests_llm.PreserveDisplayMethodTests.test_preserve_inherited_display_method_classmethod model_fields.tests_llm.PreserveDisplayMethodTests.test_preserve_inherited_display_method_regular_method model_fields.tests_llm.PreserveDisplayMethodTests.test_preserve_parent_method_for_underscored_field model_fields.tests_llm.PreserveDisplayMethodTests.test_preserve_with_generator_choices model_fields.tests_llm.PreserveDisplayMethodTests.test_preserve_with_iterator_choices
coverage json -o coverage.json
: '>>>>> End Test Output'
