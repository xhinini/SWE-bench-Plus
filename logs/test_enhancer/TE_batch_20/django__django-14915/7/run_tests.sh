#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_modelchoicefield_llm.ModelChoiceIteratorValueHashTests.setUpTestData model_forms.test_modelchoicefield_llm.ModelChoiceIteratorValueHashTests.test_equality_is_true_for_right_hand_modelchoicevalue_compare
coverage json -o coverage.json
: '>>>>> End Test Output'
