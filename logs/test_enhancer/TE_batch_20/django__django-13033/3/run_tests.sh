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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.FindOrderingNameTests._sql_for_qs ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_double_underscore_id ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_id_no_related_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_includes_related_default_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_pk_shortcut ordering.test_models_llm.FindOrderingNameTests.test_order_by_expression_then_fk_column ordering.test_models_llm.FindOrderingNameTests.test_order_by_negative_author_id_no_related_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_second_author_id_no_extra_ordering ordering.test_models_llm.FindOrderingNameTests.test_ordered_by_author_article_proxy_default_behavior ordering.test_models_llm.FindOrderingNameTests.test_ordered_by_f_article_author_id_not_add_default ordering.test_models_llm.FindOrderingNameTests.test_reference_default_ordering_by_article
coverage json -o coverage.json
: '>>>>> End Test Output'
