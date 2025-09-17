#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8

sed -i -e 's/ pytest / pytest --cov --cov-branch --cov-report json /g' tox.ini
: '>>>>> Start Test Output'
tox --current-env -epy39 -v -- tests/test_build_linkcheck_llm.py

: '>>>>> End Test Output'
