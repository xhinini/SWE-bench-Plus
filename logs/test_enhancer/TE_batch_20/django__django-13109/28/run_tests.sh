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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyValidateTests.setUp model_forms.test_models_llm.ForeignKeyValidateTests.tearDown model_forms.test_models_llm.ForeignKeyValidateTests.test_archived_instance_allowed model_forms.test_models_llm.ForeignKeyValidateTests.test_archived_pk_int_allowed model_forms.test_models_llm.ForeignKeyValidateTests.test_archived_pk_str_allowed model_forms.test_models_llm.ForeignKeyValidateTests.test_limit_choices_to_callable_dict_allows_when_unrestrictive model_forms.test_models_llm.ForeignKeyValidateTests.test_limit_choices_to_callable_dict_restricts model_forms.test_models_llm.ForeignKeyValidateTests.test_limit_choices_to_callable_q_allows_when_unrestrictive model_forms.test_models_llm.ForeignKeyValidateTests.test_limit_choices_to_callable_q_restricts model_forms.test_models_llm.ForeignKeyValidateTests.test_multiple_archived_objects_exist_validate_accepts model_forms.test_models_llm.ForeignKeyValidateTests.test_nonexistent_pk_raises model_forms.test_models_llm.ForeignKeyValidateTests.test_parent_link_skips_validation
coverage json -o coverage.json
: '>>>>> End Test Output'
