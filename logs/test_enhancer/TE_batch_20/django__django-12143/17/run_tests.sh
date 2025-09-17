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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.tests_llm.RegexPrefixTests._assert_list_editable_queryset_filtered admin_changelist.tests_llm.RegexPrefixTests._assert_prefix_extracts_pks admin_changelist.tests_llm.RegexPrefixTests._make_two_swallow_posts admin_changelist.tests_llm.RegexPrefixTests.setUp admin_changelist.tests_llm.RegexPrefixTests.setUpTestData
coverage json -o coverage.json
: '>>>>> End Test Output'
