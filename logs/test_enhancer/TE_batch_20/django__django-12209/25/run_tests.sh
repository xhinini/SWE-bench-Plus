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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.ForceInsertDecisionTests._perform_save_and_capture serializers.models.test_data_llm.ForceInsertDecisionTests.test_booleanpk_explicit_pk_non_raw_uses_insert serializers.models.test_data_llm.ForceInsertDecisionTests.test_booleanpk_explicit_pk_raw_uses_update serializers.models.test_data_llm.ForceInsertDecisionTests.test_booleanpk_no_explicit_pk_non_raw_uses_insert serializers.models.test_data_llm.ForceInsertDecisionTests.test_booleanpk_no_explicit_pk_raw_uses_update serializers.models.test_data_llm.ForceInsertDecisionTests.test_uuiddefault_explicit_pk_non_raw_uses_insert serializers.models.test_data_llm.ForceInsertDecisionTests.test_uuiddefault_explicit_pk_raw_uses_update serializers.models.test_data_llm.ForceInsertDecisionTests.test_uuiddefault_no_explicit_pk_non_raw_uses_insert serializers.models.test_data_llm.ForceInsertDecisionTests.test_uuiddefault_no_explicit_pk_raw_uses_update serializers.models.test_data_llm.ForceInsertDecisionTests.test_uuiddefault_save_base_non_raw_uses_insert serializers.models.test_data_llm.ForceInsertDecisionTests.test_uuiddefault_save_base_raw_true_uses_update
coverage json -o coverage.json
: '>>>>> End Test Output'
