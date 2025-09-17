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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.CompilerOrderingTests._get_order_by_clause ordering.test_models_llm.CompilerOrderingTests.setUp ordering.test_models_llm.CompilerOrderingTests.test_descending_order_by_relation_expands ordering.test_models_llm.CompilerOrderingTests.test_mixed_ordering_with_relation_and_field ordering.test_models_llm.CompilerOrderingTests.test_multiple_ordering_items_deduplicated ordering.test_models_llm.CompilerOrderingTests.test_order_by_annotation_reference_is_handled ordering.test_models_llm.CompilerOrderingTests.test_order_by_callable_ordering_via_orderby_f ordering.test_models_llm.CompilerOrderingTests.test_order_by_f_expression_respects_default_ordering ordering.test_models_llm.CompilerOrderingTests.test_order_by_field_on_related_model_attname_does_not_expand ordering.test_models_llm.CompilerOrderingTests.test_order_by_field_on_related_model_expands_to_related_default_ordering ordering.test_models_llm.CompilerOrderingTests.test_order_by_relation_expands_to_related_default_ordering ordering.test_models_llm.CompilerOrderingTests.test_order_by_relation_id_does_not_expand_to_related_default_ordering
coverage json -o coverage.json
: '>>>>> End Test Output'
