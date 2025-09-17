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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.FindOrderingNameTests.get_order_clause ordering.test_models_llm.FindOrderingNameTests.test_no_infinite_loop_raised_for_nested_self_fk_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_fieldname_creates_single_ordering_term ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_id_creates_single_ordering_term ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_id_descending_single_term ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_id_with_F_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_author_pk_creates_single_ordering_term ordering.test_models_llm.FindOrderingNameTests.test_order_by_related_proxy_model_field_single_term ordering.test_models_llm.FindOrderingNameTests.test_order_by_second_author_fieldname_single_term ordering.test_models_llm.FindOrderingNameTests.test_order_by_self_fk_editor_editor_id_descending ordering.test_models_llm.FindOrderingNameTests.test_order_by_self_fk_editor_editor_id_single_term
coverage json -o coverage.json
: '>>>>> End Test Output'
