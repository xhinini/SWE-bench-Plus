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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.OrderingAttnameTests._get_order_by ordering.test_models_llm.OrderingAttnameTests.test_chain_editor_editor_id_single ordering.test_models_llm.OrderingAttnameTests.test_editor_editor_id_does_not_infinite_loop ordering.test_models_llm.OrderingAttnameTests.test_editor_editor_id_single ordering.test_models_llm.OrderingAttnameTests.test_editor_id_top_level_single ordering.test_models_llm.OrderingAttnameTests.test_editor_vs_editor_id ordering.test_models_llm.OrderingAttnameTests.test_mixed_editor_and_attname ordering.test_models_llm.OrderingAttnameTests.test_multiple_fields_with_editor_editor_id ordering.test_models_llm.OrderingAttnameTests.test_multiple_repeated_attname_orderings ordering.test_models_llm.OrderingAttnameTests.test_negative_editor_editor_id_single ordering.test_models_llm.OrderingAttnameTests.test_reverse_chain_editor_editor_id_single
coverage json -o coverage.json
: '>>>>> End Test Output'
