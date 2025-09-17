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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.tests_llm.test_empty_fields_on_subclassed_model_returns_empty_dict model_forms.tests_llm.test_fields_empty_dict_keys_returns_empty_dict model_forms.tests_llm.test_fields_empty_dict_returns_empty_dict model_forms.tests_llm.test_fields_empty_frozenset_returns_empty_dict model_forms.tests_llm.test_fields_empty_list_returns_empty_dict model_forms.tests_llm.test_fields_empty_preserves_m2m_when_none model_forms.tests_llm.test_fields_empty_range_returns_empty_dict model_forms.tests_llm.test_fields_empty_set_returns_empty_dict model_forms.tests_llm.test_fields_empty_tuple_returns_empty_dict model_forms.tests_llm.test_fields_empty_with_exclude_returns_empty_dict
coverage json -o coverage.json
: '>>>>> End Test Output'
