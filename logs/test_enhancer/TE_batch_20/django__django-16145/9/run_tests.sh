#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ManageRunserverAddrFormatting.setUp admin_scripts.tests_llm.ManageRunserverAddrFormatting.test_bracketed_ipv6_addrport_prints_brackets admin_scripts.tests_llm.ManageRunserverAddrFormatting.test_custom_defaults_print admin_scripts.tests_llm.ManageRunserverAddrFormatting.test_default_addr_prints_127001_when_no_addr_and_no_ipv6 admin_scripts.tests_llm.ManageRunserverAddrFormatting.test_fqdn_prints_fqdn admin_scripts.tests_llm.ManageRunserverAddrFormatting.test_hostname_prints_hostname admin_scripts.tests_llm.ManageRunserverAddrFormatting.test_ipv6_hostname_with_use_ipv6_flag_prints_hostname_without_brackets admin_scripts.tests_llm.ManageRunserverAddrFormatting.test_use_ipv6_default_prints_brackets admin_scripts.tests_llm.ManageRunserverAddrFormatting.test_zero_ip_addr_with_checks admin_scripts.tests_llm.ManageRunserverAddrFormatting.test_zero_ip_addr_without_checks
coverage json -o coverage.json
: '>>>>> End Test Output'
