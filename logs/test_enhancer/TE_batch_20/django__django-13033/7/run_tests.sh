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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.CompilerFindOrderingTests.test_article_order_by_author_editor_id_nested ordering.test_models_llm.CompilerFindOrderingTests.test_article_order_by_author_id_single ordering.test_models_llm.CompilerFindOrderingTests.test_order_by_mixed_fields_some_id ordering.test_models_llm.CompilerFindOrderingTests.test_order_by_second_author_name_nonrelation_last_piece ordering.test_models_llm.CompilerFindOrderingTests.test_proxy_model_ordering_does_not_duplicate_id_ordering_for_id_lookup ordering.test_models_llm.CompilerFindOrderingTests.test_reference_order_by_article_author_and_editor_ids_multiple ordering.test_models_llm.CompilerFindOrderingTests.test_reference_order_by_article_author_appends_author_default_ordering ordering.test_models_llm.CompilerFindOrderingTests.test_reference_order_by_article_author_id_descending ordering.test_models_llm.CompilerFindOrderingTests.test_reference_order_by_article_author_id_single ordering.test_models_llm.CompilerFindOrderingTests.test_reference_order_by_article_author_pk_shortcut
coverage json -o coverage.json
: '>>>>> End Test Output'
