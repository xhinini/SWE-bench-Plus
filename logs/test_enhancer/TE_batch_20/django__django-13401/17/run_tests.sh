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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldOrderingHashingTests.mk_field model_fields.tests_llm.FieldOrderingHashingTests.test_lt_fields_with_models_compare_by_meta_tuple_when_same_counter model_fields.tests_llm.FieldOrderingHashingTests.test_lt_symmetry_between_bound_and_unbound model_fields.tests_llm.FieldOrderingHashingTests.test_order_no_model_fields_first_when_equal_creation_counter model_fields.tests_llm.FieldOrderingHashingTests.test_sort_mixed_same_counter_order_models_by_app_label_and_model_name model_fields.tests_llm.FieldOrderingHashingTests.test_sort_multiple_models_and_unbound_consistent
coverage json -o coverage.json
: '>>>>> End Test Output'
