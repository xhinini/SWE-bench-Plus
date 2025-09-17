#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 basic.tests_llm.CustomQuerySet._private_allowed basic.tests_llm.CustomQuerySet._private_default basic.tests_llm.CustomQuerySet.another basic.tests_llm.CustomQuerySet.custom basic.tests_llm.CustomQuerySet.skip_me basic.tests_llm.ExistingManager.filter basic.tests_llm.TestsForManagerWrapping.setUp
coverage json -o coverage.json
: '>>>>> End Test Output'
