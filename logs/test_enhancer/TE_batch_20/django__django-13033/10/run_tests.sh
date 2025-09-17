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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.CompilerOrderingTests._order_by_columns_count ordering.test_models_llm.CompilerOrderingTests.test_article_order_by_author_id_single_term ordering.test_models_llm.CompilerOrderingTests.test_article_order_by_minus_author_id_single_term_and_desc ordering.test_models_llm.CompilerOrderingTests.test_article_order_by_second_author_id_desc_single_term ordering.test_models_llm.CompilerOrderingTests.test_article_order_by_second_author_id_single_term ordering.test_models_llm.CompilerOrderingTests.test_reference_order_by_article_author_id_has_single_ordering_term ordering.test_models_llm.CompilerOrderingTests.test_reference_order_by_article_author_id_with_additional_field_preserves_expected_terms ordering.test_models_llm.CompilerOrderingTests.test_reference_order_by_article_author_pk_has_single_ordering_term ordering.test_models_llm.CompilerOrderingTests.test_reference_order_by_minus_article_author_id_has_single_ordering_term_and_desc ordering.test_models_llm.CompilerOrderingTests.test_reference_order_by_minus_article_author_id_with_additional_field_preserves_expected_terms ordering.test_models_llm.CompilerOrderingTests.test_reference_order_by_minus_article_author_pk_has_single_ordering_term_and_desc
coverage json -o coverage.json
: '>>>>> End Test Output'
