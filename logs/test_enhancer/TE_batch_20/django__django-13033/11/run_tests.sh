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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.DummyCompiler.__init__ ordering.test_models_llm.DummyCompiler._setup_joins ordering.test_models_llm.FindOrderingNameTests._run_case ordering.test_models_llm.FindOrderingNameTests.test_another_relation_id_uses_model_ordering ordering.test_models_llm.FindOrderingNameTests.test_deep_relation_id_uses_model_ordering ordering.test_models_llm.FindOrderingNameTests.test_id_suffix_with_long_field_name_uses_model_ordering ordering.test_models_llm.FindOrderingNameTests.test_id_suffix_with_numbers_uses_model_ordering ordering.test_models_llm.FindOrderingNameTests.test_long_chain_id_uses_model_ordering ordering.test_models_llm.FindOrderingNameTests.test_minus_record_root_id_uses_model_ordering ordering.test_models_llm.FindOrderingNameTests.test_multiple_targets_but_model_ordering_preferred ordering.test_models_llm.FindOrderingNameTests.test_ordering_when_attname_similar_but_not_equal_uses_model_ordering ordering.test_models_llm.FindOrderingNameTests.test_record_root_id_uses_model_ordering ordering.test_models_llm.FindOrderingNameTests.test_tricky_suffix_id_uses_model_ordering
coverage json -o coverage.json
: '>>>>> End Test Output'
