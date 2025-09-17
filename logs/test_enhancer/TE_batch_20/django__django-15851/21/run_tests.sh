#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 dbshell.test_postgresql_llm.test_multiple_parameter_flags_preserve_order_before_dbname dbshell.test_postgresql_llm.test_parameters_before_dbname_user_host_port dbshell.test_postgresql_llm.test_parameters_before_default_postgres_when_name_missing dbshell.test_postgresql_llm.test_parameters_empty_list_results_in_only_dbname dbshell.test_postgresql_llm.test_parameters_not_duplicated dbshell.test_postgresql_llm.test_parameters_order_with_ipv6_and_special_user dbshell.test_postgresql_llm.test_parameters_unicode_and_accent_preserved dbshell.test_postgresql_llm.test_parameters_with_dbname_like_parameter_preserves_order dbshell.test_postgresql_llm.test_parameters_with_passfile_and_service_and_parameters dbshell.test_postgresql_llm.test_parameters_with_service_and_parameters
coverage json -o coverage.json
: '>>>>> End Test Output'
