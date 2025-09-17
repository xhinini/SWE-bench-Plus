#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 basic.tests_llm.CustomQuerySet._exposed basic.tests_llm.CustomQuerySet._private basic.tests_llm.CustomQuerySet.annotated basic.tests_llm.CustomQuerySet.bar basic.tests_llm.CustomQuerySet.foo basic.tests_llm.CustomQuerySet.queryset_only_method
coverage json -o coverage.json
: '>>>>> End Test Output'
