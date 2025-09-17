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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyHandler.__init__ staticfiles_tests.test_handlers_llm.test_get_response_async_does_not_call_response_for_exception_on_success staticfiles_tests.test_handlers_llm.test_get_response_async_handles_many_concurrent_calls_in_threadpool staticfiles_tests.test_handlers_llm.test_get_response_async_multiple_concurrent_calls_run_in_threadpool staticfiles_tests.test_handlers_llm.test_get_response_async_preserves_exception_type_for_non_http404 staticfiles_tests.test_handlers_llm.test_get_response_async_response_for_exception_called_with_correct_arguments staticfiles_tests.test_handlers_llm.test_get_response_async_returns_value_from_response_for_exception_on_404 staticfiles_tests.test_handlers_llm.test_get_response_async_returns_value_from_serve staticfiles_tests.test_handlers_llm.test_get_response_async_runs_response_for_exception_in_threadpool_on_404 staticfiles_tests.test_handlers_llm.test_get_response_async_runs_serve_in_threadpool staticfiles_tests.test_handlers_llm.test_get_response_async_with_bound_method_serve_runs_in_threadpool
coverage json -o coverage.json
: '>>>>> End Test Output'
