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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.DummyField.__init__ ordering.test_models_llm.DummyOpts.__init__ ordering.test_models_llm.FakeQuery.__init__ ordering.test_models_llm.FindOrderingNameTests.make_compiler_with_setup ordering.test_models_llm.FindOrderingNameTests.test_default_ordering_appended_when_last_piece_is_not_attname ordering.test_models_llm.FindOrderingNameTests.test_infinite_loop_detection_raises_FieldError ordering.test_models_llm.FindOrderingNameTests.test_multiple_ordering_items_appended_when_applicable ordering.test_models_llm.FindOrderingNameTests.test_nested_lookup_multiple_parts_last_piece_attname_no_append ordering.test_models_llm.FindOrderingNameTests.test_no_default_ordering_appended_when_last_piece_is_attname_simple ordering.test_models_llm.FindOrderingNameTests.test_no_default_ordering_appended_with_descending_prefix ordering.test_models_llm.FindOrderingNameTests.test_no_default_ordering_with_multiple_targets ordering.test_models_llm.FindOrderingNameTests.test_non_relation_field_returns_direct_ordering ordering.test_models_llm.FindOrderingNameTests.test_pk_shortcut_not_treated_as_relation
coverage json -o coverage.json
: '>>>>> End Test Output'
