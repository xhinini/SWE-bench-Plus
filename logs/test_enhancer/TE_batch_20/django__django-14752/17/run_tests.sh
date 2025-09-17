#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_views.test_autocomplete_view_llm.test_serialize_result_called_in_ordering admin_views.test_autocomplete_view_llm.test_serialize_result_override_custom_to_field admin_views.test_autocomplete_view_llm.test_serialize_result_override_distinct admin_views.test_autocomplete_view_llm.test_serialize_result_override_fk_pk admin_views.test_autocomplete_view_llm.test_serialize_result_override_mti admin_views.test_autocomplete_view_llm.test_serialize_result_override_pagination admin_views.test_autocomplete_view_llm.test_serialize_result_preserves_pagination_flag_with_override admin_views.test_autocomplete_view_llm.test_serialize_result_receives_attname_and_id_is_correct admin_views.test_autocomplete_view_llm.test_serialize_result_text_is_str
coverage json -o coverage.json
: '>>>>> End Test Output'
