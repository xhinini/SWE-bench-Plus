#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8


: '>>>>> Start Test Output'
pytest -rA lib/mpl_toolkits/axes_grid1/tests/test_axes_grid1_llm.py

: '>>>>> End Test Output'
