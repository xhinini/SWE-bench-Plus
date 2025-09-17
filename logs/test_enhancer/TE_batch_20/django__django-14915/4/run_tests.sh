#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_modelchoicefield_llm.ModelChoiceIteratorValueHashTests.setUpTestData model_forms.test_modelchoicefield_llm.ModelChoiceIteratorValueHashTests.test_checkbox_widget_create_option_uses_wrapper_and_keys_work
coverage json -o coverage.json
: '>>>>> End Test Output'
