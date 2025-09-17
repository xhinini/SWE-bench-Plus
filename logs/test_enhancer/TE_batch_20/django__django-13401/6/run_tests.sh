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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.AdditionalFieldOrderingTests._make_equal_counters model_fields.tests_llm.AdditionalFieldOrderingTests.test_comparison_when_only_one_field_has_model_attribute_but_is_falsey model_fields.tests_llm.AdditionalFieldOrderingTests.test_comparison_with_unattached_and_attached_field_equals_logic model_fields.tests_llm.AdditionalFieldOrderingTests.test_list_sort_inplace_puts_no_model_first model_fields.tests_llm.AdditionalFieldOrderingTests.test_multiple_items_sort_with_mixed_model_attachment model_fields.tests_llm.AdditionalFieldOrderingTests.test_no_model_field_less_than_model_field_equal_creation_counter model_fields.tests_llm.AdditionalFieldOrderingTests.test_reverse_sort_places_model_fields_first model_fields.tests_llm.AdditionalFieldOrderingTests.test_sort_preserves_no_model_first_when_equal_creation_counter model_fields.tests_llm.AdditionalFieldOrderingTests.test_sort_stability_with_equal_creation_counters
coverage json -o coverage.json
: '>>>>> End Test Output'
