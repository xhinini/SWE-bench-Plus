#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8


: '>>>>> Start Test Output'
pytest -rA astropy/io/fits/tests/test_connect_llm.py

: '>>>>> End Test Output'
