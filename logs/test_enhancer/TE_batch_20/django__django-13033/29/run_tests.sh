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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.DummyAlias.__init__ ordering.test_models_llm.DummyConnection.__init__ ordering.test_models_llm.DummyOps.quote_name ordering.test_models_llm.FindOrderingNameTests.test_attname_equals_last_piece_descending ordering.test_models_llm.FindOrderingNameTests.test_attname_equals_last_piece_multiple_targets ordering.test_models_llm.FindOrderingNameTests.test_attname_equals_last_piece_simple ordering.test_models_llm.FindOrderingNameTests.test_attname_equals_last_piece_with_complex_name ordering.test_models_llm.FindOrderingNameTests.test_attname_not_equal_uses_opts_ordering ordering.test_models_llm.FindOrderingNameTests.test_multiple_ordering_items_are_returned_when_applicable ordering.test_models_llm.FindOrderingNameTests.test_non_relation_field_uses_transform ordering.test_models_llm.FindOrderingNameTests.test_opts_ordering_already_orderby_used ordering.test_models_llm.FindOrderingNameTests.test_pk_name_skips_default_ordering ordering.test_models_llm.FindOrderingNameTests.test_single_piece_name_equals_attname ordering.test_models_llm.make_compiler_stub
coverage json -o coverage.json
: '>>>>> End Test Output'
