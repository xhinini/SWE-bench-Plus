#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8


: '>>>>> Start Test Output'
pytest -rA astropy/nddata/mixins/tests/test_ndarithmetic.py

: '>>>>> End Test Output'
