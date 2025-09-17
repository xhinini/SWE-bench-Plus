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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.FindOrderingNameTests._order_sql ordering.test_models_llm.FindOrderingNameTests.test_multiple_ordering_includes_only_requested_columns_for_id ordering.test_models_llm.FindOrderingNameTests.test_order_by_annotated_related_field_id ordering.test_models_llm.FindOrderingNameTests.test_order_by_mixed_relation_and_id ordering.test_models_llm.FindOrderingNameTests.test_order_by_negated_relation_appends_related_default_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_negated_relation_id_does_not_append_related_default_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_pk_and_relation_id ordering.test_models_llm.FindOrderingNameTests.test_order_by_relation_appends_related_default_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_relation_id_does_not_append_related_default_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_relation_then_field ordering.test_models_llm.FindOrderingNameTests.test_order_by_relation_with_lookup_then_id ordering.test_models_llm.[] (ordering.test_models_llm.Child) ordering.test_models_llm.[] (ordering.test_models_llm.Parent)
coverage json -o coverage.json
: '>>>>> End Test Output'
