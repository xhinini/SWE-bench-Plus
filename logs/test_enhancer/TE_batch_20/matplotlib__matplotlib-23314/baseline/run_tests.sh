#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8


: '>>>>> Start Test Output'
pytest -rA lib/matplotlib/tests/test_axes.py lib/mpl_toolkits/tests/test_mplot3d.py

: '>>>>> End Test Output'
