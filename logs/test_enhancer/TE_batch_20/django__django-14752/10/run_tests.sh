#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_views.test_autocomplete_view_llm.test_serialize_result_adds_extra_field admin_views.test_autocomplete_view_llm.test_serialize_result_applies_on_second_page admin_views.test_autocomplete_view_llm.test_serialize_result_can_change_id_format admin_views.test_autocomplete_view_llm.test_serialize_result_can_use_admin_site_attribute admin_views.test_autocomplete_view_llm.test_serialize_result_handles_unicode_text admin_views.test_autocomplete_view_llm.test_serialize_result_respects_distinct_queries admin_views.test_autocomplete_view_llm.test_serialize_result_safe_fallback_when_str_is_not_used admin_views.test_autocomplete_view_llm.test_serialize_result_with_custom_to_field_uuid admin_views.test_autocomplete_view_llm.test_serialize_result_with_fk_pk_to_field
coverage json -o coverage.json
: '>>>>> End Test Output'
