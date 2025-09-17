#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.RunserverAddressFormattingTests.setUp admin_scripts.tests_llm.RunserverAddressFormattingTests.test_addrport_without_host_only_port admin_scripts.tests_llm.RunserverAddressFormattingTests.test_custom_port_reflected_in_output admin_scripts.tests_llm.RunserverAddressFormattingTests.test_hostname_display_unchanged admin_scripts.tests_llm.RunserverAddressFormattingTests.test_ipv4_address_display_unchanged admin_scripts.tests_llm.RunserverAddressFormattingTests.test_ipv6_addr_with_use_ipv6_flag_and_port admin_scripts.tests_llm.RunserverAddressFormattingTests.test_raw_ipv6_bracketed_in_output admin_scripts.tests_llm.RunserverAddressFormattingTests.test_run_called_with_correct_port admin_scripts.tests_llm.RunserverAddressFormattingTests.test_use_ipv6_default_addr_is_bracketed admin_scripts.tests_llm.RunserverAddressFormattingTests.test_zero_address_displays_0_0_0_0
coverage json -o coverage.json
: '>>>>> End Test Output'
