#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python -m pip install pytest-cov .

: '>>>>> Start Test Output'
pytest -rA test_requests_llm.py

: '>>>>> End Test Output'
