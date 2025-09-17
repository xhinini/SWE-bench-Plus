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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.test_asgi_handler_get_response_async_handles_404_in_threadpool staticfiles_tests.test_handlers_llm.test_asgi_handler_get_response_async_runs_serve_in_threadpool staticfiles_tests.test_handlers_llm.test_asgi_handler_get_response_runs_serve_on_main_thread_sync staticfiles_tests.test_handlers_llm.test_concurrent_get_response_async_does_not_block_event_loop staticfiles_tests.test_handlers_llm.test_exception_response_for_exception_threading_multiple_calls staticfiles_tests.test_handlers_llm.test_get_response_runs_serve_on_main_thread_sync staticfiles_tests.test_handlers_llm.test_mixin_get_response_async_runs_serve_in_threadpool staticfiles_tests.test_handlers_llm.test_mixin_get_response_async_uses_thread_for_response_for_exception
coverage json -o coverage.json
: '>>>>> End Test Output'
