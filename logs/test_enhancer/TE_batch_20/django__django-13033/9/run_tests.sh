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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.CompilerOrderingTests._order_by_count ordering.test_models_llm.CompilerOrderingTests.test_article_order_by_author_name_includes_author_meta_ordering ordering.test_models_llm.CompilerOrderingTests.test_article_order_by_negative_author_name_includes_author_meta_ordering ordering.test_models_llm.CompilerOrderingTests.test_orderedbyauthorarticle_order_by_author_name_includes_related_meta_ordering ordering.test_models_llm.CompilerOrderingTests.test_orderedbyfarticle_order_by_author_name_includes_related_meta_ordering ordering.test_models_llm.CompilerOrderingTests.test_reference_order_by_article_author__name_includes_author_meta_ordering ordering.test_models_llm.CompilerOrderingTests.test_reference_order_by_article_author_id_includes_author_meta_ordering ordering.test_models_llm.CompilerOrderingTests.test_reference_order_by_article_author_includes_author_meta_ordering ordering.test_models_llm.CompilerOrderingTests.test_reference_order_by_article_second_author_id_includes_author_meta_ordering ordering.test_models_llm.CompilerOrderingTests.test_reference_order_by_neg_article_author_id_includes_author_meta_ordering
coverage json -o coverage.json
: '>>>>> End Test Output'
