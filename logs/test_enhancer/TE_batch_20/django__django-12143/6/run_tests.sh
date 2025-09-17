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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.tests_llm.test_get_edited_object_pks_with_backslash_prefix admin_changelist.tests_llm.test_get_edited_object_pks_with_bracket_prefix admin_changelist.tests_llm.test_get_edited_object_pks_with_dot_prefix admin_changelist.tests_llm.test_get_edited_object_pks_with_parentheses_prefix admin_changelist.tests_llm.test_get_edited_object_pks_with_pipe_and_caret_prefixes admin_changelist.tests_llm.test_get_edited_object_pks_with_plus_prefix admin_changelist.tests_llm.test_get_edited_object_pks_with_star_prefix admin_changelist.tests_llm.test_get_list_editable_queryset_with_invalid_pk_returns_unfiltered admin_changelist.tests_llm.test_get_list_editable_queryset_with_various_regex_like_prefixes
coverage json -o coverage.json
: '>>>>> End Test Output'
