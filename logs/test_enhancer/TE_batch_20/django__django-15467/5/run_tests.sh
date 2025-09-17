#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.RadioForeignKeyEmptyLabelTests.test_direct_kw_empty_label_empty_string admin_widgets.tests_llm.RadioForeignKeyEmptyLabelTests.test_direct_kw_empty_label_none admin_widgets.tests_llm.RadioForeignKeyEmptyLabelTests.test_direct_kw_empty_label_zero admin_widgets.tests_llm.RadioForeignKeyEmptyLabelTests.test_formfield_overrides_empty_label_empty_string admin_widgets.tests_llm.RadioForeignKeyEmptyLabelTests.test_formfield_overrides_empty_label_none admin_widgets.tests_llm.RadioForeignKeyEmptyLabelTests.test_formfield_overrides_empty_label_zero admin_widgets.tests_llm.RadioForeignKeyEmptyLabelTests.test_horizontal_radio_preserves_empty_string_override admin_widgets.tests_llm.RadioForeignKeyEmptyLabelTests.test_non_blank_field_ignores_override_in_formfield_overrides
coverage json -o coverage.json
: '>>>>> End Test Output'
