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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.RelatedFieldValidateBaseManagerTests.setUp model_forms.test_models_llm.RelatedFieldValidateBaseManagerTests.test_fk_validate_instance_saved_article model_forms.test_models_llm.RelatedFieldValidateBaseManagerTests.test_fk_validate_instance_unsaved_article model_forms.test_models_llm.RelatedFieldValidateBaseManagerTests.test_fk_validate_pk_saved_article model_forms.test_models_llm.RelatedFieldValidateBaseManagerTests.test_fk_validate_pk_unsaved_article model_forms.test_models_llm.RelatedFieldValidateBaseManagerTests.test_fk_validate_with_model_instance_none_instance model_forms.test_models_llm.RelatedFieldValidateBaseManagerTests.test_fk_validate_with_model_instance_none_pk model_forms.test_models_llm.RelatedFieldValidateBaseManagerTests.test_o2o_validate_instance_saved_profile model_forms.test_models_llm.RelatedFieldValidateBaseManagerTests.test_o2o_validate_instance_unsaved_profile model_forms.test_models_llm.RelatedFieldValidateBaseManagerTests.test_o2o_validate_pk_saved_profile model_forms.test_models_llm.RelatedFieldValidateBaseManagerTests.test_o2o_validate_pk_unsaved_profile
coverage json -o coverage.json
: '>>>>> End Test Output'
