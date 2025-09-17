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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.PkDefaultSaveTests.test_boolpk_explicit_pk_true_with_update_fields serializers.models.test_data_llm.PkDefaultSaveTests.test_intpk_explicit_pk_save_with_update_fields_frozenset serializers.models.test_data_llm.PkDefaultSaveTests.test_intpk_explicit_pk_save_with_update_fields_list serializers.models.test_data_llm.PkDefaultSaveTests.test_intpk_explicit_pk_save_with_update_fields_set serializers.models.test_data_llm.PkDefaultSaveTests.test_intpk_explicit_pk_save_with_update_fields_tuple serializers.models.test_data_llm.PkDefaultSaveTests.test_intpk_explicit_pk_zero_and_update_fields serializers.models.test_data_llm.PkDefaultSaveTests.test_multiple_saves_with_different_update_fields_variants serializers.models.test_data_llm.PkDefaultSaveTests.test_save_does_not_raise_database_error_when_update_fields_provided serializers.models.test_data_llm.PkDefaultSaveTests.test_uuidpk_explicit_pk_with_update_fields serializers.models.test_data_llm.PkDefaultSaveTests.test_uuidpk_explicit_pk_with_update_fields_tuple serializers.models.test_data_llm.[] (serializers.models.test_data_llm.BoolPKDefaultModel) serializers.models.test_data_llm.[] (serializers.models.test_data_llm.IntPKDefaultModel) serializers.models.test_data_llm.[] (serializers.models.test_data_llm.UUIDPKDefaultModel)
coverage json -o coverage.json
: '>>>>> End Test Output'
