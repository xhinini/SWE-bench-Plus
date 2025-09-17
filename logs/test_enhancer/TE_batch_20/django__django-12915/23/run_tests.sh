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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm._assert_non_blocking staticfiles_tests.test_handlers_llm._assert_non_blocking_exception_path staticfiles_tests.test_handlers_llm.import_handlers staticfiles_tests.test_handlers_llm.make_handler_module_instance staticfiles_tests.test_handlers_llm.test_get_response_async_exception_path_non_blocking_bound_method staticfiles_tests.test_handlers_llm.test_get_response_async_exception_path_non_blocking_longer_sleep staticfiles_tests.test_handlers_llm.test_get_response_async_exception_path_non_blocking_short_sleep staticfiles_tests.test_handlers_llm.test_get_response_async_exception_path_non_blocking_tiny_sleep staticfiles_tests.test_handlers_llm.test_get_response_async_multiple_concurrent_calls_do_not_block_each_other staticfiles_tests.test_handlers_llm.test_get_response_async_non_blocking_bound_method staticfiles_tests.test_handlers_llm.test_get_response_async_non_blocking_longer_sleep staticfiles_tests.test_handlers_llm.test_get_response_async_non_blocking_multiple_quick_yields staticfiles_tests.test_handlers_llm.test_get_response_async_non_blocking_short_sleep staticfiles_tests.test_handlers_llm.test_get_response_async_non_blocking_tiny_sleep
coverage json -o coverage.json
: '>>>>> End Test Output'
