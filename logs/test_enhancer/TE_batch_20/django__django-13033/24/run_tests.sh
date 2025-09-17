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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.FindOrderingNameTests.setUpTestData ordering.test_models_llm.FindOrderingNameTests.test_order_by_F_expression_preserved ordering.test_models_llm.FindOrderingNameTests.test_order_by_descending_related_field ordering.test_models_llm.FindOrderingNameTests.test_order_by_random_and_mixed_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_related_attribute_does_not_prepend_model_default_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_related_field_includes_related_model_default_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_related_id_lookup_behaves_like_attribute_lookup ordering.test_models_llm.FindOrderingNameTests.test_order_by_second_author_name_uses_expression_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_self_referential_field_does_not_raise ordering.test_models_llm.FindOrderingNameTests.test_proxy_model_default_ordering_applied ordering.test_models_llm.FindOrderingNameTests.test_reference_model_ordering_uses_related_model_ordering ordering.test_models_llm._get_ordering_clause
coverage json -o coverage.json
: '>>>>> End Test Output'
