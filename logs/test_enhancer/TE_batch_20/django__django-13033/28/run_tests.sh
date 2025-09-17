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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.OrderingFindOrderingNameRegressionTests.test_order_by_author_field_appends_related_default_when_lookup_is_relation ordering.test_models_llm.OrderingFindOrderingNameRegressionTests.test_order_by_author_id_and_author_relation_only_adds_expected_terms ordering.test_models_llm.OrderingFindOrderingNameRegressionTests.test_order_by_author_id_prefers_single_term_not_default ordering.test_models_llm.OrderingFindOrderingNameRegressionTests.test_order_by_author_id_with_other_ordering_parts_keeps_explicit_term_once ordering.test_models_llm.OrderingFindOrderingNameRegressionTests.test_order_by_author_pk_shortcut_keeps_single_term ordering.test_models_llm.OrderingFindOrderingNameRegressionTests.test_order_by_record_root_id_asc_has_single_ordering_term ordering.test_models_llm.OrderingFindOrderingNameRegressionTests.test_order_by_record_root_id_desc_has_single_ordering_term ordering.test_models_llm.OrderingFindOrderingNameRegressionTests.test_order_by_second_author_id_single_term ordering.test_models_llm.OrderingFindOrderingNameRegressionTests.test_order_by_second_author_relation_appends_related_default ordering.test_models_llm.OrderingFindOrderingNameRegressionTests.test_reference_order_by_article_author_id_single_term ordering.test_models_llm._count_ordering_columns_from_sql
coverage json -o coverage.json
: '>>>>> End Test Output'
