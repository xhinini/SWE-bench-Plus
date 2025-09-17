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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyRequest.__init__ staticfiles_tests.test_handlers_llm.test_asgi_handler_delegates_non_http staticfiles_tests.test_handlers_llm.test_asgi_handler_delegates_when_not_should_handle staticfiles_tests.test_handlers_llm.test_file_path_converts_percent_encoding staticfiles_tests.test_handlers_llm.test_get_base_url_uses_settings staticfiles_tests.test_handlers_llm.test_get_response_async_handles_http404_in_thread staticfiles_tests.test_handlers_llm.test_get_response_async_propagates_non_http404 staticfiles_tests.test_handlers_llm.test_get_response_async_runs_serve_in_thread staticfiles_tests.test_handlers_llm.test_serve_calls_staticfiles_view staticfiles_tests.test_handlers_llm.test_should_handle_false_when_base_url_has_netloc staticfiles_tests.test_handlers_llm.test_should_handle_path_equal_base_url
coverage json -o coverage.json
: '>>>>> End Test Output'
