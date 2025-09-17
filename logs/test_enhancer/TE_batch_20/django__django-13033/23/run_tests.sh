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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_id_does_not_contain_meta_pub_date_or_headline ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_id_is_quoted_or_prefixed_but_unique_token ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_id_only_once ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_id_single_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_includes_related_meta_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_editor_id_single_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_editor_includes_related_meta_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_minus_author_id_single_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_minus_editor_id_single_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_second_author_id_single_ordering ordering.test_models_llm._get_order_by_parts
coverage json -o coverage.json
: '>>>>> End Test Output'
