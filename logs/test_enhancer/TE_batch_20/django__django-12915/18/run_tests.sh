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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyMixin.__init__ staticfiles_tests.test_handlers_llm.test_asgi_handler_hands_off_non_http_scope staticfiles_tests.test_handlers_llm.test_asgi_handler_uses_super_call_for_http_and_matching_path staticfiles_tests.test_handlers_llm.test_file_path_converts_url_to_relative_path staticfiles_tests.test_handlers_llm.test_get_response_async_calls_sync_to_async_on_success staticfiles_tests.test_handlers_llm.test_get_response_async_handles_Http404_and_uses_response_for_exception_async staticfiles_tests.test_handlers_llm.test_get_response_handles_Http404_and_uses_response_for_exception staticfiles_tests.test_handlers_llm.test_load_middleware_signature_has_not_changed staticfiles_tests.test_handlers_llm.test_serve_delegates_to_serve_with_insecure_flag staticfiles_tests.test_handlers_llm.test_should_handle_true_and_false staticfiles_tests.test_handlers_llm.test_should_handle_with_host_in_base_url
coverage json -o coverage.json
: '>>>>> End Test Output'
