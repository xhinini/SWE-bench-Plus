#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.test__should_handle_false_when_netloc_present staticfiles_tests.test_handlers_llm.test__should_handle_true_for_exact_match staticfiles_tests.test_handlers_llm.test_file_path_converts_url_to_path_correctly staticfiles_tests.test_handlers_llm.test_get_base_url_checks_settings staticfiles_tests.test_handlers_llm.test_get_response_async_calls_sync_to_async_on_success staticfiles_tests.test_handlers_llm.test_get_response_async_propagates_non_http404_exceptions staticfiles_tests.test_handlers_llm.test_get_response_async_uses_sync_to_async_for_404 staticfiles_tests.test_handlers_llm.test_get_response_calls_serve_on_success staticfiles_tests.test_handlers_llm.test_get_response_sync_handles_http404
coverage json -o coverage.json
: '>>>>> End Test Output'
