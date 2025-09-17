#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_views.test_autocomplete_view_llm.AutocompleteSerializeRegressionTests.test_customize_output_keys_via_serialize_result_reflected_in_json admin_views.test_autocomplete_view_llm.AutocompleteSerializeRegressionTests.test_get_docstring_mentions_serialize_result admin_views.test_autocomplete_view_llm.AutocompleteSerializeRegressionTests.test_get_uses_instance_serialize_result_when_building_json admin_views.test_autocomplete_view_llm.AutocompleteSerializeRegressionTests.test_multiple_objects_serialized_in_order admin_views.test_autocomplete_view_llm.AutocompleteSerializeRegressionTests.test_serialize_result_defined_after_get_in_source admin_views.test_autocomplete_view_llm.MockObj.__init__ admin_views.test_autocomplete_view_llm.MockObj.__str__
coverage json -o coverage.json
: '>>>>> End Test Output'
