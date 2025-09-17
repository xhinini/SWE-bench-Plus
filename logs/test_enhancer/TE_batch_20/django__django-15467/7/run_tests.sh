#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.RadioFieldsEmptyLabelTests.test_preserve_empty_string_from_formfield_overrides_horizontal admin_widgets.tests_llm.RadioFieldsEmptyLabelTests.test_preserve_empty_string_from_formfield_overrides_vertical admin_widgets.tests_llm.RadioFieldsEmptyLabelTests.test_preserve_empty_string_from_kwargs_vertical admin_widgets.tests_llm.RadioFieldsEmptyLabelTests.test_preserve_none_from_formfield_overrides_horizontal admin_widgets.tests_llm.RadioFieldsEmptyLabelTests.test_preserve_none_from_formfield_overrides_vertical admin_widgets.tests_llm.RadioFieldsEmptyLabelTests.test_preserve_none_from_kwargs_vertical
coverage json -o coverage.json
: '>>>>> End Test Output'
