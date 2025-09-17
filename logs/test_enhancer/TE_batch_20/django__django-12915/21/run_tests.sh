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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyHandler.__init__ staticfiles_tests.test_handlers_llm.run_async staticfiles_tests.test_handlers_llm.test_get_response_async_interleaved_calls_to_serve_and_exception staticfiles_tests.test_handlers_llm.test_get_response_async_runs_blocking_serve_in_threadpool staticfiles_tests.test_handlers_llm.test_get_response_async_runs_response_for_exception_in_threadpool staticfiles_tests.test_handlers_llm.test_get_response_async_runs_response_for_exception_in_threadpool_multiple_calls staticfiles_tests.test_handlers_llm.test_get_response_async_runs_serve_in_threadpool_on_multiple_calls staticfiles_tests.test_handlers_llm.test_get_response_async_runs_serve_in_threadpool_simple staticfiles_tests.test_handlers_llm.test_get_response_async_uses_threadpool_for_concurrent_requests staticfiles_tests.test_handlers_llm.test_get_response_async_with_long_running_block staticfiles_tests.test_handlers_llm.test_get_response_async_with_quick_return_and_exception
coverage json -o coverage.json
: '>>>>> End Test Output'
