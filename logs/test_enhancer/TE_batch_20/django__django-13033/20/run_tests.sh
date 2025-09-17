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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.FindOrderingNameTests.test_multiple_ordering_mix_id_and_relation ordering.test_models_llm.FindOrderingNameTests.test_order_by_relation_appends_related_default_ordering ordering.test_models_llm.FindOrderingNameTests.test_order_by_second_author_id_no_related_defaults ordering.test_models_llm._get_sql ordering.test_models_llm._has_token
coverage json -o coverage.json
: '>>>>> End Test Output'
