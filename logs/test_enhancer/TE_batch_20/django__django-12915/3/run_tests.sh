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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyRequest.__init__ staticfiles_tests.test_handlers_llm.test_asgi_handler_get_response_async_runs_response_for_exception_in_thread_on_404 staticfiles_tests.test_handlers_llm.test_asgi_handler_get_response_async_runs_serve_in_thread_on_success staticfiles_tests.test_handlers_llm.test_file_path_decodes_percent_encoding staticfiles_tests.test_handlers_llm.test_file_path_returns_empty_for_exact_base_url staticfiles_tests.test_handlers_llm.test_load_middleware_has_no_extra_parameters staticfiles_tests.test_handlers_llm.test_mixin_get_response_async_runs_response_for_exception_in_thread_on_404 staticfiles_tests.test_handlers_llm.test_mixin_get_response_async_runs_serve_in_thread_on_success staticfiles_tests.test_handlers_llm.test_should_handle_returns_false_if_netloc_present staticfiles_tests.test_handlers_llm.test_should_handle_returns_true_when_path_under_base_and_no_netloc
coverage json -o coverage.json
: '>>>>> End Test Output'
