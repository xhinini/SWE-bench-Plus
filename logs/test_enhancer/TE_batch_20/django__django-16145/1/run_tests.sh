#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.test_bracketed_ipv6_with_explicit_port_print admin_scripts.tests_llm.test_default_addr_ipv6_override_print admin_scripts.tests_llm.test_default_addr_override_print admin_scripts.tests_llm.test_invalid_ipv6_without_brackets_raises admin_scripts.tests_llm.test_ipv4_with_use_ipv6_flag_raises admin_scripts.tests_llm.test_starting_server_hostname_print admin_scripts.tests_llm.test_starting_server_ipv4_address_print admin_scripts.tests_llm.test_starting_server_ipv6_bracketed_print admin_scripts.tests_llm.test_use_ipv6_with_port_only_print admin_scripts.tests_llm.test_zero_addr_with_custom_port_print
coverage json -o coverage.json
: '>>>>> End Test Output'
