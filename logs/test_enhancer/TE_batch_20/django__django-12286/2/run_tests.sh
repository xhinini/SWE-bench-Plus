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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 check_framework.test_translation_llm.TranslationConsistencyImportTests._reload_checks_with check_framework.test_translation_llm.TranslationConsistencyImportTests.test_public_ok_transreal_raises_fr check_framework.test_translation_llm.TranslationConsistencyImportTests.test_public_ok_transreal_raises_zh_hans check_framework.test_translation_llm.TranslationConsistencyImportTests.test_public_raises_transreal_ok_en_us check_framework.test_translation_llm.TranslationConsistencyImportTests.test_public_raises_transreal_ok_es_419 check_framework.test_translation_llm.TranslationConsistencyImportTests.test_public_raises_transreal_ok_sr_latn
coverage json -o coverage.json
: '>>>>> End Test Output'
