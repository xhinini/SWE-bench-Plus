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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.tests_llm.ModelToDictFieldsParamRegressionTests.test_article_with_categories_empty_tuple_returns_empty model_forms.tests_llm.ModelToDictFieldsParamRegressionTests.test_multiple_models_consistently_handle_empty_fields
coverage json -o coverage.json
: '>>>>> End Test Output'
