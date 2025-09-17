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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyHandler.__init__ staticfiles_tests.test_handlers_llm.DummyRequest.__init__ staticfiles_tests.test_handlers_llm.make_spy_sync_to_async staticfiles_tests.test_handlers_llm.test__should_handle_accepts_paths_equal_to_base_path staticfiles_tests.test_handlers_llm.test__should_handle_respects_host_in_base_url staticfiles_tests.test_handlers_llm.test_asgi_handler_pass_through_for_non_matching_scope staticfiles_tests.test_handlers_llm.test_file_path_converts_url_to_path staticfiles_tests.test_handlers_llm.test_get_response_async_calls_response_for_exception_on_http404 staticfiles_tests.test_handlers_llm.test_get_response_async_propagates_non_http404_exception staticfiles_tests.test_handlers_llm.test_get_response_async_returns_value_from_serve_bound_method staticfiles_tests.test_handlers_llm.test_get_response_async_uses_sync_to_async_for_response_for_exception staticfiles_tests.test_handlers_llm.test_get_response_async_uses_sync_to_async_on_success
coverage json -o coverage.json
: '>>>>> End Test Output'
