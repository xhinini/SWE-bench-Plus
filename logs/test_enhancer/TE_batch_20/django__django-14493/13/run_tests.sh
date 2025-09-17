#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_storage_llm.PostProcessMaxPassesZeroTests._hash staticfiles_tests.test_storage_llm.PostProcessMaxPassesZeroTests._make_src_file staticfiles_tests.test_storage_llm.PostProcessMaxPassesZeroTests._run_post_process staticfiles_tests.test_storage_llm.PostProcessMaxPassesZeroTests.setUp staticfiles_tests.test_storage_llm.PostProcessMaxPassesZeroTests.tearDown staticfiles_tests.test_storage_llm.PostProcessMaxPassesZeroTests.test_css_name_with_fragment_in_mapping_key staticfiles_tests.test_storage_llm.PostProcessMaxPassesZeroTests.test_css_name_with_querystring_in_mapping_key staticfiles_tests.test_storage_llm.PostProcessMaxPassesZeroTests.test_simple_css_and_image_processed_without_error
coverage json -o coverage.json
: '>>>>> End Test Output'
