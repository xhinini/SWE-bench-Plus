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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 check_framework.test_translation_llm.TranslationConsistencyRegressionTests._assert_inconsistent_with_patched_wrapper check_framework.test_translation_llm.TranslationConsistencyRegressionTests._make_raise_lookup check_framework.test_translation_llm.TranslationConsistencyRegressionTests.test_inconsistent_ca_ES_valencia check_framework.test_translation_llm.TranslationConsistencyRegressionTests.test_inconsistent_de check_framework.test_translation_llm.TranslationConsistencyRegressionTests.test_inconsistent_en_us check_framework.test_translation_llm.TranslationConsistencyRegressionTests.test_inconsistent_es_419 check_framework.test_translation_llm.TranslationConsistencyRegressionTests.test_inconsistent_fr check_framework.test_translation_llm.TranslationConsistencyRegressionTests.test_inconsistent_fr_CA check_framework.test_translation_llm.TranslationConsistencyRegressionTests.test_inconsistent_mas check_framework.test_translation_llm.TranslationConsistencyRegressionTests.test_inconsistent_sgn_ase check_framework.test_translation_llm.TranslationConsistencyRegressionTests.test_inconsistent_sr_Latn check_framework.test_translation_llm.TranslationConsistencyRegressionTests.test_inconsistent_zh_Hans
coverage json -o coverage.json
: '>>>>> End Test Output'
