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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldModelPresenceOrderingTests._set_and_restore_counters model_fields.tests_llm.FieldModelPresenceOrderingTests.test_bound_field_greater_than_unbound_field_equal_creation_counter model_fields.tests_llm.FieldModelPresenceOrderingTests.test_comparison_commutativity_between_bound_and_unbound model_fields.tests_llm.FieldModelPresenceOrderingTests.test_multiple_bound_and_unbound_stable_grouping model_fields.tests_llm.FieldModelPresenceOrderingTests.test_sort_bound_then_unbound_multiple_times
coverage json -o coverage.json
: '>>>>> End Test Output'
