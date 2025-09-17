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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldOrderingHashTests.test_comparison_symmetry_for_model_and_no_model model_fields.tests_llm.FieldOrderingHashTests.test_model_vs_no_model_swapped_operands model_fields.tests_llm.FieldOrderingHashTests.test_models_order_by_model_name_case_difference model_fields.tests_llm.FieldOrderingHashTests.test_no_model_before_model_when_creation_counter_equal model_fields.tests_llm.FieldOrderingHashTests.test_sorted_mixture_of_no_model_and_models model_fields.tests_llm.make_dummy_model
coverage json -o coverage.json
: '>>>>> End Test Output'
