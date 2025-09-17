#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
pytest -rA sklearn/linear_model/tests/test_logistic_llm.py
coverage json -o coverage.json
: '>>>>> End Test Output'
