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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.CompilerOrderingRegressionTests._get_ordering_list ordering.test_models_llm.CompilerOrderingRegressionTests.setUpTestData ordering.test_models_llm.CompilerOrderingRegressionTests.test_multi_level_nested_relation_appends_default_ordering ordering.test_models_llm.CompilerOrderingRegressionTests.test_nested_related_field_appends_default_ordering_author_editor ordering.test_models_llm.CompilerOrderingRegressionTests.test_reference_through_proxy_model_relation_appends_defaults ordering.test_models_llm.CompilerOrderingRegressionTests.test_single_level_relation_author_appends_default
coverage json -o coverage.json
: '>>>>> End Test Output'
