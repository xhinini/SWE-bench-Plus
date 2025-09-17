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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 check_framework.test_translation_llm.TranslationConsistencyReloadPatchTests.setUp check_framework.test_translation_llm.TranslationConsistencyReloadPatchTests.tearDown check_framework.test_translation_llm.TranslationConsistencyReloadPatchTests.test_decorator_patch_raises_lookuperror_it check_framework.test_translation_llm.TranslationConsistencyReloadPatchTests.test_decorator_patch_raises_lookuperror_ja check_framework.test_translation_llm.TranslationConsistencyReloadPatchTests.test_decorator_patch_raises_lookuperror_pt check_framework.test_translation_llm.TranslationConsistencyReloadPatchTests.test_decorator_patch_raises_lookuperror_ru check_framework.test_translation_llm.TranslationConsistencyReloadPatchTests.test_decorator_patch_raises_lookuperror_sv check_framework.test_translation_llm.TranslationConsistencyReloadPatchTests.test_patch_raises_lookuperror_ca_es_variant_language check_framework.test_translation_llm.TranslationConsistencyReloadPatchTests.test_patch_raises_lookuperror_en_us_language check_framework.test_translation_llm.TranslationConsistencyReloadPatchTests.test_patch_raises_lookuperror_es_419_language check_framework.test_translation_llm.TranslationConsistencyReloadPatchTests.test_patch_raises_lookuperror_fr_language check_framework.test_translation_llm.TranslationConsistencyReloadPatchTests.test_patch_raises_lookuperror_zh_hans_language
coverage json -o coverage.json
: '>>>>> End Test Output'
