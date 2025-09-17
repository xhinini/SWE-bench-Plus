#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8


: '>>>>> Start Test Output'
pytest -rA astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs_llm.py

: '>>>>> End Test Output'
