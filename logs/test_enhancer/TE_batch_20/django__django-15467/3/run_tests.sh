#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.AdminRadioFieldEmptyLabelTests.test_preserve_empty_string_override_horizontal admin_widgets.tests_llm.AdminRadioFieldEmptyLabelTests.test_preserve_empty_string_override_vertical admin_widgets.tests_llm.AdminRadioFieldEmptyLabelTests.test_preserve_none_override_horizontal admin_widgets.tests_llm.AdminRadioFieldEmptyLabelTests.test_preserve_none_override_vertical
coverage json -o coverage.json
: '>>>>> End Test Output'
