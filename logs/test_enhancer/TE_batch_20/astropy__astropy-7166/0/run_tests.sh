#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8


: '>>>>> Start Test Output'
pytest -rA -vv -o console_output_style=classic --tb=no astropy/utils/tests/test_misc_llm.py

: '>>>>> End Test Output'
