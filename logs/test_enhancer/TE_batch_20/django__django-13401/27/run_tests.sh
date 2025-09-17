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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.DummyMeta.__init__ model_fields.tests_llm.DummyModel.__init__ model_fields.tests_llm.FieldOrderingAndHashTests.make_field model_fields.tests_llm.FieldOrderingAndHashTests.test_model_ordering_by_app_label_and_model_name_when_counters_equal model_fields.tests_llm.FieldOrderingAndHashTests.test_no_model_order_before_model_when_counters_equal model_fields.tests_llm.FieldOrderingAndHashTests.test_sort_many_equal_counters_mixed_models model_fields.tests_llm.FieldOrderingAndHashTests.test_sort_with_one_model_none_and_other_has_model_reflexivity model_fields.tests_llm.FieldOrderingAndHashTests.test_sorted_stable_with_mixed_fields
coverage json -o coverage.json
: '>>>>> End Test Output'
