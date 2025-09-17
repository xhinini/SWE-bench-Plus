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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.FindOrderingNameTests._get_ordering_sqls ordering.test_models_llm.FindOrderingNameTests.setUp ordering.test_models_llm.FindOrderingNameTests.test_order_by_annotation_reference_resolution ordering.test_models_llm.FindOrderingNameTests.test_order_by_combined_ordering_items_do_not_duplicate_terms ordering.test_models_llm.FindOrderingNameTests.test_order_by_f_expression_nulls_and_direction ordering.test_models_llm.FindOrderingNameTests.test_order_by_fk_attname_descending_produces_desc ordering.test_models_llm.FindOrderingNameTests.test_order_by_fk_attname_produces_single_ordering_term ordering.test_models_llm.FindOrderingNameTests.test_order_by_multiple_related_fields ordering.test_models_llm.FindOrderingNameTests.test_order_by_proxy_model_inherits_and_resolves_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_relation_name_uses_related_model_default_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_relation_pk_shortcut_appends_related_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_relation_with_f_expression_handling
coverage json -o coverage.json
: '>>>>> End Test Output'
