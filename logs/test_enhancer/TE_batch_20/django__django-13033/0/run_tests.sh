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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.FindOrderingNameTests._order_sqls ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_applies_author_default_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_editor_nested_variants ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_id_is_single_expression ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_vs_author_id_behavior_difference ordering.test_models_llm.FindOrderingNameTests.test_order_by_nested_relation_id_descending_does_not_apply_related_default_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_nested_relation_id_does_not_apply_related_default_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_nested_relation_relation_applies_related_default_ordering ordering.test_models_llm.FindOrderingNameTests.test_ordered_by_f_article_author_id_is_single_expression ordering.test_models_llm.FindOrderingNameTests.test_proxy_model_ordering_by_relation_includes_related_meta_ordering ordering.test_models_llm.FindOrderingNameTests.test_reference_order_by_article_editor_id_is_single_expression
coverage json -o coverage.json
: '>>>>> End Test Output'
